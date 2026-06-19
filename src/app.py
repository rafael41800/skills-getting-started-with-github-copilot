"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team soccer practices and matches",
        "schedule": "Mondays & Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Swimming Club": {
        "description": "Swimming training sessions and competitions",
        "schedule": "Tuesdays & Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Art Club": {
        "description": "Painting, drawing, and creative art workshops",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Theater rehearsals and performance practice",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Team": {
        "description": "Competitive debate practice and tournaments",
        "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Olympiad": {
        "description": "Hands-on science problem solving and challenge prep",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Normalize and validate email
    normalized_email = email.strip().lower()

    # Prevent duplicate sign-ups
    if normalized_email in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Prevent over-capacity
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity."""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    # Find and remove participant (case-insensitive)
    for p in list(activity["participants"]):
        if p.strip().lower() == normalized_email:
            activity["participants"].remove(p)
            return {"message": f"Unregistered {normalized_email} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Student not signed up for this activity")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
