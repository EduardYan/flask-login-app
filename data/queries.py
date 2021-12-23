"""
This module have some queries
for make in the database.
"""

# queries
GET_FOR_ID = 'SELECT id, name FROM users WHERE(id = {id})'
GET_FOR_NAME = 'SELECT id, name FROM users WHERE(name = "{name}")'
INSERT_NEW_USER = 'INSERT INTO users VALUES(NULL, "{name}", "{password}")'