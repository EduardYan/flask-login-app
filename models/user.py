"""
This module have the class user, for create
a model of th user.
"""

from models.password import Password

class User:
    """
    Create a user object, with a name and a password.
    """

    def __init__(self, name:str, password:str) -> None:
        # values of the user
        self.name = name
        self.password = Password(password)

    def __str__(self) -> str:
        return f'This is a user with name {self.name}.'