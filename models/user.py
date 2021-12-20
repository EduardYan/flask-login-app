"""
This module have the class user, for create
a model of th user.
"""

class User:
  def __init__(self, name) -> None:
      self.name = name

  def __str__(self) -> str:
      return f'This is a user with name {self.name}.'