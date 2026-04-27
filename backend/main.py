from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.data_manager import DataManager, leaderboard
from classes.habit import Habit
from classes.user import User

app = FastAPI(title="Home Streak API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HouseholdCreate(BaseModel):
    name: str
    password: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    household_name: str

class HouseholdAuth(BaseModel):
    household_name: str
    password: str

class HabitCreate(BaseModel):
    name: str
    periodicity: str
    points: int
    is_bonus: bool = False

class HabitComplete(BaseModel):
    username: str
    habit_name: str

@app.get("/")
def read_root():
    return {"message": "Home Streak API", "version": "1.0.0"}

@app.post("/households")
def create_household(household: HouseholdCreate):
    try:
        DataManager.create_household(household.name)
        return {"message": f"Household '{household.name}' created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/households")
def get_households():
    data = DataManager.load_data()
    return {"households": list(data["households"].keys())}

@app.post("/users")
def create_user(user: UserCreate):
    try:
        data = DataManager.load_data()
        if user.household_name not in data["households"]:
            raise ValueError(f"Household '{user.household_name}' does not exist")
        
        new_user = User(user.username, user.household_name, 0)
        new_user.habits_completed = {}
        new_user.streaks = {}
        new_user.bonus_claimed = {}
        DataManager.save_user(new_user)
        leaderboard.update(new_user)
        
        return {"message": f"User '{user.username}' added to household '{user.household_name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{username}")
def get_user(username: str):
    user = DataManager.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return user.to_dict()

@app.get("/users")
def get_all_users():
    users = DataManager.load_users()
    return {"users": users}

@app.post("/habits")
def create_habit(habit: HabitCreate):
    try:
        new_habit = Habit(habit.name, habit.periodicity, habit.points, habit.is_bonus)
        if habit.is_bonus:
            DataManager.save_bonus_habit(new_habit)
        else:
            DataManager.save_habit(new_habit)
        return {"message": f"Habit '{habit.name}' created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/habits")
def get_habits():
    habits = DataManager.load_habits()
    return {"habits": habits}

@app.post("/habits/complete")
def complete_habit(completion: HabitComplete):
    result = DataManager.complete_habit(completion.username, completion.habit_name)
    if not result:
        raise HTTPException(status_code=400, detail=f"Could not complete habit '{completion.habit_name}'")
    
    data = DataManager.load_data()
    bonus_habit = next((h for h in data["bonus_habits"] if h["name"] == completion.habit_name), None)
    
    if bonus_habit:
        return {"message": f"Bonus Habit '{completion.habit_name}' claimed by '{completion.username}'"}
    return {"message": f"Habit '{completion.habit_name}' completed by '{completion.username}'"}

@app.get("/leaderboard/{household_name}")
def get_leaderboard(household_name: str):
    rankings = leaderboard.get_sorted_rankings(household_name)
    if not rankings:
        return {"household": household_name, "rankings": []}
    
    rankings_list = [
        {"rank": idx + 1, "username": username, "points": points}
        for idx, (username, points) in enumerate(rankings.items())
    ]
    return {"household": household_name, "rankings": rankings_list}

@app.get("/leaderboard/{household_name}/past")
def get_past_rankings(household_name: str):
    data = DataManager.load_data()
    if "leaderboard" not in data or "past_rankings" not in data["leaderboard"]:
        return {"past_rankings": []}
    return {"past_rankings": data["leaderboard"]["past_rankings"]}

@app.get("/top-performers")
def get_top_performers():
    data = DataManager.load_data()
    if "leaderboard" not in data or "top_performers" not in data["leaderboard"]:
        return {"top_performers": []}
    return {"top_performers": data["leaderboard"]["top_performers"]}

@app.post("/reset-monthly")
def reset_monthly_scores():
    leaderboard.reset_monthly()
    DataManager.reset_monthly_scores()
    return {"message": "Monthly scores reset successfully"}

@app.delete("/data")
def clear_all_data():
    DataManager.clear_data()
    return {"message": "All data cleared successfully"}

@app.post("/admin/members")
def add_family_member(username: str, household_name: str):
    """Admin endpoint to add a family member"""
    try:
        new_user = User(username, household_name, 0, is_admin=False)
        new_user.habits_completed = {}
        new_user.streaks = {}
        new_user.bonus_claimed = {}
        DataManager.save_user(new_user)
        leaderboard.update(new_user)
        return {"message": f"Member '{username}' added to household '{household_name}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/households/{household_name}/members")
def get_household_members(household_name: str):
    """Get all members of a household"""
    data = DataManager.load_data()
    if household_name not in data["households"]:
        raise HTTPException(status_code=404, detail=f"Household '{household_name}' not found")
    
    members = []
    for username in data["households"][household_name]["members"]:
        user_data = data["user_data"].get(username, {})
        members.append({
            "username": username,
            "points": user_data.get("points", 0),
            "is_admin": user_data.get("is_admin", False)
        })
    return {"members": members}

@app.post("/households/{household_name}/admin")
def create_household_with_admin(household_name: str, admin_username: str, password: Optional[str] = None):
    """Create household and set first user as admin"""
    try:
        DataManager.create_household(household_name)
        
        # Store household password if provided
        if password:
            data = DataManager.load_data()
            if "household_passwords" not in data:
                data["household_passwords"] = {}
            data["household_passwords"][household_name] = password
            DataManager.save_data(data)
        
        admin_user = User(admin_username, household_name, 0, is_admin=True)
        admin_user.habits_completed = {}
        admin_user.streaks = {}
        admin_user.bonus_claimed = {}
        DataManager.save_user(admin_user)
        leaderboard.update(admin_user)
        return {"message": f"Household '{household_name}' created with admin '{admin_username}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/households/verify")
def verify_household_password(auth: HouseholdAuth):
    """Verify household password"""
    data = DataManager.load_data()
    
    if auth.household_name not in data["households"]:
        raise HTTPException(status_code=404, detail="Household not found")
    
    stored_password = data.get("household_passwords", {}).get(auth.household_name)
    
    # If no password set, allow access
    if not stored_password:
        return {"verified": True}
    
    # Check password
    if stored_password == auth.password:
        return {"verified": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")

@app.put("/households/{household_name}/password")
def update_household_password(household_name: str, new_password: str):
    """Update household password (admin only)"""
    data = DataManager.load_data()
    
    if household_name not in data["households"]:
        raise HTTPException(status_code=404, detail="Household not found")
    
    if "household_passwords" not in data:
        data["household_passwords"] = {}
    
    data["household_passwords"][household_name] = new_password
    DataManager.save_data(data)
    
    return {"message": "Password updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
