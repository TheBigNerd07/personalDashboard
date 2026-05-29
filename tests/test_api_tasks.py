from __future__ import annotations


def test_task_creation_listing_and_completion(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Finish geometry assignment",
            "category": "school",
            "priority": "high",
            "status": "active",
        },
    )
    assert create_response.status_code == 200
    task = create_response.json()
    assert task["id"]
    assert task["title"] == "Finish geometry assignment"

    list_response = client.get("/api/tasks", params={"category": "school"})
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["priority"] == "high"

    complete_response = client.post(f"/api/tasks/{task['id']}/complete")
    assert complete_response.status_code == 200
    completed = complete_response.json()
    assert completed["status"] == "completed"
    assert completed["completed_at"] is not None

