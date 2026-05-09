def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_participant(client):
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 200
    assert "Signed up test@mergington.edu for Chess Club" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_duplicate_signup(client):
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "Removed michael@mergington.edu from Chess Club" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_missing_participant(client):
    response = client.delete("/activities/Chess%20Club/participants?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
