"""
This module have the class Password
for have a model of the passwords.
"""

class Password:
  """
  Crete a password with a content.
  """
  def __init__(self, content:bytes) -> None:
    # validating the type of data
    if type(content) not in [bytes]:
      raise TypeError('The parameter password, must be a string.')

    self.content = content
    self.len = len(content)

  def __str__(self) -> str:
    return 'This is a secure password.'