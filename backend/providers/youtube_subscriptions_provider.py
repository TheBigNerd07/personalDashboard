from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import re
from typing import Any, Dict, List
from xml.etree import ElementTree as ET

import httpx

from backend.providers.base import BaseProvider

ATOM_NS = "{http://www.w3.org/2005/Atom}"
YT_NS = "{http://www.youtube.com/xml/schemas/2015}"


class YouTubeSubscriptionsProvider(BaseProvider):
    name = "youtube_subscriptions"

    def __init__(
        self,
        channel_ids: List[str],
        enabled: bool = True,
        poll_interval: float = 60.0,
        cache_ttl: float = 20.0,
        timeout_s: float = 8.0,
        max_videos: int = 15,
    ):
        super().__init__(enabled=enabled, poll_interval=poll_interval, cache_ttl=cache_ttl)
        self.channel_ids = [cid.strip() for cid in channel_ids if cid and cid.strip()]
        self.timeout_s = timeout_s
        self.max_videos = max(1, max_videos)

    @staticmethod
    def _extract_channel_id_from_ref(channel_ref: str) -> str | None:
        ref = (channel_ref or "").strip()
        if not ref:
            return None

        if ref.startswith("UC") and len(ref) >= 24:
            return ref

        if "youtube.com/channel/" in ref:
            match = re.search(r"/channel/(UC[\w-]{22,})", ref)
            if match:
                return match.group(1)

        return None

    async def _resolve_channel_ref(self, client: httpx.AsyncClient, channel_ref: str) -> Dict[str, Any]:
        direct_id = self._extract_channel_id_from_ref(channel_ref)
        if direct_id:
            return {"ok": True, "ref": channel_ref, "channel_id": direct_id}

        ref = (channel_ref or "").strip()
        if not ref:
            return {"ok": False, "ref": channel_ref, "error": "Empty channel reference"}

        if ref.startswith("@"):
            url = f"https://www.youtube.com/{ref}"
        elif ref.startswith("http://") or ref.startswith("https://"):
            url = ref
        else:
            url = f"https://www.youtube.com/{ref.lstrip('/')}"

        # First try oEmbed, which often exposes stable author_url=/channel/UC...
        try:
            oembed_url = "https://www.youtube.com/oembed"
            oembed_resp = await client.get(
                oembed_url,
                params={"url": url, "format": "json"},
                follow_redirects=True,
            )
            if oembed_resp.status_code == 200:
                data = oembed_resp.json()
                author_url = (data.get("author_url") or "").strip()
                oembed_id = self._extract_channel_id_from_ref(author_url)
                if oembed_id:
                    return {"ok": True, "ref": channel_ref, "channel_id": oembed_id}
        except Exception:
            pass

        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            html = response.text

            # Try several metadata patterns YouTube may emit.
            patterns = [
                r'"channelId":"(UC[\w-]{22,})"',
                r'"externalId":"(UC[\w-]{22,})"',
                r'"browseId":"(UC[\w-]{22,})"',
            ]
            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    return {"ok": True, "ref": channel_ref, "channel_id": match.group(1)}
            return {"ok": False, "ref": channel_ref, "error": "Could not resolve channel ID"}
        except Exception as exc:
            return {"ok": False, "ref": channel_ref, "error": self._format_exception(exc)}

    @staticmethod
    def _format_exception(exc: Exception) -> str:
        response = getattr(exc, "response", None)
        if response is not None:
            status = getattr(response, "status_code", "unknown")
            return f"HTTP {status} from provider"
        message = str(exc).strip()
        if not message:
            return exc.__class__.__name__
        return message.split(" For more information", 1)[0]

    async def _fetch_channel_feed(self, client: httpx.AsyncClient, channel_id: str) -> Dict[str, Any]:
        feed_urls = [
            f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
            # Uploads playlist feed often works even when channel feed is flaky.
            f"https://www.youtube.com/feeds/videos.xml?playlist_id=UU{channel_id[2:]}",
        ]

        last_exc: Exception | None = None
        root = None
        for url in feed_urls:
            try:
                response = await client.get(
                    url,
                    headers={"User-Agent": "personalDashboard/1.0", "Accept": "application/atom+xml, application/xml"},
                )
                response.raise_for_status()
                root = ET.fromstring(response.text)
                break
            except Exception as exc:
                last_exc = exc

        if root is None:
            raise last_exc if last_exc is not None else ValueError("Unable to fetch channel feed")

        channel_title = (root.findtext(f"{ATOM_NS}title") or "").strip()

        entries = []
        for entry in root.findall(f"{ATOM_NS}entry"):
            title = (entry.findtext(f"{ATOM_NS}title") or "").strip()
            video_id = (entry.findtext(f"{YT_NS}videoId") or "").strip()
            published = (entry.findtext(f"{ATOM_NS}published") or "").strip()
            author_name = (entry.findtext(f"{ATOM_NS}author/{ATOM_NS}name") or channel_title).strip()
            link = entry.find(f"{ATOM_NS}link")
            href = link.attrib.get("href", "") if link is not None else ""

            if not video_id:
                continue

            entries.append(
                {
                    "video_id": video_id,
                    "title": title,
                    "channel_id": channel_id,
                    "channel_title": author_name,
                    "published_at": published,
                    "url": href or f"https://www.youtube.com/watch?v={video_id}",
                }
            )

        return {
            "channel_id": channel_id,
            "channel_title": channel_title,
            "entries": entries,
        }

    async def fetch(self) -> Dict[str, Any]:
        if not self.channel_ids:
            return {"feeds": [], "errors": [{"message": "No channel IDs configured"}]}

        timeout = httpx.Timeout(self.timeout_s)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resolved = await asyncio.gather(
                *(self._resolve_channel_ref(client, channel_ref) for channel_ref in self.channel_ids)
            )

            resolved_ids = []
            seen = set()
            errors = []
            for item in resolved:
                if item.get("ok"):
                    cid = item["channel_id"]
                    if cid not in seen:
                        seen.add(cid)
                        resolved_ids.append(cid)
                else:
                    errors.append({"channel_ref": item.get("ref"), "message": item.get("error", "resolve failed")})

            results = await asyncio.gather(
                *(self._fetch_channel_feed(client, channel_id) for channel_id in resolved_ids),
                return_exceptions=True,
            )

        feeds = []
        for channel_id, result in zip(resolved_ids, results):
            if isinstance(result, Exception):
                errors.append({"channel_id": channel_id, "message": self._format_exception(result)})
            else:
                feeds.append(result)

        return {
            "feeds": feeds,
            "errors": errors,
            "resolved_channels": len(resolved_ids),
        }

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        videos = []
        for feed in raw.get("feeds", []):
            videos.extend(feed.get("entries", []))

        def _parse_time(value: str) -> datetime:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except Exception:
                return datetime.fromtimestamp(0, tz=timezone.utc)

        videos.sort(key=lambda item: _parse_time(item.get("published_at", "")), reverse=True)
        videos = videos[: self.max_videos]

        return {
            "summary": {
                "configured_channels": len(self.channel_ids),
                "resolved_channels": int(raw.get("resolved_channels", 0)),
                "fetched_channels": len(raw.get("feeds", [])),
                "errors": len(raw.get("errors", [])),
                "videos": len(videos),
            },
            "videos": videos,
            "errors": raw.get("errors", []),
        }
