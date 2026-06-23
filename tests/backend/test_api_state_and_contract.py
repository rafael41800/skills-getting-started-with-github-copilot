from tests.conftest import INITIAL_ACTIVITIES


def test_signup_updates_only_target_activity(client):
    # Arrange
    email = "targeted@mergington.edu"

    # Act
    signup_response = client.post("/activities/Chess Club/signup", params={"email": email})
    activities_payload = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert email in activities_payload["Chess Club"]["participants"]
    assert email not in activities_payload["Programming Class"]["participants"]
    assert email not in activities_payload["Gym Class"]["participants"]


def test_multiple_signups_keep_shared_state_consistent(client):
    # Arrange
    new_students = [
        "a_student@mergington.edu",
        "b_student@mergington.edu",
        "c_student@mergington.edu",
    ]

    # Act
    for email in new_students:
        response = client.post("/activities/Chess Club/signup", params={"email": email})
        assert response.status_code == 200

    participants = client.get("/activities").json()["Chess Club"]["participants"]

    # Assert
    assert participants[-3:] == new_students
    assert len(participants) == len(INITIAL_ACTIVITIES["Chess Club"]["participants"]) + len(new_students)


def test_get_activities_response_contract_matches_expected_schema(client):
    # Arrange
    expected_activities = set(INITIAL_ACTIVITIES.keys())
    required_activity_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert set(payload.keys()) == expected_activities

    for activity_data in payload.values():
        assert set(activity_data.keys()) == required_activity_keys
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
