const cardsContainer = document.getElementById("cards");
const cardTemplate = document.getElementById("card-template");
const summaryEl = document.getElementById("summary");
const togglePauseBtn = document.getElementById("toggle-pause");
const toggleArrangeBtn = document.getElementById("toggle-arrange");
const setRateBtn = document.getElementById("set-rate");
const refreshNowBtn = document.getElementById("refresh-now");
const exportBtn = document.getElementById("export-json");
const openSettingsBtn = document.getElementById("open-settings");
const closeSettingsBtn = document.getElementById("close-settings");
const reloadSettingsBtn = document.getElementById("reload-settings");
const saveSettingsBtn = document.getElementById("save-settings");
const settingsModal = document.getElementById("settings-modal");
const settingsStatus = document.getElementById("settings-status");
const settingsSearchInput = document.getElementById("settings-search-input");
const settingsGroupFilter = document.getElementById("settings-group-filter");
const settingsExpandAllBtn = document.getElementById("settings-expand-all");
const settingsCollapseAllBtn = document.getElementById("settings-collapse-all");
const settingsSubmenuButtons = [...document.querySelectorAll(".settings-submenu-btn")];
const rateInput = document.getElementById("refresh-rate");
const wallboardBtn = document.getElementById("wallboard-toggle");
const searchInput = document.getElementById("search-input");
const statusFilter = document.getElementById("status-filter");
const categoryFilter = document.getElementById("category-filter");
const brandPaletteSelect = document.getElementById("brand-palette");
const layoutModeSelect = document.getElementById("layout-mode");
const densityModeSelect = document.getElementById("density-mode");
const toggleGlanceBtn = document.getElementById("toggle-glance");
const cfgUnitSystem = document.getElementById("cfg-unit-system");
const cfgBrandPalette = document.getElementById("cfg-brand-palette");

const cfgGlobalRefreshRate = document.getElementById("cfg-global-refresh-rate");
const cfgHistorySize = document.getElementById("cfg-history-size");
const cfgWeatherEnabled = document.getElementById("cfg-weather-enabled");
const cfgWeatherCity = document.getElementById("cfg-weather-city");
const cfgWeatherLatitude = document.getElementById("cfg-weather-latitude");
const cfgWeatherLongitude = document.getElementById("cfg-weather-longitude");
const cfgWeatherPoll = document.getElementById("cfg-weather-poll");
const cfgWeatherTtl = document.getElementById("cfg-weather-ttl");
const cfgSystemEnabled = document.getElementById("cfg-system-enabled");
const cfgSystemTimezones = document.getElementById("cfg-system-timezones");
const cfgSystemPoll = document.getElementById("cfg-system-poll");
const cfgSystemTtl = document.getElementById("cfg-system-ttl");
const cfgStock1Enabled = document.getElementById("cfg-stock1-enabled");
const cfgStock1Symbol = document.getElementById("cfg-stock1-symbol");
const cfgStock1Poll = document.getElementById("cfg-stock1-poll");
const cfgStock1Ttl = document.getElementById("cfg-stock1-ttl");
const cfgStock1Timeout = document.getElementById("cfg-stock1-timeout");
const cfgStock2Enabled = document.getElementById("cfg-stock2-enabled");
const cfgStock2Symbol = document.getElementById("cfg-stock2-symbol");
const cfgStock2Poll = document.getElementById("cfg-stock2-poll");
const cfgStock2Ttl = document.getElementById("cfg-stock2-ttl");
const cfgStock2Timeout = document.getElementById("cfg-stock2-timeout");
const cfgStock3Enabled = document.getElementById("cfg-stock3-enabled");
const cfgStock3Symbol = document.getElementById("cfg-stock3-symbol");
const cfgStock3Poll = document.getElementById("cfg-stock3-poll");
const cfgStock3Ttl = document.getElementById("cfg-stock3-ttl");
const cfgStock3Timeout = document.getElementById("cfg-stock3-timeout");
const cfgStatusEnabled = document.getElementById("cfg-status-enabled");
const cfgStatusPoll = document.getElementById("cfg-status-poll");
const cfgStatusTtl = document.getElementById("cfg-status-ttl");
const cfgStatusTimeout = document.getElementById("cfg-status-timeout");
const cfgStatusServices = document.getElementById("cfg-status-services");
const cfgHeartbeatEnabled = document.getElementById("cfg-heartbeat-enabled");
const cfgHeartbeatPoll = document.getElementById("cfg-heartbeat-poll");
const cfgHeartbeatTtl = document.getElementById("cfg-heartbeat-ttl");
const cfgSevereEnabled = document.getElementById("cfg-severe-enabled");
const cfgSeverePoll = document.getElementById("cfg-severe-poll");
const cfgSevereTtl = document.getElementById("cfg-severe-ttl");
const cfgSevereTimeout = document.getElementById("cfg-severe-timeout");
const cfgSevereTopn = document.getElementById("cfg-severe-topn");
const cfgSevereCities = document.getElementById("cfg-severe-cities");
const cfgYoutubeEnabled = document.getElementById("cfg-youtube-enabled");
const cfgYoutubePoll = document.getElementById("cfg-youtube-poll");
const cfgYoutubeTtl = document.getElementById("cfg-youtube-ttl");
const cfgYoutubeTimeout = document.getElementById("cfg-youtube-timeout");
const cfgYoutubeMax = document.getElementById("cfg-youtube-max");
const cfgYoutubeChannels = document.getElementById("cfg-youtube-channels");
const cfgTravelEnabled = document.getElementById("cfg-travel-enabled");
const cfgTravelPoll = document.getElementById("cfg-travel-poll");
const cfgTravelTtl = document.getElementById("cfg-travel-ttl");
const cfgTravelTimeout = document.getElementById("cfg-travel-timeout");
const cfgTravelOrigin = document.getElementById("cfg-travel-origin");
const cfgTravelDests = document.getElementById("cfg-travel-dests");
const cfgCryptoEnabled = document.getElementById("cfg-crypto-enabled");
const cfgCryptoSymbol = document.getElementById("cfg-crypto-symbol");
const cfgCryptoPoll = document.getElementById("cfg-crypto-poll");
const cfgCryptoTtl = document.getElementById("cfg-crypto-ttl");
const cfgCryptoTimeout = document.getElementById("cfg-crypto-timeout");
const cfgHnEnabled = document.getElementById("cfg-hn-enabled");
const cfgHnTopn = document.getElementById("cfg-hn-topn");
const cfgHnPoll = document.getElementById("cfg-hn-poll");
const cfgHnTtl = document.getElementById("cfg-hn-ttl");
const cfgHnTimeout = document.getElementById("cfg-hn-timeout");
const cfgEarthEnabled = document.getElementById("cfg-earth-enabled");
const cfgEarthMax = document.getElementById("cfg-earth-max");
const cfgEarthPoll = document.getElementById("cfg-earth-poll");
const cfgEarthTtl = document.getElementById("cfg-earth-ttl");
const cfgEarthTimeout = document.getElementById("cfg-earth-timeout");
const cfgSunEnabled = document.getElementById("cfg-sun-enabled");
const cfgSunLatitude = document.getElementById("cfg-sun-latitude");
const cfgSunLongitude = document.getElementById("cfg-sun-longitude");
const cfgSunPoll = document.getElementById("cfg-sun-poll");
const cfgSunTtl = document.getElementById("cfg-sun-ttl");
const cfgSunTimeout = document.getElementById("cfg-sun-timeout");
const cfgAirEnabled = document.getElementById("cfg-air-enabled");
const cfgAirLatitude = document.getElementById("cfg-air-latitude");
const cfgAirLongitude = document.getElementById("cfg-air-longitude");
const cfgAirPoll = document.getElementById("cfg-air-poll");
const cfgAirTtl = document.getElementById("cfg-air-ttl");
const cfgAirTimeout = document.getElementById("cfg-air-timeout");
const cfgIssEnabled = document.getElementById("cfg-iss-enabled");
const cfgIssPoll = document.getElementById("cfg-iss-poll");
const cfgIssTtl = document.getElementById("cfg-iss-ttl");
const cfgIssTimeout = document.getElementById("cfg-iss-timeout");
const cfgDnsEnabled = document.getElementById("cfg-dns-enabled");
const cfgDnsHosts = document.getElementById("cfg-dns-hosts");
const cfgDnsPoll = document.getElementById("cfg-dns-poll");
const cfgDnsTtl = document.getElementById("cfg-dns-ttl");
const cfgIndicesEnabled = document.getElementById("cfg-indices-enabled");
const cfgIndicesSymbols = document.getElementById("cfg-indices-symbols");
const cfgIndicesPoll = document.getElementById("cfg-indices-poll");
const cfgIndicesTtl = document.getElementById("cfg-indices-ttl");
const cfgIndicesTimeout = document.getElementById("cfg-indices-timeout");
const cfgFxEnabled = document.getElementById("cfg-fx-enabled");
const cfgFxBase = document.getElementById("cfg-fx-base");
const cfgFxSymbols = document.getElementById("cfg-fx-symbols");
const cfgFxPoll = document.getElementById("cfg-fx-poll");
const cfgFxTtl = document.getElementById("cfg-fx-ttl");
const cfgFxTimeout = document.getElementById("cfg-fx-timeout");
const cfgSpaceEnabled = document.getElementById("cfg-space-enabled");
const cfgSpacePoll = document.getElementById("cfg-space-poll");
const cfgSpaceTtl = document.getElementById("cfg-space-ttl");
const cfgSpaceTimeout = document.getElementById("cfg-space-timeout");
const cfgQuoteEnabled = document.getElementById("cfg-quote-enabled");
const cfgQuotePoll = document.getElementById("cfg-quote-poll");
const cfgQuoteTtl = document.getElementById("cfg-quote-ttl");
const cfgQuoteTimeout = document.getElementById("cfg-quote-timeout");
const cfgMempoolEnabled = document.getElementById("cfg-mempool-enabled");
const cfgMempoolPoll = document.getElementById("cfg-mempool-poll");
const cfgMempoolTtl = document.getElementById("cfg-mempool-ttl");
const cfgMempoolTimeout = document.getElementById("cfg-mempool-timeout");
const cfgNasaEnabled = document.getElementById("cfg-nasa-enabled");
const cfgNasaLimit = document.getElementById("cfg-nasa-limit");
const cfgNasaPoll = document.getElementById("cfg-nasa-poll");
const cfgNasaTtl = document.getElementById("cfg-nasa-ttl");
const cfgNasaTimeout = document.getElementById("cfg-nasa-timeout");
const cfgXrayEnabled = document.getElementById("cfg-xray-enabled");
const cfgXrayPoll = document.getElementById("cfg-xray-poll");
const cfgXrayTtl = document.getElementById("cfg-xray-ttl");
const cfgXrayTimeout = document.getElementById("cfg-xray-timeout");
const cfgCryptoGlobalEnabled = document.getElementById("cfg-crypto-global-enabled");
const cfgCryptoGlobalPoll = document.getElementById("cfg-crypto-global-poll");
const cfgCryptoGlobalTtl = document.getElementById("cfg-crypto-global-ttl");
const cfgCryptoGlobalTimeout = document.getElementById("cfg-crypto-global-timeout");
const cfgLaunchesEnabled = document.getElementById("cfg-launches-enabled");
const cfgLaunchesLimit = document.getElementById("cfg-launches-limit");
const cfgLaunchesPoll = document.getElementById("cfg-launches-poll");
const cfgLaunchesTtl = document.getElementById("cfg-launches-ttl");
const cfgLaunchesTimeout = document.getElementById("cfg-launches-timeout");

let paused = false;
let fetchInterval = null;
let snapshotCache = null;
let settingsCache = null;
let currentUnitSystem = "metric";
let currentBrandPalette = "fleet";
let arrangeMode = false;
let cardOrder = [];
let lastVisualSignature = "";
let lastTimestampRefreshAt = 0;
let lastSummarySignature = "";
const CARD_ORDER_STORAGE_KEY = "dashboard_card_order_v1";
const BRAND_PALETTE_STORAGE_KEY = "dashboard_brand_palette_v1";
const SETTINGS_COLLAPSE_STORAGE_KEY = "dashboard_settings_collapsed_v1";
const LAYOUT_MODE_STORAGE_KEY = "dashboard_layout_mode_v1";
const DENSITY_MODE_STORAGE_KEY = "dashboard_density_mode_v1";
const GLANCE_MODE_STORAGE_KEY = "dashboard_glance_mode_v1";
const BRAND_PALETTES = {
  fleet: { bg: "#E9EEF6", bg_alt: "#DCE5F1", surface: "#F8FAFD", text: "#101B2D", muted: "#55657E", accent: "#1657A5", ok: "#158B5C", warn: "#A76A16", error: "#BE3B30" },
  boeing: { bg: "#E8EEF5", bg_alt: "#D5E0EE", surface: "#F7FAFD", text: "#0D1B2A", muted: "#4C5D73", accent: "#0039A6", ok: "#1C8B5A", warn: "#9E7212", error: "#BF3A2A" },
  alaska: { bg: "#EAF4F2", bg_alt: "#D9EBE7", surface: "#F7FCFB", text: "#102329", muted: "#4A646A", accent: "#006D77", ok: "#238A64", warn: "#9A7418", error: "#B64236" },
  jetblue: { bg: "#EAF0F9", bg_alt: "#DCE6F5", surface: "#F8FBFE", text: "#0F1D3A", muted: "#4E5F82", accent: "#00205B", ok: "#208C66", warn: "#9A6D1B", error: "#B53C32" },
  blueorigin: { bg: "#ECEFF4", bg_alt: "#DEE3EC", surface: "#FAFBFD", text: "#0E1520", muted: "#515D71", accent: "#1E3A8A", ok: "#1E8A61", warn: "#9B6E1A", error: "#B13B31" },
};
const DEFAULT_BRAND_PALETTE = "fleet";
const DEFAULT_LAYOUT_MODE = "auto";
const DEFAULT_DENSITY_MODE = "max";
const DEFAULT_GLANCE_MODE = true;

let preferredLayoutMode = DEFAULT_LAYOUT_MODE;
let preferredDensityMode = DEFAULT_DENSITY_MODE;
let glanceMode = DEFAULT_GLANCE_MODE;

function toTitle(text) {
  return text.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function normalizeHexColor(value, fallback) {
  const raw = (value || "").trim();
  if (!raw) return fallback;
  const prefixed = raw.startsWith("#") ? raw : `#${raw}`;
  if (/^#[0-9a-fA-F]{3}$/.test(prefixed)) {
    const r = prefixed[1];
    const g = prefixed[2];
    const b = prefixed[3];
    return `#${r}${r}${g}${g}${b}${b}`.toUpperCase();
  }
  if (/^#[0-9a-fA-F]{6}$/.test(prefixed)) {
    return prefixed.toUpperCase();
  }
  return fallback;
}

function hexToRgb(hex) {
  const value = normalizeHexColor(hex, "#000000");
  return {
    r: parseInt(value.slice(1, 3), 16),
    g: parseInt(value.slice(3, 5), 16),
    b: parseInt(value.slice(5, 7), 16),
  };
}

function rgbaFromHex(hex, alpha) {
  const { r, g, b } = hexToRgb(hex);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function buildTheme(theme = {}) {
  const fallback = BRAND_PALETTES[currentBrandPalette] || BRAND_PALETTES[DEFAULT_BRAND_PALETTE];
  return {
    bg: normalizeHexColor(theme.bg, fallback.bg),
    bg_alt: normalizeHexColor(theme.bg_alt, fallback.bg_alt),
    surface: normalizeHexColor(theme.surface, fallback.surface),
    text: normalizeHexColor(theme.text, fallback.text),
    muted: normalizeHexColor(theme.muted, fallback.muted),
    accent: normalizeHexColor(theme.accent, fallback.accent),
    ok: normalizeHexColor(theme.ok, fallback.ok),
    warn: normalizeHexColor(theme.warn, fallback.warn),
    error: normalizeHexColor(theme.error, fallback.error),
  };
}

function normalizeBrandPalette(value) {
  const raw = String(value || "").toLowerCase();
  return BRAND_PALETTES[raw] ? raw : DEFAULT_BRAND_PALETTE;
}

function loadBrandPalette() {
  const raw = localStorage.getItem(BRAND_PALETTE_STORAGE_KEY);
  return normalizeBrandPalette(raw);
}

function saveBrandPalette(palette) {
  localStorage.setItem(BRAND_PALETTE_STORAGE_KEY, normalizeBrandPalette(palette));
}

function normalizeLayoutMode(mode) {
  const raw = String(mode || "").toLowerCase();
  if (raw === "horizontal" || raw === "vertical") return raw;
  return DEFAULT_LAYOUT_MODE;
}

function normalizeDensityMode(mode) {
  const raw = String(mode || "").toLowerCase();
  if (raw === "comfortable" || raw === "dense" || raw === "max") return raw;
  return DEFAULT_DENSITY_MODE;
}

function loadLayoutMode() {
  return normalizeLayoutMode(localStorage.getItem(LAYOUT_MODE_STORAGE_KEY));
}

function saveLayoutMode(mode) {
  localStorage.setItem(LAYOUT_MODE_STORAGE_KEY, normalizeLayoutMode(mode));
}

function loadDensityMode() {
  return normalizeDensityMode(localStorage.getItem(DENSITY_MODE_STORAGE_KEY));
}

function saveDensityMode(mode) {
  localStorage.setItem(DENSITY_MODE_STORAGE_KEY, normalizeDensityMode(mode));
}

function loadGlanceMode() {
  const raw = localStorage.getItem(GLANCE_MODE_STORAGE_KEY);
  if (raw == null) return DEFAULT_GLANCE_MODE;
  return raw === "1";
}

function saveGlanceMode(enabled) {
  localStorage.setItem(GLANCE_MODE_STORAGE_KEY, enabled ? "1" : "0");
}

function activeOrientation() {
  if (preferredLayoutMode !== DEFAULT_LAYOUT_MODE) {
    return preferredLayoutMode;
  }
  return window.innerWidth >= window.innerHeight ? "horizontal" : "vertical";
}

function applyLayoutAndDensity() {
  const orientation = activeOrientation();
  document.body.dataset.orientation = orientation;
  document.body.dataset.layout = preferredLayoutMode;
  document.body.dataset.density = preferredDensityMode;
  document.body.classList.toggle("glance-mode", glanceMode);
  if (toggleGlanceBtn) {
    toggleGlanceBtn.textContent = glanceMode ? "Glance On" : "Glance Off";
  }
  if (layoutModeSelect) layoutModeSelect.value = preferredLayoutMode;
  if (densityModeSelect) densityModeSelect.value = preferredDensityMode;
}

function applyGlanceColumns(sourceCount) {
  if (!glanceMode) {
    cardsContainer.style.removeProperty("--glance-columns");
    return;
  }
  const orientation = activeOrientation();
  const targetRows = orientation === "horizontal" ? 4 : 5;
  const minCols = orientation === "horizontal" ? 4 : 3;
  const maxCols = orientation === "horizontal" ? 8 : 6;
  const calculated = Math.ceil(Math.max(sourceCount, 1) / targetRows);
  const cols = Math.max(minCols, Math.min(maxCols, calculated));
  cardsContainer.style.setProperty("--glance-columns", `${cols}`);
}

function applyTheme(theme = {}) {
  const t = buildTheme(theme);
  const root = document.documentElement;
  root.style.setProperty("--bg", "#0A111A");
  root.style.setProperty("--bg-alt", "#0E1826");
  root.style.setProperty("--bg-grad-end", "#132033");
  root.style.setProperty("--bg-glow-1", rgbaFromHex(t.accent, 0.26));
  root.style.setProperty("--bg-glow-2", rgbaFromHex(t.ok, 0.18));
  root.style.setProperty("--surface", "rgba(18, 28, 42, 0.84)");
  root.style.setProperty("--surface-strong", "rgba(14, 22, 35, 0.95)");
  root.style.setProperty("--text", "#E7EEF8");
  root.style.setProperty("--muted", "#A1B1C8");
  root.style.setProperty("--line", "rgba(161, 177, 200, 0.28)");
  root.style.setProperty("--line-soft", "rgba(161, 177, 200, 0.16)");
  root.style.setProperty("--blue", t.accent);
  root.style.setProperty("--blue-soft", rgbaFromHex(t.accent, 0.14));
  root.style.setProperty("--ok", t.ok);
  root.style.setProperty("--ok-soft", rgbaFromHex(t.ok, 0.15));
  root.style.setProperty("--warn", t.warn);
  root.style.setProperty("--warn-soft", rgbaFromHex(t.warn, 0.16));
  root.style.setProperty("--err", t.error);
  root.style.setProperty("--err-soft", rgbaFromHex(t.error, 0.14));
  root.style.setProperty("--toolbar-bg", "rgba(10, 17, 27, 0.82)");
  root.style.setProperty("--control-bg", "rgba(19, 30, 45, 0.9)");
  root.style.setProperty("--control-hover-border", rgbaFromHex(t.accent, 0.4));
  root.style.setProperty("--focus-ring", rgbaFromHex(t.accent, 0.2));
  root.style.setProperty("--settings-section-bg", "rgba(18, 29, 43, 0.88)");
  root.style.setProperty("--settings-section-border", "rgba(161, 177, 200, 0.2)");
  root.style.setProperty("--modal-overlay", "rgba(4, 8, 14, 0.62)");
  root.style.setProperty("--shadow-1", "0 12px 30px rgba(0, 0, 0, 0.32)");
  root.style.setProperty("--shadow-2", "0 26px 56px rgba(0, 0, 0, 0.46)");
}

function applyVisualSettings({ palette = DEFAULT_BRAND_PALETTE } = {}) {
  currentBrandPalette = normalizeBrandPalette(palette);
  document.body.dataset.brand = currentBrandPalette;
  if (brandPaletteSelect) brandPaletteSelect.value = currentBrandPalette;
  if (cfgBrandPalette) cfgBrandPalette.value = currentBrandPalette;
  applyTheme(BRAND_PALETTES[currentBrandPalette] || BRAND_PALETTES[DEFAULT_BRAND_PALETTE]);
}

function formatNumber(value, digits = 1) {
  if (typeof value !== "number") {
    return "-";
  }
  return Number.isInteger(value) ? `${value}` : value.toFixed(digits);
}

function formatCompactNumber(value) {
  if (typeof value !== "number") return "-";
  return new Intl.NumberFormat(undefined, { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

function formatTimestamp(msOrSeconds) {
  if (typeof msOrSeconds !== "number") return "-";
  const millis = msOrSeconds > 10_000_000_000 ? msOrSeconds : msOrSeconds * 1000;
  return new Date(millis).toLocaleString();
}

function isImperial() {
  return currentUnitSystem === "imperial";
}

function formatTempFromC(c) {
  if (typeof c !== "number") return "-";
  if (isImperial()) {
    const f = (c * 9) / 5 + 32;
    return `${formatNumber(f)}°F`;
  }
  return `${formatNumber(c)}°C`;
}

function formatWindFromKph(kph) {
  if (typeof kph !== "number") return "-";
  if (isImperial()) {
    const mph = kph * 0.621371;
    return `${formatNumber(mph)} mph`;
  }
  return `${formatNumber(kph)} km/h`;
}

function formatDistanceFromKm(km) {
  if (typeof km !== "number") return "-";
  if (isImperial()) {
    const mi = km * 0.621371;
    return `${formatNumber(mi)} mi`;
  }
  return `${formatNumber(km)} km`;
}

function relativeTime(dateIso) {
  if (!dateIso) {
    return "not available";
  }
  const seconds = Math.floor((Date.now() - new Date(dateIso).getTime()) / 1000);
  if (seconds < 2) {
    return "just now";
  }
  if (seconds < 60) {
    return `${seconds}s ago`;
  }
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return `${minutes}m ago`;
  }
  return `${Math.floor(minutes / 60)}h ago`;
}

function row(key, value, mono = false) {
  return `<div class="kv"><span class="k">${key}</span><span class="v${mono ? " mono" : ""}">${value}</span></div>`;
}

function inferSettingsGroup(title) {
  const text = String(title || "").toLowerCase();
  if (text.includes("global") || text.includes("theme")) return "global";
  if (text.includes("stock")) return "stocks";
  if (text.includes("youtube")) return "integrations";
  return "monitoring";
}

function loadCollapsedSettingsTitles() {
  try {
    const raw = localStorage.getItem(SETTINGS_COLLAPSE_STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return new Set(Array.isArray(parsed) ? parsed : []);
  } catch {
    return new Set();
  }
}

function saveCollapsedSettingsTitles() {
  const collapsed = [...document.querySelectorAll(".settings-section.is-collapsed")]
    .map((section) => section.dataset.title)
    .filter(Boolean);
  localStorage.setItem(SETTINGS_COLLAPSE_STORAGE_KEY, JSON.stringify(collapsed));
}

function applySettingsFilters() {
  const term = (settingsSearchInput?.value || "").trim().toLowerCase();
  const group = settingsGroupFilter?.value || "all";
  document.querySelectorAll(".settings-section").forEach((section) => {
    const title = (section.dataset.title || "").toLowerCase();
    const matchTerm = !term || title.includes(term) || section.textContent.toLowerCase().includes(term);
    const matchGroup = group === "all" || (group === "modules" ? section.dataset.group !== "global" : section.dataset.group === group);
    section.classList.toggle("is-hidden", !(matchTerm && matchGroup));
  });
  syncSettingsSubmenu(group);
}

function syncSettingsSubmenu(group) {
  settingsSubmenuButtons.forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.group === group);
  });
}

function toggleSettingsSection(section, collapsed) {
  const shouldCollapse = typeof collapsed === "boolean" ? collapsed : !section.classList.contains("is-collapsed");
  section.classList.toggle("is-collapsed", shouldCollapse);
  const btn = section.querySelector(".settings-section-toggle");
  if (btn) {
    btn.textContent = shouldCollapse ? "Expand" : "Collapse";
  }
}

function initSettingsSectionsUi() {
  if (document.querySelector(".settings-section-toggle")) {
    applySettingsFilters();
    return;
  }

  const collapsedTitles = loadCollapsedSettingsTitles();
  const sections = [...document.querySelectorAll(".settings-section")];
  sections.forEach((section) => {
    const heading = section.querySelector("h4");
    if (!heading) return;

    const title = heading.textContent.trim();
    section.dataset.title = title;
    section.dataset.group = inferSettingsGroup(title);

    const body = document.createElement("div");
    body.className = "settings-section-body";
    while (heading.nextSibling) {
      body.appendChild(heading.nextSibling);
    }
    section.appendChild(body);

    const headerRow = document.createElement("div");
    headerRow.className = "settings-section-head";
    heading.parentNode.insertBefore(headerRow, heading);
    headerRow.appendChild(heading);

    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "settings-section-toggle";
    toggleBtn.textContent = "Collapse";
    toggleBtn.addEventListener("click", () => {
      toggleSettingsSection(section);
      saveCollapsedSettingsTitles();
    });
    headerRow.appendChild(toggleBtn);

    if (collapsedTitles.has(title)) {
      toggleSettingsSection(section, true);
    }
  });

  settingsSearchInput?.addEventListener("input", applySettingsFilters);
  settingsGroupFilter?.addEventListener("change", () => applySettingsFilters());
  settingsSubmenuButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!settingsGroupFilter) return;
      settingsGroupFilter.value = btn.dataset.group || "all";
      applySettingsFilters();
    });
  });
  settingsExpandAllBtn?.addEventListener("click", () => {
    sections.forEach((section) => toggleSettingsSection(section, false));
    saveCollapsedSettingsTitles();
  });
  settingsCollapseAllBtn?.addEventListener("click", () => {
    sections.forEach((section) => toggleSettingsSection(section, true));
    saveCollapsedSettingsTitles();
  });

  applySettingsFilters();
}

function sparkline(values) {
  const bars = "▁▂▃▄▅▆▇█";
  if (!values.length) {
    return "-";
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  if (max === min) {
    return bars[3].repeat(values.length);
  }
  return values
    .map((v) => {
      const idx = Math.max(0, Math.min(7, Math.round(((v - min) / (max - min)) * 7)));
      return bars[idx];
    })
    .join("");
}

function trendFromHistory(sourceName, history) {
  if (!Array.isArray(history) || history.length < 2) {
    return "-";
  }

  if (sourceName === "weather") {
    const temps = history.map((h) => h.data?.temperature_c).filter((n) => typeof n === "number");
    return temps.length > 1 ? `${sparkline(temps)} ${temps[temps.length - 1].toFixed(1)}°C` : "-";
  }

  if (sourceName.startsWith("stock_")) {
    const prices = history
      .map((h) => h.data?.quotes?.[0]?.price)
      .filter((n) => typeof n === "number");
    return prices.length > 1 ? `${sparkline(prices)} $${prices[prices.length - 1].toFixed(2)}` : "-";
  }

  if (sourceName === "crypto_price") {
    const prices = history.map((h) => h.data?.price).filter((n) => typeof n === "number");
    return prices.length > 1 ? `${sparkline(prices)} $${prices[prices.length - 1].toFixed(2)}` : "-";
  }

  if (sourceName === "air_quality") {
    const aqi = history.map((h) => h.data?.aqi_us).filter((n) => typeof n === "number");
    return aqi.length > 1 ? `${sparkline(aqi)} AQI ${aqi[aqi.length - 1].toFixed(0)}` : "-";
  }

  if (sourceName === "market_indices") {
    const avgPrices = history
      .map((h) => {
        const indices = h.data?.indices || [];
        const prices = indices.map((i) => i.price).filter((n) => typeof n === "number");
        if (!prices.length) return null;
        return prices.reduce((a, b) => a + b, 0) / prices.length;
      })
      .filter((n) => typeof n === "number");
    return avgPrices.length > 1 ? `${sparkline(avgPrices)} idx ${avgPrices[avgPrices.length - 1].toFixed(1)}` : "-";
  }

  if (sourceName === "fx_rates") {
    const eur = history.map((h) => h.data?.rates?.find((r) => r.symbol === "EUR")?.rate).filter((n) => typeof n === "number");
    return eur.length > 1 ? `${sparkline(eur)} EUR ${eur[eur.length - 1].toFixed(4)}` : "-";
  }

  if (sourceName === "mempool_fees") {
    const fast = history.map((h) => h.data?.fastest_sat_vb).filter((n) => typeof n === "number");
    return fast.length > 1 ? `${sparkline(fast)} fast ${fast[fast.length - 1].toFixed(0)}` : "-";
  }

  if (sourceName === "crypto_global") {
    const caps = history.map((h) => h.data?.total_market_cap_usd).filter((n) => typeof n === "number");
    return caps.length > 1 ? `${sparkline(caps)} mcap ${formatCompactNumber(caps[caps.length - 1])}` : "-";
  }

  return `${history.length} samples`;
}

function categoryForSource(sourceName) {
  if (sourceName.startsWith("stock_") || ["market_indices", "fx_rates", "crypto_price", "crypto_global", "mempool_fees"].includes(sourceName)) {
    return "finance";
  }
  if (["weather", "usa_severe_weather", "air_quality", "sun_times"].includes(sourceName)) {
    return "weather";
  }
  if (["travel_time"].includes(sourceName)) {
    return "aviation";
  }
  if (["iss_position", "space_weather", "nasa_events", "solar_xray", "space_launches"].includes(sourceName)) {
    return "space";
  }
  if (["hn_trends", "youtube_subscriptions", "network_dns", "public_status"].includes(sourceName)) {
    return "tech";
  }
  if (["heartbeat", "system_metrics", "time", "earthquakes"].includes(sourceName)) {
    return "ops";
  }
  return "other";
}

function extractSeries(sourceName, history) {
  const samples = Array.isArray(history) ? history : [];
  if (!samples.length) return [];

  if (sourceName === "weather") {
    return samples.map((h) => h.data?.temperature_c).filter((n) => typeof n === "number");
  }
  if (sourceName.startsWith("stock_")) {
    return samples.map((h) => h.data?.quotes?.[0]?.price).filter((n) => typeof n === "number");
  }
  if (sourceName === "crypto_price") {
    return samples.map((h) => h.data?.price).filter((n) => typeof n === "number");
  }
  if (sourceName === "market_indices") {
    return samples
      .map((h) => {
        const values = (h.data?.indices || []).map((item) => item.price).filter((n) => typeof n === "number");
        if (!values.length) return null;
        return values.reduce((a, b) => a + b, 0) / values.length;
      })
      .filter((n) => typeof n === "number");
  }
  if (sourceName === "fx_rates") {
    return samples.map((h) => h.data?.rates?.[0]?.rate).filter((n) => typeof n === "number");
  }
  if (sourceName === "air_quality") {
    return samples.map((h) => h.data?.aqi_us).filter((n) => typeof n === "number");
  }
  if (sourceName === "crypto_global") {
    return samples.map((h) => h.data?.total_market_cap_usd).filter((n) => typeof n === "number");
  }
  if (sourceName === "mempool_fees") {
    return samples.map((h) => h.data?.fastest_sat_vb).filter((n) => typeof n === "number");
  }
  if (sourceName === "heartbeat") {
    return samples.map((h) => h.data?.uptime_seconds).filter((n) => typeof n === "number");
  }
  return [];
}

function linePath(values, width = 180, height = 48, pad = 4) {
  if (values.length < 2) {
    return "";
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const step = (width - pad * 2) / Math.max(1, values.length - 1);
  return values
    .map((value, index) => {
      const x = pad + index * step;
      const y = pad + (1 - (value - min) / span) * (height - pad * 2);
      return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
}

function bars(values, count = 14) {
  return values.slice(-count).map((v, idx, list) => {
    const min = Math.min(...list);
    const max = Math.max(...list);
    const pct = max === min ? 55 : 20 + ((v - min) / (max - min)) * 80;
    return `<span style="height:${pct.toFixed(1)}%"></span>`;
  }).join("");
}

function ring(status) {
  const ratio = status === "ok" ? 1 : status === "stale" ? 0.58 : 0.22;
  const size = 34;
  const r = 13;
  const c = Math.PI * 2 * r;
  return `
    <svg class="status-ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">
      <circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ring-track"></circle>
      <circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ring-value" style="stroke-dasharray:${c};stroke-dashoffset:${(1 - ratio) * c};"></circle>
    </svg>
  `;
}

function renderMissionViz(sourceData) {
  const series = extractSeries(sourceData.source, sourceData.history);
  const latest = series.length ? series[series.length - 1] : null;
  const direction = series.length > 1 ? (series[series.length - 1] >= series[0] ? "rising" : "falling") : "steady";

  return `
    <div class="panel-viz">
      <div class="panel-viz-line">
        ${
          series.length > 1
            ? `<svg viewBox="0 0 180 48" preserveAspectRatio="none" role="img" aria-label="Trend line">
                <path d="${linePath(series)}"></path>
              </svg>`
            : `<div class="panel-viz-empty">Awaiting telemetry</div>`
        }
      </div>
      <div class="panel-viz-bars">${series.length ? bars(series) : `<span class="is-empty"></span>`}</div>
      <div class="panel-viz-meta">
        ${ring(sourceData.status)}
        <div>
          <div class="panel-viz-value mono">${latest == null ? "-" : formatCompactNumber(latest)}</div>
          <div class="panel-viz-dir">${direction}</div>
        </div>
      </div>
    </div>
  `;
}

function renderWeather(data, history) {
  return [
    row("City", data.city ?? "-"),
    row("Condition", data.condition ?? "-"),
    row("Temperature", formatTempFromC(data.temperature_c)),
    row("Humidity", `${formatNumber(data.humidity_pct, 0)}%`),
    row("Wind", formatWindFromKph(data.wind_kph)),
    row("Trend", trendFromHistory("weather", history), true),
  ].join("");
}

function renderSystemMetrics(data) {
  const zones = Array.isArray(data.zones) ? data.zones : [];
  const zoneRows = zones
    .map(
      (z) => `
      <tr>
        <td class="mono">${z.timezone}</td>
        <td class="mono">${z.time || "-"}</td>
      </tr>
    `
    )
    .join("");

  return `
    ${row("UTC", data.utc_iso ? new Date(data.utc_iso).toLocaleString() : "-", true)}
    ${row("Local TZ", data.local_timezone ?? "-", true)}
    <table class="mini-table">
      <thead>
        <tr><th>Timezone</th><th>Time</th></tr>
      </thead>
      <tbody>${zoneRows || `<tr><td colspan="2" class="empty">No zones configured</td></tr>`}</tbody>
    </table>
  `;
}

function stockSeriesFromHistory(history) {
  return (history || [])
    .map((h) => h.data?.quotes?.[0]?.price)
    .filter((n) => typeof n === "number");
}

function lineChart(values) {
  if (values.length < 2) {
    return `<div class="empty">Waiting for chart data...</div>`;
  }

  const width = 320;
  const height = 90;
  const padding = 8;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const step = (width - padding * 2) / Math.max(1, values.length - 1);
  const points = values
    .map((value, idx) => {
      const x = padding + idx * step;
      const y = padding + (1 - (value - min) / span) * (height - padding * 2);
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

  return `
    <svg class="stock-chart" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" role="img" aria-label="Stock price chart">
      <polyline points="${points}" />
    </svg>
  `;
}

function renderStock(sourceName, data, history) {
  const quote = Array.isArray(data.quotes) ? data.quotes[0] : null;
  if (!quote) {
    return `<div class="empty">No quote available</div>`;
  }

  const pct = typeof quote.change_pct === "number" ? `${quote.change_pct.toFixed(2)}%` : "-";
  const moveColor = typeof quote.change_pct === "number" ? (quote.change_pct >= 0 ? "#0f9d58" : "#b42318") : "inherit";
  const prices = stockSeriesFromHistory(history);

  return `
    ${row("Symbol", quote.symbol, true)}
    ${row("Name", quote.name || "-", true)}
    ${row("Price", `$${formatNumber(quote.price, 2)}`, true)}
    ${row("Move", `<span style="color: ${moveColor}">${pct}</span>`)}
    ${row("Open", `$${formatNumber(quote.open, 2)}`, true)}
    ${row("Day High", `$${formatNumber(quote.high, 2)}`, true)}
    ${row("Day Low", `$${formatNumber(quote.low, 2)}`, true)}
    ${row("Volume", formatCompactNumber(quote.volume), true)}
    ${row("Market Cap", formatCompactNumber(quote.market_cap), true)}
    ${row("P/E", formatNumber(quote.pe_ratio, 2), true)}
    ${row("Currency", quote.currency || "-", true)}
    ${row("Exchange", quote.exchange || "-", true)}
    ${row("Feed", quote.source || "-", true)}
    ${row("Trend", trendFromHistory(sourceName, history), true)}
    ${lineChart(prices)}
  `;
}

function renderPublicStatus(data) {
  const summary = data.summary || {};
  const services = Array.isArray(data.services) ? data.services : [];
  const rows = services
    .map((s) => {
      const state = s.ok ? "UP" : "DOWN";
      const color = s.ok ? "style=\"color: #0f9d58\"" : "style=\"color: #b42318\"";
      const latency = typeof s.latency_ms === "number" ? `${s.latency_ms.toFixed(1)} ms` : "-";
      return `
        <tr>
          <td>${s.name}</td>
          <td ${color}>${state}</td>
          <td>${latency}</td>
        </tr>
      `;
    })
    .join("");

  return `
    ${row("Up", `${summary.up ?? 0}/${summary.total ?? 0}`)}
    ${row("Down", `${summary.down ?? 0}`)}
    ${row("Avg Latency", summary.avg_latency_ms ? `${summary.avg_latency_ms} ms` : "-")}
    <table class="mini-table">
      <thead>
        <tr><th>Service</th><th>Status</th><th>Latency</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No services configured</td></tr>`}</tbody>
    </table>
  `;
}

function renderHeartbeat(data, history) {
  const uptimes = (history || [])
    .map((h) => h.data?.uptime_seconds)
    .filter((n) => typeof n === "number");
  const heartbeatTrend = uptimes.length > 1 ? sparkline(uptimes) : "-";
  return `
    ${row("State", data.heartbeat ?? "-", true)}
    ${row("Uptime", typeof data.uptime_seconds === "number" ? `${data.uptime_seconds.toFixed(1)} s` : "-", true)}
    ${row("UTC", data.utc_now ? new Date(data.utc_now).toLocaleTimeString() : "-", true)}
    ${row("Trend", heartbeatTrend, true)}
  `;
}

function renderUSASevereWeather(data) {
  const national = data.national || {};
  const worst = Array.isArray(data.worst) ? data.worst : [];

  const rows = worst
    .map(
      (entry, idx) => `
        <tr>
          <td>#${idx + 1} ${entry.city}, ${entry.state}</td>
          <td>${entry.severity_score}</td>
          <td>${entry.reason}</td>
        </tr>
      `
    )
    .join("");

  return `
    ${row("US Level", toTitle(national.severity_level || "calm"))}
    ${row("Peak Score", national.peak_score ?? 0)}
    ${row("Monitored", national.monitored_cities ?? 0)}
    <table class="mini-table">
      <thead>
        <tr><th>Worst Locations</th><th>Score</th><th>Why</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No weather data available</td></tr>`}</tbody>
    </table>
  `;
}

function renderYouTube(data) {
  const summary = data.summary || {};
  const videos = Array.isArray(data.videos) ? data.videos : [];
  const errors = Array.isArray(data.errors) ? data.errors : [];
  const rows = videos
    .map((v) => {
      const when = v.published_at ? new Date(v.published_at).toLocaleString() : "-";
      return `
        <tr>
          <td><a href="${v.url}" target="_blank" rel="noopener noreferrer">${v.title || "Untitled"}</a></td>
          <td>${v.channel_title || "-"}</td>
          <td>${when}</td>
        </tr>
      `;
    })
    .join("");

  const errorRows = errors
    .map((e) => {
      const label = e.channel_ref || e.channel_id || "unknown channel";
      const message = e.message || "unknown error";
      return `<div class="error-item"><span class="mono">${label}</span>: ${message}</div>`;
    })
    .join("");

  return `
    ${row("Channels", `${summary.fetched_channels ?? 0}/${summary.configured_channels ?? 0}`)}
    ${row("Resolved", summary.resolved_channels ?? 0)}
    ${row("Videos", summary.videos ?? 0)}
    ${row("Errors", summary.errors ?? 0)}
    <table class="mini-table">
      <thead>
        <tr><th>Recent Video</th><th>Channel</th><th>Published</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No videos yet. Add channel IDs in Settings.</td></tr>`}</tbody>
    </table>
    ${errorRows ? `<div class="error-list"><div class="error-list-title">Channel Errors</div>${errorRows}</div>` : ""}
  `;
}

function renderTravelTime(data) {
  const summary = data.summary || {};
  const origin = data.origin || {};
  const routes = Array.isArray(data.routes) ? data.routes : [];
  const rows = routes
    .map((r) => {
      const minutes = typeof r.minutes === "number" ? `${r.minutes} min` : "-";
      const dist = formatDistanceFromKm(r.distance_km);
      const color = r.status === "error" ? "style=\"color: #d72d20\"" : "";
      return `
        <tr>
          <td>${r.name || "-"}</td>
          <td ${color}>${minutes}</td>
          <td>${dist}</td>
        </tr>
      `;
    })
    .join("");

  return `
    ${row("Origin", origin.name || "-")}
    ${row("Reachable", `${summary.reachable ?? 0}/${summary.destinations ?? 0}`)}
    ${row("Fastest", summary.fastest_minutes != null ? `${summary.fastest_minutes} min` : "-")}
    <table class="mini-table">
      <thead>
        <tr><th>Destination</th><th>ETA</th><th>Distance</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No destinations configured.</td></tr>`}</tbody>
    </table>
  `;
}

function renderCryptoPrice(data, history) {
  return `
    ${row("Symbol", `${data.symbol || "-"} / ${data.currency || "-"}`, true)}
    ${row("Spot Price", typeof data.price === "number" ? `$${data.price.toFixed(2)}` : "-", true)}
    ${row("Trend", trendFromHistory("crypto_price", history), true)}
    ${row("Source", data.source || "-", true)}
  `;
}

function renderHNTrends(data) {
  const stories = Array.isArray(data.stories) ? data.stories : [];
  const rows = stories
    .map(
      (s) => `
      <tr>
        <td><a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.title || "Untitled"}</a></td>
        <td>${s.score ?? "-"}</td>
        <td>${s.comments ?? "-"}</td>
      </tr>
    `
    )
    .join("");

  return `
    ${row("Stories", data.count ?? 0)}
    <table class="mini-table">
      <thead>
        <tr><th>Top Story</th><th>Score</th><th>Comments</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No stories available</td></tr>`}</tbody>
    </table>
  `;
}

function renderEarthquakes(data) {
  const events = Array.isArray(data.events) ? data.events : [];
  const rows = events
    .map(
      (e) => `
      <tr>
        <td>${e.place || "-"}</td>
        <td>${typeof e.mag === "number" ? e.mag.toFixed(1) : "-"}</td>
        <td>${formatTimestamp(e.time_ms)}</td>
      </tr>
    `
    )
    .join("");
  return `
    ${row("Events (1h)", data.count_last_hour ?? 0)}
    ${row("Peak Magnitude", typeof data.max_magnitude === "number" ? data.max_magnitude.toFixed(1) : "-")}
    <table class="mini-table">
      <thead>
        <tr><th>Location</th><th>Mag</th><th>Time</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No recent earthquakes</td></tr>`}</tbody>
    </table>
  `;
}

function renderSunTimes(data) {
  const sunrise = data.sunrise_utc ? new Date(data.sunrise_utc).toLocaleTimeString() : "-";
  const sunset = data.sunset_utc ? new Date(data.sunset_utc).toLocaleTimeString() : "-";
  return `
    ${row("Sunrise", sunrise, true)}
    ${row("Sunset", sunset, true)}
    ${row("Day Length", typeof data.day_length_hours === "number" ? `${data.day_length_hours.toFixed(2)}h` : "-", true)}
  `;
}

function renderAirQuality(data, history) {
  return `
    ${row("US AQI", typeof data.aqi_us === "number" ? `${data.aqi_us}` : "-", true)}
    ${row("PM2.5", typeof data.pm2_5 === "number" ? `${data.pm2_5.toFixed(1)} ug/m3` : "-", true)}
    ${row("PM10", typeof data.pm10 === "number" ? `${data.pm10.toFixed(1)} ug/m3` : "-", true)}
    ${row("Ozone", typeof data.ozone === "number" ? `${data.ozone.toFixed(1)}` : "-", true)}
    ${row("Trend", trendFromHistory("air_quality", history), true)}
  `;
}

function renderISSPosition(data) {
  return `
    ${row("Latitude", typeof data.latitude === "number" ? data.latitude.toFixed(4) : "-", true)}
    ${row("Longitude", typeof data.longitude === "number" ? data.longitude.toFixed(4) : "-", true)}
    ${row("Updated", formatTimestamp(data.timestamp), true)}
  `;
}

function renderNetworkDNS(data) {
  const summary = data.summary || {};
  const checks = Array.isArray(data.checks) ? data.checks : [];
  const rows = checks
    .map(
      (c) => `
      <tr>
        <td>${c.host || "-"}</td>
        <td>${c.ok ? "OK" : "DOWN"}</td>
        <td class="mono">${(c.addresses || []).slice(0, 1).join(", ") || "-"}</td>
      </tr>
    `
    )
    .join("");

  return `
    ${row("Resolved", `${summary.ok ?? 0}/${summary.total ?? 0}`)}
    <table class="mini-table">
      <thead>
        <tr><th>Host</th><th>Status</th><th>Address</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No DNS checks configured</td></tr>`}</tbody>
    </table>
  `;
}

function renderMarketIndices(data, history) {
  const indices = Array.isArray(data.indices) ? data.indices : [];
  const rows = indices
    .map((i) => {
      const pct = typeof i.change_pct === "number" ? `${i.change_pct.toFixed(2)}%` : "-";
      const color = typeof i.change_pct === "number" ? (i.change_pct >= 0 ? "style=\"color: #0f9d58\"" : "style=\"color: #b42318\"") : "";
      return `
        <tr>
          <td class="mono">${i.symbol || "-"}</td>
          <td>${typeof i.price === "number" ? i.price.toLocaleString(undefined, { maximumFractionDigits: 2 }) : "-"}</td>
          <td ${color}>${pct}</td>
        </tr>
      `;
    })
    .join("");
  return `
    ${row("Tracked", data.count ?? 0)}
    ${row("Trend", trendFromHistory("market_indices", history), true)}
    <table class="mini-table">
      <thead>
        <tr><th>Index</th><th>Price</th><th>Move</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No index data available</td></tr>`}</tbody>
    </table>
  `;
}

function renderFxRates(data, history) {
  const rates = Array.isArray(data.rates) ? data.rates : [];
  const rows = rates
    .map((r) => {
      const value = typeof r.rate === "number" ? r.rate.toFixed(4) : "-";
      return `
        <tr>
          <td class="mono">${data.base_currency || "USD"}/${r.symbol || "-"}</td>
          <td>${value}</td>
        </tr>
      `;
    })
    .join("");
  return `
    ${row("Base", data.base_currency || "-", true)}
    ${row("Updated", data.updated_utc || "-", true)}
    ${row("Trend", trendFromHistory("fx_rates", history), true)}
    <table class="mini-table">
      <thead>
        <tr><th>Pair</th><th>Rate</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="2" class="empty">No FX rates available</td></tr>`}</tbody>
    </table>
  `;
}

function renderSpaceWeather(data) {
  const kp = typeof data.kp_index === "number" ? data.kp_index.toFixed(2) : "-";
  return `
    ${row("Planetary Kp", kp, true)}
    ${row("Level", toTitle(data.level || "unknown"), true)}
    ${row("Observed", data.observed_time || "-", true)}
    ${row("Source", data.source || "-", true)}
  `;
}

function renderQuoteOfDay(data) {
  const quote = data.quote || "No quote available.";
  return `
    <div class="quote-block">"${quote}"</div>
    ${row("Author", data.author || "-", true)}
    ${row("Source", data.source || "-", true)}
  `;
}

function renderMempoolFees(data, history) {
  return `
    ${row("Fastest", typeof data.fastest_sat_vb === "number" ? `${data.fastest_sat_vb} sat/vB` : "-", true)}
    ${row("30m", typeof data.half_hour_sat_vb === "number" ? `${data.half_hour_sat_vb} sat/vB` : "-", true)}
    ${row("1h", typeof data.hour_sat_vb === "number" ? `${data.hour_sat_vb} sat/vB` : "-", true)}
    ${row("Minimum", typeof data.minimum_sat_vb === "number" ? `${data.minimum_sat_vb} sat/vB` : "-", true)}
    ${row("Trend", trendFromHistory("mempool_fees", history), true)}
  `;
}

function renderNasaEvents(data) {
  const events = Array.isArray(data.events) ? data.events : [];
  const rows = events
    .map(
      (e) => `
      <tr>
        <td>${e.title || "-"}</td>
        <td>${e.category || "-"}</td>
        <td>${e.date ? new Date(e.date).toLocaleDateString() : "-"}</td>
      </tr>
    `
    )
    .join("");
  return `
    ${row("Open Events", data.count ?? 0)}
    <table class="mini-table">
      <thead>
        <tr><th>Event</th><th>Type</th><th>Date</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No open events</td></tr>`}</tbody>
    </table>
  `;
}

function renderSolarXray(data) {
  return `
    ${row("Flux", typeof data.flux_w_m2 === "number" ? data.flux_w_m2.toExponential(2) : "-", true)}
    ${row("Class", data.flux_class || "-", true)}
    ${row("Observed", data.observed_time || "-", true)}
    ${row("Source", data.source || "-", true)}
  `;
}

function renderCryptoGlobal(data, history) {
  return `
    ${row("Active Coins", formatCompactNumber(data.active_cryptocurrencies), true)}
    ${row("Markets", formatCompactNumber(data.markets), true)}
    ${row("Mkt Cap", data.total_market_cap_usd ? `$${formatCompactNumber(data.total_market_cap_usd)}` : "-", true)}
    ${row("24h Volume", data.total_volume_usd ? `$${formatCompactNumber(data.total_volume_usd)}` : "-", true)}
    ${row("BTC Dom", typeof data.btc_dominance_pct === "number" ? `${data.btc_dominance_pct.toFixed(2)}%` : "-", true)}
    ${row("Trend", trendFromHistory("crypto_global", history), true)}
  `;
}

function renderSpaceLaunches(data) {
  const launches = Array.isArray(data.launches) ? data.launches : [];
  const rows = launches
    .map(
      (l) => `
      <tr>
        <td>${l.name || "-"}</td>
        <td>${l.window_start ? new Date(l.window_start).toLocaleString() : "-"}</td>
        <td>${l.status || "-"}</td>
      </tr>
    `
    )
    .join("");
  return `
    ${row("Upcoming", data.count ?? 0)}
    ${row("Source", data.source || "-", true)}
    <table class="mini-table">
      <thead>
        <tr><th>Launch</th><th>Window</th><th>Status</th></tr>
      </thead>
      <tbody>${rows || `<tr><td colspan="3" class="empty">No upcoming launches</td></tr>`}</tbody>
    </table>
  `;
}

function renderFallback(data) {
  const entries = Object.entries(data || {});
  if (!entries.length) {
    return `<div class="empty">No data available</div>`;
  }
  return entries.map(([k, v]) => row(toTitle(k), typeof v === "object" ? JSON.stringify(v) : String(v))).join("");
}

function renderSourceData(sourceName, data, history) {
  if (sourceName === "weather") {
    return renderWeather(data, history);
  }
  if (sourceName === "system_metrics" || sourceName === "time") {
    return renderSystemMetrics(data);
  }
  if (sourceName.startsWith("stock_")) {
    return renderStock(sourceName, data, history);
  }
  if (sourceName === "public_status") {
    return renderPublicStatus(data);
  }
  if (sourceName === "heartbeat") {
    return renderHeartbeat(data, history);
  }
  if (sourceName === "usa_severe_weather") {
    return renderUSASevereWeather(data);
  }
  if (sourceName === "youtube_subscriptions") {
    return renderYouTube(data);
  }
  if (sourceName === "travel_time") {
    return renderTravelTime(data);
  }
  if (sourceName === "crypto_price") {
    return renderCryptoPrice(data, history);
  }
  if (sourceName === "hn_trends") {
    return renderHNTrends(data);
  }
  if (sourceName === "earthquakes") {
    return renderEarthquakes(data);
  }
  if (sourceName === "sun_times") {
    return renderSunTimes(data);
  }
  if (sourceName === "air_quality") {
    return renderAirQuality(data, history);
  }
  if (sourceName === "iss_position") {
    return renderISSPosition(data);
  }
  if (sourceName === "network_dns") {
    return renderNetworkDNS(data);
  }
  if (sourceName === "market_indices") {
    return renderMarketIndices(data, history);
  }
  if (sourceName === "fx_rates") {
    return renderFxRates(data, history);
  }
  if (sourceName === "space_weather") {
    return renderSpaceWeather(data);
  }
  if (sourceName === "quote_of_day") {
    return renderQuoteOfDay(data);
  }
  if (sourceName === "mempool_fees") {
    return renderMempoolFees(data, history);
  }
  if (sourceName === "nasa_events") {
    return renderNasaEvents(data);
  }
  if (sourceName === "solar_xray") {
    return renderSolarXray(data);
  }
  if (sourceName === "crypto_global") {
    return renderCryptoGlobal(data, history);
  }
  if (sourceName === "space_launches") {
    return renderSpaceLaunches(data);
  }
  return renderFallback(data);
}

function sourceMatchesFilter(sourceData) {
  const term = searchInput.value.trim().toLowerCase();
  const status = statusFilter.value;
  const category = categoryFilter?.value || "all";
  const matchTerm = !term || sourceData.source.toLowerCase().includes(term);
  const matchStatus = status === "all" || sourceData.status === status;
  const sourceCategory = categoryForSource(sourceData.source);
  const matchCategory = category === "all" || sourceCategory === category;
  return matchTerm && matchStatus && matchCategory;
}

function renderSummary(snapshot) {
  const counts = { ok: 0, stale: 0, error: 0 };
  snapshot.sources.forEach((s) => {
    counts[s.status] = (counts[s.status] ?? 0) + 1;
  });
  const orientation = activeOrientation();
  const signature = JSON.stringify({
    ok: counts.ok,
    stale: counts.stale,
    error: counts.error,
    source_count: snapshot.source_count,
    orientation,
    density: preferredDensityMode,
    glance: glanceMode,
  });
  if (signature === lastSummarySignature) {
    return;
  }
  lastSummarySignature = signature;

  summaryEl.innerHTML = `
    <div class="summary-pill summary-ok">OK: ${counts.ok}</div>
    <div class="summary-pill summary-stale">Stale: ${counts.stale}</div>
    <div class="summary-pill summary-error">Error: ${counts.error}</div>
    <div class="summary-pill summary-orientation">${toTitle(orientation)} Layout</div>
    <div class="summary-pill summary-density">${toTitle(preferredDensityMode)} Density</div>
    <div class="summary-pill summary-density">${glanceMode ? "Glance On" : "Glance Off"}</div>
    <div class="summary-meta">Sources: ${snapshot.source_count} | Generated: ${new Date(snapshot.generated_at).toLocaleTimeString()}</div>
  `;
}

function render(snapshot) {
  snapshotCache = snapshot;
  currentUnitSystem = (snapshot.unit_system || "metric").toLowerCase();
  const palette = normalizeBrandPalette(snapshot.brand_palette || settingsCache?.brand_palette || loadBrandPalette());
  const visualSignature = JSON.stringify({ palette });
  if (visualSignature !== lastVisualSignature) {
    applyVisualSettings({ palette });
    lastVisualSignature = visualSignature;
  }
  renderSummary(snapshot);
  const visibleSources = sortSourcesByOrder(snapshot.sources.filter(sourceMatchesFilter));
  applyGlanceColumns(visibleSources.length);
  const visibleSet = new Set(visibleSources.map((s) => s.source));
  const now = Date.now();
  const shouldRefreshRelativeTimes = now - lastTimestampRefreshAt >= 5000;

  // Remove cards that should no longer be shown.
  cardsContainer.querySelectorAll(".card").forEach((card) => {
    const source = card.dataset.source;
    if (!visibleSet.has(source)) {
      card.remove();
    }
  });

  // Create or update cards without re-creating the whole container.
  visibleSources.forEach((sourceData, index) => {
    let card = cardsContainer.querySelector(`.card[data-source="${sourceData.source}"]`);
    if (!card) {
      card = cardTemplate.content.firstElementChild.cloneNode(true);
      card.dataset.source = sourceData.source;
    }
    card.draggable = arrangeMode;
    card.classList.remove("card-half");

    const sourceEl = card.querySelector(".source");
    const statusEl = card.querySelector(".status-badge");
    const payloadEl = card.querySelector(".payload");
    const timestampEl = card.querySelector(".timestamp");
    const samplesEl = card.querySelector(".samples");
    const errorEl = card.querySelector(".error");
    const sourceRefreshBtn = card.querySelector(".source-refresh");
    const sourceToggleBtn = card.querySelector(".source-toggle");

    const category = categoryForSource(sourceData.source);
    card.dataset.category = category;
    card.classList.remove("category-finance", "category-weather", "category-aviation", "category-space", "category-tech", "category-ops", "category-other");
    card.classList.add(`category-${category}`);

    const quoteSymbol = sourceData.data?.quotes?.[0]?.symbol;
    const sourceTitleHtml = `
      <span>${sourceData.source.startsWith("stock_") && quoteSymbol
        ? `${toTitle(sourceData.source)} (${quoteSymbol})`
        : toTitle(sourceData.source)}</span>
      <small>${category.toUpperCase()}</small>
    `;
    if (sourceEl.innerHTML !== sourceTitleHtml) {
      sourceEl.innerHTML = sourceTitleHtml;
    }

    const sourceSignature = JSON.stringify({
      status: sourceData.status,
      error: sourceData.error || "",
      source_paused: Boolean(sourceData.source_paused),
      data: sourceData.data,
      history: sourceData.history || [],
    });

    if (card.dataset.renderSignature !== sourceSignature) {
      statusEl.textContent = sourceData.status;
      statusEl.className = "status-badge";
      statusEl.classList.add(`status-${sourceData.status}`);
      const nextPayload = `<div class="payload-grid">${renderSourceData(sourceData.source, sourceData.data, sourceData.history)}</div>`;
      payloadEl.innerHTML = nextPayload;
      samplesEl.textContent = `History samples: ${(sourceData.history || []).length}`;
      errorEl.textContent = sourceData.error ? `Error: ${sourceData.error}` : "";
      sourceToggleBtn.textContent = sourceData.source_paused ? "Resume Source" : "Pause Source";
      card.dataset.renderSignature = sourceSignature;
    }

    sourceRefreshBtn.dataset.source = sourceData.source;
    sourceToggleBtn.dataset.source = sourceData.source;

    if (shouldRefreshRelativeTimes || !timestampEl.textContent) {
      timestampEl.textContent = sourceData.fetched_at
        ? `Updated ${relativeTime(sourceData.fetched_at)} (${new Date(sourceData.fetched_at).toLocaleTimeString()})`
        : "Updated: not available";
    }

    // Keep order stable without forcing a full reflow every tick.
    const currentAtIndex = cardsContainer.children[index];
    if (currentAtIndex !== card) {
      cardsContainer.insertBefore(card, currentAtIndex || null);
    }
  });

  paused = snapshot.paused;
  togglePauseBtn.textContent = paused ? "Resume" : "Pause";
  refreshNowBtn.disabled = paused;
  setRateBtn.disabled = paused;
  rateInput.disabled = paused;
  if (paused) {
    stopAutoRefresh();
  } else {
    startAutoRefresh();
  }
  rateInput.value = snapshot.global_refresh_rate;
  if (shouldRefreshRelativeTimes) {
    lastTimestampRefreshAt = now;
  }
}

function loadCardOrder() {
  try {
    const raw = localStorage.getItem(CARD_ORDER_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveCardOrder() {
  localStorage.setItem(CARD_ORDER_STORAGE_KEY, JSON.stringify(cardOrder));
}

function ensureCardOrderContains(sources) {
  const existing = new Set(cardOrder);
  sources.forEach((s) => {
    if (!existing.has(s.source)) {
      cardOrder.push(s.source);
      existing.add(s.source);
    }
  });
  // Drop entries for modules no longer present.
  const sourceSet = new Set(sources.map((s) => s.source));
  cardOrder = cardOrder.filter((s) => sourceSet.has(s));
  saveCardOrder();
}

function sortSourcesByOrder(sources) {
  ensureCardOrderContains(sources);
  const rank = new Map(cardOrder.map((source, idx) => [source, idx]));
  return [...sources].sort((a, b) => (rank.get(a.source) ?? 9999) - (rank.get(b.source) ?? 9999));
}

function reorderCardOrder(draggedSource, targetSource) {
  if (!draggedSource || !targetSource || draggedSource === targetSource) {
    return;
  }
  const from = cardOrder.indexOf(draggedSource);
  const to = cardOrder.indexOf(targetSource);
  if (from < 0 || to < 0) return;
  cardOrder.splice(from, 1);
  cardOrder.splice(to, 0, draggedSource);
  saveCardOrder();
}

function toggleArrangeMode() {
  arrangeMode = !arrangeMode;
  document.body.classList.toggle("arrange-mode", arrangeMode);
  toggleArrangeBtn.textContent = arrangeMode ? "Done" : "Arrange";
  if (snapshotCache) render(snapshotCache);
}

async function loadSnapshot() {
  try {
    const response = await fetch("/api/snapshot");
    const snapshot = await response.json();
    render(snapshot);
  } catch (err) {
    console.error("Failed to load snapshot", err);
  }
}

async function togglePause() {
  const endpoint = paused ? "/api/resume" : "/api/pause";
  await fetch(endpoint, { method: "POST" });
  if (!paused) {
    stopAutoRefresh();
  }
  await loadSnapshot();
}

async function refreshNow(source = null) {
  if (paused) return;
  await fetch("/api/refresh-now", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source }),
  });
  await loadSnapshot();
}

async function toggleSource(source) {
  if (paused) return;
  const current = snapshotCache?.sources?.find((s) => s.source === source);
  if (!current) {
    return;
  }
  const endpoint = current.source_paused ? `/api/source/${source}/resume` : `/api/source/${source}/pause`;
  await fetch(endpoint, { method: "POST" });
  await loadSnapshot();
}

async function updateRefreshRate() {
  if (paused) return;
  const value = Number(rateInput.value);
  if (!value || value <= 0) {
    return;
  }

  await fetch("/api/refresh-rate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ global_refresh_rate: value }),
  });
  await loadSnapshot();
}

function exportSnapshot() {
  if (!snapshotCache) {
    return;
  }
  const blob = new Blob([JSON.stringify(snapshotCache, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const stamp = new Date().toISOString().replaceAll(":", "-");
  a.href = url;
  a.download = `snapshot-${stamp}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function startAutoRefresh() {
  if (fetchInterval) return;
  fetchInterval = setInterval(loadSnapshot, 1000);
}

function stopAutoRefresh() {
  if (!fetchInterval) return;
  clearInterval(fetchInterval);
  fetchInterval = null;
}

function setSettingsStatus(message, isError = false) {
  settingsStatus.textContent = message;
  settingsStatus.style.color = isError ? "#b42318" : "#64748b";
}

function toCsv(values) {
  return (values || []).join(", ");
}

function parseCsv(text) {
  return text
    .split(",")
    .map((v) => v.trim())
    .filter(Boolean);
}

function serviceLinesToText(services) {
  return (services || []).map((s) => `${s.name || ""}|${s.url || ""}|${s.expect_status ?? 200}`).join("\n");
}

function parseServiceLines(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [name, url, expect] = line.split("|").map((v) => (v || "").trim());
      return {
        name: name || url || "Service",
        url,
        expect_status: expect ? Number(expect) : 200,
      };
    })
    .filter((s) => s.url);
}

function cityLinesToText(cities) {
  return (cities || [])
    .map((c) => `${c.city || ""},${c.state || ""},${c.latitude ?? ""},${c.longitude ?? ""}`)
    .join("\n");
}

function parseCityLines(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [city, state, lat, lon] = line.split(",").map((v) => (v || "").trim());
      return {
        city,
        state,
        latitude: Number(lat),
        longitude: Number(lon),
      };
    })
    .filter((c) => c.city && Number.isFinite(c.latitude) && Number.isFinite(c.longitude));
}

function linesToList(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function locationLineToText(loc) {
  if (!loc) return "";
  if (typeof loc.address === "string" && loc.address.trim()) {
    return loc.address.trim();
  }
  if (typeof loc.name === "string" && loc.name.trim()) {
    return loc.name.trim();
  }
  return `${loc.name || ""},${loc.latitude ?? ""},${loc.longitude ?? ""}`;
}

function parseLocationLine(line) {
  const raw = (line || "").trim();
  if (!raw) {
    return { name: "Location", address: "" };
  }

  // Backward-compatible coordinate parsing: name,lat,lon
  const parts = raw.split(",").map((v) => (v || "").trim());
  if (parts.length >= 3) {
    const lat = Number(parts[parts.length - 2]);
    const lon = Number(parts[parts.length - 1]);
    if (Number.isFinite(lat) && Number.isFinite(lon)) {
      return {
        name: parts.slice(0, -2).join(", ") || "Location",
        latitude: lat,
        longitude: lon,
      };
    }
  }

  return {
    name: raw,
    address: raw,
  };
}

function parseDestinationLines(text) {
  return (text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map(parseLocationLine)
    .filter((loc) => (typeof loc.address === "string" && loc.address.trim()) || (Number.isFinite(loc.latitude) && Number.isFinite(loc.longitude)));
}

function populateSettingsForm(cfg) {
  const providers = cfg.providers || {};
  const palette = normalizeBrandPalette(cfg.brand_palette || loadBrandPalette());
  const weather = providers.weather || {};
  const system = providers.system_metrics || {};
  const stock1 = providers.stock_1 || {};
  const stock2 = providers.stock_2 || {};
  const stock3 = providers.stock_3 || {};
  const legacyMarket = providers.mock_market || {};
  const status = providers.public_status || {};
  const heartbeat = providers.heartbeat || {};
  const severe = providers.usa_severe_weather || {};
  const youtube = providers.youtube_subscriptions || {};
  const travel = providers.travel_time || {};
  const crypto = providers.crypto_price || {};
  const hn = providers.hn_trends || {};
  const earth = providers.earthquakes || {};
  const sun = providers.sun_times || {};
  const air = providers.air_quality || {};
  const iss = providers.iss_position || {};
  const dns = providers.network_dns || {};
  const indices = providers.market_indices || {};
  const fx = providers.fx_rates || {};
  const space = providers.space_weather || {};
  const quote = providers.quote_of_day || {};
  const mempool = providers.mempool_fees || {};
  const nasa = providers.nasa_events || {};
  const xray = providers.solar_xray || {};
  const cryptoGlobal = providers.crypto_global || {};
  const launches = providers.space_launches || {};

  cfgGlobalRefreshRate.value = cfg.global_refresh_rate ?? 1.0;
  cfgHistorySize.value = cfg.history_size ?? 20;
  cfgUnitSystem.value = (cfg.unit_system || "metric").toLowerCase() === "imperial" ? "imperial" : "metric";
  if (cfgBrandPalette) cfgBrandPalette.value = palette;

  cfgWeatherEnabled.checked = Boolean(weather.enabled);
  cfgWeatherCity.value = weather.city ?? "";
  cfgWeatherLatitude.value = weather.latitude ?? "";
  cfgWeatherLongitude.value = weather.longitude ?? "";
  cfgWeatherPoll.value = weather.poll_interval ?? 10;
  cfgWeatherTtl.value = weather.cache_ttl ?? 3;

  cfgSystemEnabled.checked = Boolean(system.enabled);
  cfgSystemTimezones.value = toCsv(system.timezones || []);
  cfgSystemPoll.value = system.poll_interval ?? 1;
  cfgSystemTtl.value = system.cache_ttl ?? 1;

  cfgStock1Enabled.checked = Boolean(stock1.enabled ?? legacyMarket.enabled ?? true);
  cfgStock1Symbol.value = stock1.symbol ?? legacyMarket.symbols?.[0] ?? "AAPL";
  cfgStock1Poll.value = stock1.poll_interval ?? legacyMarket.poll_interval ?? 2;
  cfgStock1Ttl.value = stock1.cache_ttl ?? legacyMarket.cache_ttl ?? 2;
  cfgStock1Timeout.value = stock1.timeout_s ?? 6;

  cfgStock2Enabled.checked = Boolean(stock2.enabled ?? legacyMarket.enabled ?? true);
  cfgStock2Symbol.value = stock2.symbol ?? legacyMarket.symbols?.[1] ?? "MSFT";
  cfgStock2Poll.value = stock2.poll_interval ?? legacyMarket.poll_interval ?? 2;
  cfgStock2Ttl.value = stock2.cache_ttl ?? legacyMarket.cache_ttl ?? 2;
  cfgStock2Timeout.value = stock2.timeout_s ?? 6;

  cfgStock3Enabled.checked = Boolean(stock3.enabled ?? legacyMarket.enabled ?? true);
  cfgStock3Symbol.value = stock3.symbol ?? legacyMarket.symbols?.[2] ?? "NVDA";
  cfgStock3Poll.value = stock3.poll_interval ?? legacyMarket.poll_interval ?? 2;
  cfgStock3Ttl.value = stock3.cache_ttl ?? legacyMarket.cache_ttl ?? 2;
  cfgStock3Timeout.value = stock3.timeout_s ?? 6;

  cfgStatusEnabled.checked = Boolean(status.enabled);
  cfgStatusPoll.value = status.poll_interval ?? 8;
  cfgStatusTtl.value = status.cache_ttl ?? 4;
  cfgStatusTimeout.value = status.timeout_s ?? 5;
  cfgStatusServices.value = serviceLinesToText(status.services || []);

  cfgHeartbeatEnabled.checked = Boolean(heartbeat.enabled);
  cfgHeartbeatPoll.value = heartbeat.poll_interval ?? 1;
  cfgHeartbeatTtl.value = heartbeat.cache_ttl ?? 1;

  cfgSevereEnabled.checked = Boolean(severe.enabled);
  cfgSeverePoll.value = severe.poll_interval ?? 20;
  cfgSevereTtl.value = severe.cache_ttl ?? 8;
  cfgSevereTimeout.value = severe.timeout_s ?? 8;
  cfgSevereTopn.value = severe.top_n ?? 8;
  cfgSevereCities.value = cityLinesToText(severe.cities || []);

  cfgYoutubeEnabled.checked = Boolean(youtube.enabled);
  cfgYoutubePoll.value = youtube.poll_interval ?? 60;
  cfgYoutubeTtl.value = youtube.cache_ttl ?? 20;
  cfgYoutubeTimeout.value = youtube.timeout_s ?? 8;
  cfgYoutubeMax.value = youtube.max_videos ?? 15;
  cfgYoutubeChannels.value = (youtube.channel_ids || []).join("\n");

  cfgTravelEnabled.checked = Boolean(travel.enabled);
  cfgTravelPoll.value = travel.poll_interval ?? 45;
  cfgTravelTtl.value = travel.cache_ttl ?? 20;
  cfgTravelTimeout.value = travel.timeout_s ?? 8;
  cfgTravelOrigin.value = locationLineToText(travel.origin || { name: "Home", latitude: "", longitude: "" });
  cfgTravelDests.value = (travel.destinations || []).map(locationLineToText).join("\n");

  cfgCryptoEnabled.checked = Boolean(crypto.enabled);
  cfgCryptoSymbol.value = crypto.symbol ?? "BTC-USD";
  cfgCryptoPoll.value = crypto.poll_interval ?? 8;
  cfgCryptoTtl.value = crypto.cache_ttl ?? 4;
  cfgCryptoTimeout.value = crypto.timeout_s ?? 6;

  cfgHnEnabled.checked = Boolean(hn.enabled);
  cfgHnTopn.value = hn.top_n ?? 8;
  cfgHnPoll.value = hn.poll_interval ?? 45;
  cfgHnTtl.value = hn.cache_ttl ?? 20;
  cfgHnTimeout.value = hn.timeout_s ?? 8;

  cfgEarthEnabled.checked = Boolean(earth.enabled);
  cfgEarthMax.value = earth.max_events ?? 6;
  cfgEarthPoll.value = earth.poll_interval ?? 30;
  cfgEarthTtl.value = earth.cache_ttl ?? 12;
  cfgEarthTimeout.value = earth.timeout_s ?? 7;

  cfgSunEnabled.checked = Boolean(sun.enabled);
  cfgSunLatitude.value = sun.latitude ?? 47.6588;
  cfgSunLongitude.value = sun.longitude ?? -117.426;
  cfgSunPoll.value = sun.poll_interval ?? 90;
  cfgSunTtl.value = sun.cache_ttl ?? 60;
  cfgSunTimeout.value = sun.timeout_s ?? 6;

  cfgAirEnabled.checked = Boolean(air.enabled);
  cfgAirLatitude.value = air.latitude ?? 47.6588;
  cfgAirLongitude.value = air.longitude ?? -117.426;
  cfgAirPoll.value = air.poll_interval ?? 25;
  cfgAirTtl.value = air.cache_ttl ?? 10;
  cfgAirTimeout.value = air.timeout_s ?? 8;

  cfgIssEnabled.checked = Boolean(iss.enabled);
  cfgIssPoll.value = iss.poll_interval ?? 5;
  cfgIssTtl.value = iss.cache_ttl ?? 3;
  cfgIssTimeout.value = iss.timeout_s ?? 5;

  cfgDnsEnabled.checked = Boolean(dns.enabled);
  cfgDnsHosts.value = toCsv(dns.hosts || []);
  cfgDnsPoll.value = dns.poll_interval ?? 35;
  cfgDnsTtl.value = dns.cache_ttl ?? 15;

  cfgIndicesEnabled.checked = Boolean(indices.enabled);
  cfgIndicesSymbols.value = toCsv(indices.symbols || []);
  cfgIndicesPoll.value = indices.poll_interval ?? 12;
  cfgIndicesTtl.value = indices.cache_ttl ?? 6;
  cfgIndicesTimeout.value = indices.timeout_s ?? 6;

  cfgFxEnabled.checked = Boolean(fx.enabled);
  cfgFxBase.value = fx.base_currency ?? "USD";
  cfgFxSymbols.value = toCsv(fx.symbols || []);
  cfgFxPoll.value = fx.poll_interval ?? 30;
  cfgFxTtl.value = fx.cache_ttl ?? 15;
  cfgFxTimeout.value = fx.timeout_s ?? 6;

  cfgSpaceEnabled.checked = Boolean(space.enabled);
  cfgSpacePoll.value = space.poll_interval ?? 20;
  cfgSpaceTtl.value = space.cache_ttl ?? 10;
  cfgSpaceTimeout.value = space.timeout_s ?? 6;

  cfgQuoteEnabled.checked = Boolean(quote.enabled);
  cfgQuotePoll.value = quote.poll_interval ?? 120;
  cfgQuoteTtl.value = quote.cache_ttl ?? 60;
  cfgQuoteTimeout.value = quote.timeout_s ?? 6;

  cfgMempoolEnabled.checked = Boolean(mempool.enabled);
  cfgMempoolPoll.value = mempool.poll_interval ?? 15;
  cfgMempoolTtl.value = mempool.cache_ttl ?? 8;
  cfgMempoolTimeout.value = mempool.timeout_s ?? 6;

  cfgNasaEnabled.checked = Boolean(nasa.enabled);
  cfgNasaLimit.value = nasa.limit ?? 8;
  cfgNasaPoll.value = nasa.poll_interval ?? 40;
  cfgNasaTtl.value = nasa.cache_ttl ?? 20;
  cfgNasaTimeout.value = nasa.timeout_s ?? 8;

  cfgXrayEnabled.checked = Boolean(xray.enabled);
  cfgXrayPoll.value = xray.poll_interval ?? 25;
  cfgXrayTtl.value = xray.cache_ttl ?? 10;
  cfgXrayTimeout.value = xray.timeout_s ?? 8;

  cfgCryptoGlobalEnabled.checked = Boolean(cryptoGlobal.enabled);
  cfgCryptoGlobalPoll.value = cryptoGlobal.poll_interval ?? 20;
  cfgCryptoGlobalTtl.value = cryptoGlobal.cache_ttl ?? 10;
  cfgCryptoGlobalTimeout.value = cryptoGlobal.timeout_s ?? 8;

  cfgLaunchesEnabled.checked = Boolean(launches.enabled);
  cfgLaunchesLimit.value = launches.limit ?? 6;
  cfgLaunchesPoll.value = launches.poll_interval ?? 60;
  cfgLaunchesTtl.value = launches.cache_ttl ?? 30;
  cfgLaunchesTimeout.value = launches.timeout_s ?? 8;
}

function buildConfigFromForm() {
  const base = structuredClone(settingsCache || {});
  base.global_refresh_rate = Number(cfgGlobalRefreshRate.value || 1);
  base.history_size = Math.max(1, Number(cfgHistorySize.value || 20));
  base.unit_system = cfgUnitSystem.value === "imperial" ? "imperial" : "metric";
  base.brand_palette = normalizeBrandPalette(cfgBrandPalette?.value || currentBrandPalette);
  base.appearance_mode = "light";
  base.theme = {};
  base.providers = base.providers || {};

  base.providers.weather = {
    ...(base.providers.weather || {}),
    enabled: cfgWeatherEnabled.checked,
    city: cfgWeatherCity.value.trim(),
    latitude: Number(cfgWeatherLatitude.value || 0),
    longitude: Number(cfgWeatherLongitude.value || 0),
    poll_interval: Number(cfgWeatherPoll.value || 10),
    cache_ttl: Number(cfgWeatherTtl.value || 3),
  };

  base.providers.system_metrics = {
    ...(base.providers.system_metrics || {}),
    enabled: cfgSystemEnabled.checked,
    timezones: parseCsv(cfgSystemTimezones.value),
    poll_interval: Number(cfgSystemPoll.value || 1),
    cache_ttl: Number(cfgSystemTtl.value || 1),
  };

  base.providers.stock_1 = {
    ...(base.providers.stock_1 || {}),
    enabled: cfgStock1Enabled.checked,
    symbol: (cfgStock1Symbol.value || "AAPL").trim().toUpperCase(),
    poll_interval: Number(cfgStock1Poll.value || 2),
    cache_ttl: Number(cfgStock1Ttl.value || 2),
    timeout_s: Math.max(1, Number(cfgStock1Timeout.value || 6)),
  };

  base.providers.stock_2 = {
    ...(base.providers.stock_2 || {}),
    enabled: cfgStock2Enabled.checked,
    symbol: (cfgStock2Symbol.value || "MSFT").trim().toUpperCase(),
    poll_interval: Number(cfgStock2Poll.value || 2),
    cache_ttl: Number(cfgStock2Ttl.value || 2),
    timeout_s: Math.max(1, Number(cfgStock2Timeout.value || 6)),
  };

  base.providers.stock_3 = {
    ...(base.providers.stock_3 || {}),
    enabled: cfgStock3Enabled.checked,
    symbol: (cfgStock3Symbol.value || "NVDA").trim().toUpperCase(),
    poll_interval: Number(cfgStock3Poll.value || 2),
    cache_ttl: Number(cfgStock3Ttl.value || 2),
    timeout_s: Math.max(1, Number(cfgStock3Timeout.value || 6)),
  };

  base.providers.public_status = {
    ...(base.providers.public_status || {}),
    enabled: cfgStatusEnabled.checked,
    poll_interval: Number(cfgStatusPoll.value || 8),
    cache_ttl: Number(cfgStatusTtl.value || 4),
    timeout_s: Number(cfgStatusTimeout.value || 5),
    services: parseServiceLines(cfgStatusServices.value),
  };

  base.providers.heartbeat = {
    ...(base.providers.heartbeat || {}),
    enabled: cfgHeartbeatEnabled.checked,
    poll_interval: Number(cfgHeartbeatPoll.value || 1),
    cache_ttl: Number(cfgHeartbeatTtl.value || 1),
  };

  base.providers.usa_severe_weather = {
    ...(base.providers.usa_severe_weather || {}),
    enabled: cfgSevereEnabled.checked,
    poll_interval: Number(cfgSeverePoll.value || 20),
    cache_ttl: Number(cfgSevereTtl.value || 8),
    timeout_s: Number(cfgSevereTimeout.value || 8),
    top_n: Math.max(1, Number(cfgSevereTopn.value || 8)),
    cities: parseCityLines(cfgSevereCities.value),
  };

  base.providers.youtube_subscriptions = {
    ...(base.providers.youtube_subscriptions || {}),
    enabled: cfgYoutubeEnabled.checked,
    poll_interval: Math.max(1, Number(cfgYoutubePoll.value || 60)),
    cache_ttl: Math.max(1, Number(cfgYoutubeTtl.value || 20)),
    timeout_s: Math.max(1, Number(cfgYoutubeTimeout.value || 8)),
    max_videos: Math.max(1, Number(cfgYoutubeMax.value || 15)),
    channel_ids: linesToList(cfgYoutubeChannels.value),
  };

  const parsedOrigin = parseLocationLine(cfgTravelOrigin.value);
  base.providers.travel_time = {
    ...(base.providers.travel_time || {}),
    enabled: cfgTravelEnabled.checked,
    poll_interval: Math.max(1, Number(cfgTravelPoll.value || 45)),
    cache_ttl: Math.max(1, Number(cfgTravelTtl.value || 20)),
    timeout_s: Math.max(1, Number(cfgTravelTimeout.value || 8)),
    origin: Number.isFinite(parsedOrigin.latitude) && Number.isFinite(parsedOrigin.longitude)
      ? {
          name: parsedOrigin.name,
          latitude: parsedOrigin.latitude,
          longitude: parsedOrigin.longitude,
        }
      : {
          name: parsedOrigin.name,
          address: parsedOrigin.address || cfgTravelOrigin.value.trim(),
        },
    destinations: parseDestinationLines(cfgTravelDests.value),
  };

  base.providers.crypto_price = {
    ...(base.providers.crypto_price || {}),
    enabled: cfgCryptoEnabled.checked,
    symbol: (cfgCryptoSymbol.value || "BTC-USD").trim().toUpperCase(),
    poll_interval: Math.max(1, Number(cfgCryptoPoll.value || 8)),
    cache_ttl: Math.max(1, Number(cfgCryptoTtl.value || 4)),
    timeout_s: Math.max(1, Number(cfgCryptoTimeout.value || 6)),
  };

  base.providers.hn_trends = {
    ...(base.providers.hn_trends || {}),
    enabled: cfgHnEnabled.checked,
    top_n: Math.max(1, Number(cfgHnTopn.value || 8)),
    poll_interval: Math.max(1, Number(cfgHnPoll.value || 45)),
    cache_ttl: Math.max(1, Number(cfgHnTtl.value || 20)),
    timeout_s: Math.max(1, Number(cfgHnTimeout.value || 8)),
  };

  base.providers.earthquakes = {
    ...(base.providers.earthquakes || {}),
    enabled: cfgEarthEnabled.checked,
    max_events: Math.max(1, Number(cfgEarthMax.value || 6)),
    poll_interval: Math.max(1, Number(cfgEarthPoll.value || 30)),
    cache_ttl: Math.max(1, Number(cfgEarthTtl.value || 12)),
    timeout_s: Math.max(1, Number(cfgEarthTimeout.value || 7)),
  };

  base.providers.sun_times = {
    ...(base.providers.sun_times || {}),
    enabled: cfgSunEnabled.checked,
    latitude: Number(cfgSunLatitude.value || 47.6588),
    longitude: Number(cfgSunLongitude.value || -117.426),
    poll_interval: Math.max(1, Number(cfgSunPoll.value || 90)),
    cache_ttl: Math.max(1, Number(cfgSunTtl.value || 60)),
    timeout_s: Math.max(1, Number(cfgSunTimeout.value || 6)),
  };

  base.providers.air_quality = {
    ...(base.providers.air_quality || {}),
    enabled: cfgAirEnabled.checked,
    latitude: Number(cfgAirLatitude.value || 47.6588),
    longitude: Number(cfgAirLongitude.value || -117.426),
    poll_interval: Math.max(1, Number(cfgAirPoll.value || 25)),
    cache_ttl: Math.max(1, Number(cfgAirTtl.value || 10)),
    timeout_s: Math.max(1, Number(cfgAirTimeout.value || 8)),
  };

  base.providers.iss_position = {
    ...(base.providers.iss_position || {}),
    enabled: cfgIssEnabled.checked,
    poll_interval: Math.max(1, Number(cfgIssPoll.value || 5)),
    cache_ttl: Math.max(1, Number(cfgIssTtl.value || 3)),
    timeout_s: Math.max(1, Number(cfgIssTimeout.value || 5)),
  };

  base.providers.network_dns = {
    ...(base.providers.network_dns || {}),
    enabled: cfgDnsEnabled.checked,
    hosts: parseCsv(cfgDnsHosts.value),
    poll_interval: Math.max(1, Number(cfgDnsPoll.value || 35)),
    cache_ttl: Math.max(1, Number(cfgDnsTtl.value || 15)),
  };

  base.providers.market_indices = {
    ...(base.providers.market_indices || {}),
    enabled: cfgIndicesEnabled.checked,
    symbols: parseCsv(cfgIndicesSymbols.value),
    poll_interval: Math.max(1, Number(cfgIndicesPoll.value || 12)),
    cache_ttl: Math.max(1, Number(cfgIndicesTtl.value || 6)),
    timeout_s: Math.max(1, Number(cfgIndicesTimeout.value || 6)),
  };

  base.providers.fx_rates = {
    ...(base.providers.fx_rates || {}),
    enabled: cfgFxEnabled.checked,
    base_currency: (cfgFxBase.value || "USD").trim().toUpperCase(),
    symbols: parseCsv(cfgFxSymbols.value),
    poll_interval: Math.max(1, Number(cfgFxPoll.value || 30)),
    cache_ttl: Math.max(1, Number(cfgFxTtl.value || 15)),
    timeout_s: Math.max(1, Number(cfgFxTimeout.value || 6)),
  };

  base.providers.space_weather = {
    ...(base.providers.space_weather || {}),
    enabled: cfgSpaceEnabled.checked,
    poll_interval: Math.max(1, Number(cfgSpacePoll.value || 20)),
    cache_ttl: Math.max(1, Number(cfgSpaceTtl.value || 10)),
    timeout_s: Math.max(1, Number(cfgSpaceTimeout.value || 6)),
  };

  base.providers.quote_of_day = {
    ...(base.providers.quote_of_day || {}),
    enabled: cfgQuoteEnabled.checked,
    poll_interval: Math.max(1, Number(cfgQuotePoll.value || 120)),
    cache_ttl: Math.max(1, Number(cfgQuoteTtl.value || 60)),
    timeout_s: Math.max(1, Number(cfgQuoteTimeout.value || 6)),
  };

  base.providers.mempool_fees = {
    ...(base.providers.mempool_fees || {}),
    enabled: cfgMempoolEnabled.checked,
    poll_interval: Math.max(1, Number(cfgMempoolPoll.value || 15)),
    cache_ttl: Math.max(1, Number(cfgMempoolTtl.value || 8)),
    timeout_s: Math.max(1, Number(cfgMempoolTimeout.value || 6)),
  };

  base.providers.nasa_events = {
    ...(base.providers.nasa_events || {}),
    enabled: cfgNasaEnabled.checked,
    limit: Math.max(1, Number(cfgNasaLimit.value || 8)),
    poll_interval: Math.max(1, Number(cfgNasaPoll.value || 40)),
    cache_ttl: Math.max(1, Number(cfgNasaTtl.value || 20)),
    timeout_s: Math.max(1, Number(cfgNasaTimeout.value || 8)),
  };

  base.providers.solar_xray = {
    ...(base.providers.solar_xray || {}),
    enabled: cfgXrayEnabled.checked,
    poll_interval: Math.max(1, Number(cfgXrayPoll.value || 25)),
    cache_ttl: Math.max(1, Number(cfgXrayTtl.value || 10)),
    timeout_s: Math.max(1, Number(cfgXrayTimeout.value || 8)),
  };

  base.providers.crypto_global = {
    ...(base.providers.crypto_global || {}),
    enabled: cfgCryptoGlobalEnabled.checked,
    poll_interval: Math.max(1, Number(cfgCryptoGlobalPoll.value || 20)),
    cache_ttl: Math.max(1, Number(cfgCryptoGlobalTtl.value || 10)),
    timeout_s: Math.max(1, Number(cfgCryptoGlobalTimeout.value || 8)),
  };

  base.providers.space_launches = {
    ...(base.providers.space_launches || {}),
    enabled: cfgLaunchesEnabled.checked,
    limit: Math.max(1, Number(cfgLaunchesLimit.value || 6)),
    poll_interval: Math.max(1, Number(cfgLaunchesPoll.value || 60)),
    cache_ttl: Math.max(1, Number(cfgLaunchesTtl.value || 30)),
    timeout_s: Math.max(1, Number(cfgLaunchesTimeout.value || 8)),
  };

  delete base.providers.flight_board;
  delete base.providers.airport_delay;
  delete base.providers.mock_market;

  return base;
}

async function loadSettingsIntoForm() {
  setSettingsStatus("Loading settings...");
  const response = await fetch("/api/settings");
  const payload = await response.json();
  settingsCache = payload.config;
  populateSettingsForm(settingsCache);
  applySettingsFilters();
  setSettingsStatus("Settings loaded.");
}

async function openSettingsModal() {
  initSettingsSectionsUi();
  settingsModal.classList.remove("hidden");
  await loadSettingsIntoForm();
}

function closeSettingsModal() {
  settingsModal.classList.add("hidden");
}

async function saveSettings() {
  const parsed = buildConfigFromForm();

  setSettingsStatus("Saving and applying...");
  const response = await fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(parsed),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: "Failed to save settings" }));
    setSettingsStatus(`Save failed: ${err.detail || "unknown error"}`, true);
    return;
  }

  setSettingsStatus("Saved and applied.");
  settingsCache = parsed;
  saveBrandPalette(parsed.brand_palette || DEFAULT_BRAND_PALETTE);
  applyVisualSettings({ palette: parsed.brand_palette || DEFAULT_BRAND_PALETTE });
  await loadSnapshot();
}

async function persistBrandPalette(palette) {
  try {
    const settingsResponse = await fetch("/api/settings");
    const payload = await settingsResponse.json();
    const cfg = payload.config || {};
    cfg.brand_palette = normalizeBrandPalette(palette);
    cfg.appearance_mode = "light";
    cfg.theme = {};

    await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cfg),
    });
    settingsCache = cfg;
  } catch (err) {
    console.error("Failed to persist brand palette", err);
  }
}

togglePauseBtn.addEventListener("click", togglePause);
toggleArrangeBtn.addEventListener("click", toggleArrangeMode);
setRateBtn.addEventListener("click", updateRefreshRate);
refreshNowBtn.addEventListener("click", () => refreshNow(null));
exportBtn.addEventListener("click", exportSnapshot);
openSettingsBtn.addEventListener("click", openSettingsModal);
closeSettingsBtn.addEventListener("click", closeSettingsModal);
reloadSettingsBtn.addEventListener("click", loadSettingsIntoForm);
saveSettingsBtn.addEventListener("click", saveSettings);
searchInput.addEventListener("input", () => snapshotCache && render(snapshotCache));
statusFilter.addEventListener("change", () => snapshotCache && render(snapshotCache));
categoryFilter?.addEventListener("change", () => snapshotCache && render(snapshotCache));
brandPaletteSelect?.addEventListener("change", () => {
  const next = normalizeBrandPalette(brandPaletteSelect.value);
  currentBrandPalette = next;
  if (settingsCache) settingsCache.brand_palette = next;
  if (snapshotCache) snapshotCache.brand_palette = next;
  saveBrandPalette(next);
  applyVisualSettings({ palette: next });
  void persistBrandPalette(next);
});
layoutModeSelect?.addEventListener("change", () => {
  preferredLayoutMode = normalizeLayoutMode(layoutModeSelect.value);
  saveLayoutMode(preferredLayoutMode);
  applyLayoutAndDensity();
  if (snapshotCache) render(snapshotCache);
});
densityModeSelect?.addEventListener("change", () => {
  preferredDensityMode = normalizeDensityMode(densityModeSelect.value);
  saveDensityMode(preferredDensityMode);
  applyLayoutAndDensity();
  if (snapshotCache) render(snapshotCache);
});
toggleGlanceBtn?.addEventListener("click", () => {
  glanceMode = !glanceMode;
  saveGlanceMode(glanceMode);
  applyLayoutAndDensity();
  if (snapshotCache) render(snapshotCache);
});
wallboardBtn.addEventListener("click", () => {
  document.body.classList.toggle("wallboard");
});
window.addEventListener("resize", () => {
  if (preferredLayoutMode === DEFAULT_LAYOUT_MODE) {
    applyLayoutAndDensity();
    if (snapshotCache) render(snapshotCache);
  }
});

cardsContainer.addEventListener("click", (event) => {
  const refreshBtn = event.target.closest(".source-refresh");
  const toggleBtn = event.target.closest(".source-toggle");

  if (refreshBtn) {
    refreshNow(refreshBtn.dataset.source);
  }

  if (toggleBtn) {
    toggleSource(toggleBtn.dataset.source);
  }
});

cardsContainer.addEventListener("dragstart", (event) => {
  if (!arrangeMode) {
    event.preventDefault();
    return;
  }
  const card = event.target.closest(".card");
  if (!card) return;
  event.dataTransfer.setData("text/plain", card.dataset.source || "");
  event.dataTransfer.effectAllowed = "move";
});

cardsContainer.addEventListener("dragover", (event) => {
  if (!arrangeMode) return;
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
});

cardsContainer.addEventListener("drop", (event) => {
  if (!arrangeMode) return;
  event.preventDefault();
  const targetCard = event.target.closest(".card");
  if (!targetCard) return;
  const draggedSource = event.dataTransfer.getData("text/plain");
  const targetSource = targetCard.dataset.source;
  reorderCardOrder(draggedSource, targetSource);
  if (snapshotCache) render(snapshotCache);
});

settingsModal.addEventListener("click", (event) => {
  if (event.target === settingsModal) {
    closeSettingsModal();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !settingsModal.classList.contains("hidden")) {
    closeSettingsModal();
  }
});

currentBrandPalette = loadBrandPalette();
applyVisualSettings({ palette: currentBrandPalette });
preferredLayoutMode = loadLayoutMode();
preferredDensityMode = loadDensityMode();
glanceMode = loadGlanceMode();
applyLayoutAndDensity();
loadSnapshot();
startAutoRefresh();
cardOrder = loadCardOrder();
