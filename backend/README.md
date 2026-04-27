# Home Streak Backend API

FastAPI backend for the Home Streak mobile application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Households
- `POST /households` - Create a new household
- `GET /households` - Get all households

### Users
- `POST /users` - Create a new user
- `GET /users/{username}` - Get user details
- `GET /users` - Get all users

### Habits
- `POST /habits` - Create a new habit
- `GET /habits` - Get all habits
- `POST /habits/complete` - Complete a habit

### Leaderboard
- `GET /leaderboard/{household_name}` - Get current leaderboard
- `GET /leaderboard/{household_name}/past` - Get past rankings
- `GET /top-performers` - Get top performers

### Admin
- `POST /reset-monthly` - Reset monthly scores
- `DELETE /data` - Clear all data
