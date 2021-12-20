"""
This is the principal file for execute
the server.
"""

from flask import Flask, render_template, request, redirect, url_for
from models.user import User
from models.database import DataBase, DB_PATH

# variable for the visits
visits = 0

# creating the server
app = Flask(__name__)

@app.route('/<string:name>')
@app.route('/home/<string:name>')
def home(name):
  """
  This route is for the initial 
  route, of the server.
  """

  global visits
  visits += 1 # adding the visits

  db = DataBase(DB_PATH) # connectiong

  # getting the users and names for validat
  users_list = db.select('SELECT * FROM users')
  names_list= [user[1] for user in users_list]


  # validating if the name passed in the url is in the database
  if name in names_list:
    return render_template('index.html', username = name)

  else:
    return render_template('not-log.html')

@app.route('/login', methods = ['GET'])
def login():
  """
  This route is for render the login
  page.
  """

  return render_template('login.html')

@app.route('/login', methods = ['POST'])
def save_user():
  """
  This route is for save the user
  in the database.
  """

  # gettings the info of the user for save in the database
  name = request.form['name-user']

  db = DataBase(DB_PATH) # connectiong

  # getting the users and names for validat
  users_list = db.select('SELECT * FROM users')
  names_list= [user[1] for user in users_list]

  # validating if the name is in the list of the database
  if name in names_list:
    return redirect(f'/home/{name}')

  else:
    # creating a user
    user = User(name)
    # in case not in the database
    db.insert( f'INSERT INTO users VALUES(NULL, "{user.name}")' )
    db.close()

    return redirect(f'/home/{user.name}') # rediricting with the route in the name of the user


@app.route('/about')
def about():
  """
  This route is for render
  the about page.
  """

  return render_template('about.html')

if __name__== '__main__':
  # running the server
  app.run(host = '0.0.0.0', port = 4000, debug = True)