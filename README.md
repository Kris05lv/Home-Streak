# Home-Streak

This is a fun command-line habit tracker designed to promote healthy habits within the family through a game-like point system. The tracker allows individual users to join a household and compete amongst each other by gaining points for each habit they complete.

## Features
* Track daily and weekly habits
* Earn points for every habit you complete
* Bonus habits that are worth more points and work on a first-come, first-served basis
* Rewards for streaks
* Household leaderboard that allows you to compete with your family members
* Persistent JSON data storage 
* Simple and efficient habit management through the Command-Line Interface (CLI)
* Analytics module to gain insights into habits

## Installation

### Prerequisites
* Python 3.11 or higher
* pip package manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Kris05lv/Home-Streak.git
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate your environment:
   * Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   * macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python cli.py [OPTIONS] COMMAND [ARGS]
```

To show help message and exit, use:
```bash
python cli.py --help
```

### Available Commands

* `create-household` - Create a new household
* `add-user` - Add a user to a household
* `add-habit` - Add a habit with periodicity and points
* `add-bonus-habit` - Add a bonus habit worth extra points (first-come, first-serve)
* `complete-habit` - Mark a habit as completed and update streaks
* `list-habits` - List all habits in the system
* `view-leaderboard` - View current household leaderboard rankings
* `view-past-rankings` - View past leaderboard rankings
* `view-top-performers` - View the top performers of past months
* `reset-monthly-scores` - Reset all users' monthly scores
* `clear-data` - Clear all data in the system (reset data.json)

## Data Storage
The application uses a JSON file (`data.json`) to persistently store all habit tracking data, including:
* Household information
* User profiles and scores
* Habit definitions and completion records
* Streak information

## Testing
To run the test suite:
```bash
pytest
```

This will run all unit tests and ensure the application is functioning correctly. The tests cover:
* Habit management
* User management
* Household operations
* Leaderboard functionality
* Data persistence

## Future Enhancements
* Add bonus points for extra completions (e.g., eating 2 fruits instead of the required 1)
* Add support for custom habit categories
* Implement habit suggestions based on user preferences
* Add weekly and monthly habit completion reports
* Implement achievement badges for consistent habit completion

## Contributing
Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run the tests to ensure everything works
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

Please make sure to update tests as appropriate and adhere to the existing coding style.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
