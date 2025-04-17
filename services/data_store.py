"""Module for handling data persistence in the habit tracking application."""
import json

DATA_FILE = "data.json"

def load_data():
    """Loads data from JSON file or initializes default structure."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                data = json.loads(content)
            else:
                data = create_default_structure()
    except (FileNotFoundError, json.JSONDecodeError):
        data = create_default_structure()
    
    # Ensure all required fields exist
    if "bonus_habits" not in data:
        data["bonus_habits"] = []
    if "streaks" not in data:
        data["streaks"] = {}
    return data

def save_data(data):
    """Saves data to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def create_default_structure():
    """Creates the default data structure."""
    return {
        "households": {}, 
        "habits": [], 
        "bonus_habits": [],  
        "leaderboard": {"rankings": {}, "past_rankings": []},
        "streaks": {}  
    }
