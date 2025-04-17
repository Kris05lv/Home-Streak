"""Module for managing households in a habit tracking application.
This module provides the Household class which represents a household that 
users can join to earn points.
It includes functionality for adding users to the household and getting the 
leaderboard of users in the household.
"""
class Household:
    """A class representing a household that users can join to earn points."""
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, user):
        """Add a user to the household.

        Args:
            user: The user to add.
        """
        if user not in self.members:
            self.members.append(user)
    
    def get_leaderboard(self):
        """Get the leaderboard of users in the household.

        Returns:
            list: List of users sorted by points in descending order.
        """
        return sorted(self.members, key=lambda user: getattr(user, 'points', 0), reverse=True)
    
    def to_dict(self):
        """
        Convert the Household object to a dictionary representation.
        
        Returns:
            dict: A dictionary containing the household's data
        """
        return {
            'name': self.name,
            'members': [member.to_dict() for member in self.members]
        }