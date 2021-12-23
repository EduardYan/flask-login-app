"""
This is the principal file for execute
the server.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from models.user import User
from models.password import Password
from models.database import DataBase, DB_PATH
from data.messages import MESSAGES_ERRORS
from data.queries import GET_FOR_ID, GET_FOR_NAME, INSERT_NEW_USER
from bcrypt import checkpw, gensalt, hashpw

# variable for the visits
visits = 0

# creating the server
app = Flask(__name__)

# setting for the server
app.config['SECRET_KEY'] = 'mysecretkey'

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

  # getting the users and names for validate
  users_list = db.select('SELECT * FROM users')
  names_list= [user[1] for user in users_list]
  user = db.select(GET_FOR_NAME.format(name = name))[0]
  db.close()


  # validating if the name passed in the url is in the database
  if name in names_list:
    return render_template('index.html', user = user)

  else:
    return render_template('errors/not-log.html')

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
  password = request.form['password-user']
  salt = gensalt()
  password_hashed = hashpw(password.encode(), salt) # getting the password in hash

  db = DataBase(DB_PATH) # connecting

  # getting the users and names for validat
  users_list = db.select('SELECT * FROM users')
  names_list= [user[1] for user in users_list]

  # validating if the name is in the list of the database
  if name in names_list:
    password_hashed = db.select(f'SELECT password FROM users WHERE(name = "{name}")')[0][0]

    if checkpw(password.encode(), password_hashed.encode()): # validating the password
      return redirect(f'/home/{name}')
    else:
      flash(MESSAGES_ERRORS['password-incorrect'].format(name = name))
      return redirect(url_for('save_user'))

  else:
    # creating a user
    user = User(name, password_hashed)

    # validating the password
    if password == '':
      flash(MESSAGES_ERRORS['password-empty'])

      return redirect(url_for('save_user'))

    # in case the password is short
    elif not len(password) > 5:
      flash(MESSAGES_ERRORS['less-characters'])
      return redirect(url_for('save_user'))

    else:
      # in case not in the database
      db.insert( INSERT_NEW_USER.format(name = user.name, password = user.password.content) )
      db.close()

      return redirect(f'/home/{user.name}') # rediricting with the route in the name of the user

@app.route('/about/<string:name>')
def about(name):
  """
  This route is for render
  the about page.
  """

  # selecting only the id and the name for send to about page
  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_NAME.format(name = name))[0]
  db.close()

  return render_template('about.html', user = user)


@app.route('/mycount/<string:name>', methods = ['GET'])
def my_acount(name):
  """
  This route is for show the count
  of the user.
  """

  # selecting the id and the name
  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_NAME.format(name = name))[0]
  db.close()

  # user = User(user[0], user[1])
  return render_template('count.html', user = user)

@app.route('/change-password/<string:id>', methods = ['GET'])
def change_password_template(id):
  """
  This is the route for render the template
  for change the password of the user.
  """
  
  db = DataBase(DB_PATH)
  user = db.select(f'SELECT id, name FROM users WHERE(id = {id})')[0]
  db.close()

  # return render_template('change-password.html', user = user)
  return render_template('forms/change-password.html', user = user)

@app.route('/validate-password/<string:id>', methods= ['GET'])
def validate_password_template(id):
  """
  This route is for render the page
  for validate the password.
  """

  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_ID.format(id = id))[0]
  db.close()

  return render_template('forms/validate-password.html', user = user)

@app.route('/validate-password/<string:id>', methods = ['POST'])
def validate_password(id):
  """
  This route is for validate the password
  of the user for change, and render the page for change it.
  """

  password_to_validate = request.form['password-to-validate'].encode()

  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_ID.format(id = id))[0]
  db.close()

  if checkpw(password_to_validate, user[2].encode()):
    return redirect(f'/change-password/{user[0]}')

  else:
    flash(MESSAGES_ERRORS['password-incorrect'].format(name = user[1]))
    return redirect(f'/validate-password/{user[0]}')

@app.route('/validate-password-for-name/<string:id>', methods= ['GET'])
def validate_password_for_name_template(id):
  """
  This route is for render the page
  for validate the password in case the data to change
  is the name.
  """

  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_ID.format(id = id))[0]
  db.close()

  return render_template('forms/validate-password-for-name.html', user = user)

@app.route('/validate-password-for-name/<string:id>', methods = ['POST'])
def validate_password_for_name(id):
  """
  This route is for validate the password
  in case is the name to change.
  """
  print('hello')

  password_to_validate = request.form['password-to-validate'].encode()

  db = DataBase(DB_PATH)
  user = db.select(f'SELECT id, name, password FROM users WHERE(id = {id})')[0]
  db.close()

  if checkpw(password_to_validate, user[2].encode()):
    return redirect(f'/change-name/{user[0]}')

  else:
    flash(MESSAGES_ERRORS['password-incorrect'].format(name = user[1]))
    return redirect(f'/validate-password-for-name/{user[0]}')


@app.route('/change-password/<string:id>', methods = ['POST'])
def change_password(id):
  """
  This route is for
  change the password of the user.

  The route recived the id for change
  the password of the user.
  """

  db = DataBase(DB_PATH)
  user = db.select(f'SELECT id FROM users WHERE(id = {id})')[0]
  new_password = request.form['new-password']

  salt = gensalt()
  new_password = hashpw(new_password.encode(), salt)
  new_password = Password(new_password)

  db.update(f'UPDATE users SET password = "{new_password.content}" WHERE(id = {user[0]})')
  user = db.select(f'SELECT name FROM users WHERE(id = {id})')[0]
  db.close()

  flash('Password Updated')

  return redirect(f'/home/{user[0]}')


@app.route('/change-name/<string:id>', methods = ['GET'])
def change_name_template(id):
  """
  This is the route for render the template
  for change the name.
  """

  db = DataBase(DB_PATH)
  user = db.select(GET_FOR_ID.format(id = id))[0]
  db.close()

  return render_template('forms/change-name.html',  user = user)

@app.route('/change-name/<string:id>', methods = ['POST'])
def change_name(id):
  """
  This route is for
  change the name of the user.

  The route recived the id, for change the name.
  """

  db = DataBase(DB_PATH)
  user = db.select(f'SELECT id FROM users WHERE(id = {id})')[0]
  new_name = request.form['new-name']

  print(user[0])
  print(f'UPDATE users SET name = "{new_name}" WHERE(id = {int(user[0])})')
  db.update(f'UPDATE users SET name = "{new_name}" WHERE(id = {int(user[0])})')

  print(id)
  print(type(id))

  user = db.select(f'SELECT name FROM users WHERE(id = {id})')[0]

  db.close()

  flash('Name Updated Sucessfully')

  return redirect(f'/home/{user[0]}')


if __name__== '__main__':
  # running the server
  app.run(host = '0.0.0.0', port = 4000, debug = True)
