"""
This is the principal file for execute
the server.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from bcrypt import checkpw, gensalt, hashpw
from models.user import User
from models.password import Password
from data.messages import MESSAGES_ERRORS

# variable for the visits
visits = 0

# creating the server
app = Flask(__name__)
# settings for the server
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/users.db'

# starting the database and creating the model for the user
db = SQLAlchemy(app)

class Users(db.Model):
  """
  This is the model for the user
  in the database.
  """

  # defining the columns for the database
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(600))
  

@app.route('/<string:name>')
@app.route('/home/<string:name>')
def home(name):
  """
  This route is for the initial 
  route, of the server.
  """

  global visits
  visits += 1 # adding the visits


  # getting the users and names for validate
  users_list = Users.query.all()
  names_list = [user.name for user in users_list]
  user = Users.query.filter_by(name = name).first()

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

  # getting the users and names for validat
  users_list = Users.query.all()
  names_list = [user.name for user in users_list]

  # validating if the name is in the list of the database
  if name in names_list:
    user = Users.query.filter_by(name = name).first()

    # creating a password object
    passwordObject = Password(user.password.encode())

    if checkpw(password.encode(), passwordObject.content.encode()): # validating the password
      return redirect(f'/home/{user.name}')
    else:
      flash(MESSAGES_ERRORS['password-incorrect'].format(name = user.name))
      return redirect(url_for('login'))

  else:
    # generating a hash for save
    salt = gensalt()
    password_hashed = hashpw(password.encode(), salt) # getting the password in hash

    # creating a user
    userObject = User(name, password_hashed)

    # validating the password
    if password == '':
      flash(MESSAGES_ERRORS['password-empty'])

      return redirect(url_for('save_user'))

    # in case the password is short
    elif not len(password) > 5:
      flash(MESSAGES_ERRORS['less-characters'])
      return redirect(url_for('save_user'))

    else:
      # in case not in the database, saving
      user = Users(id = None, name = userObject.name, password = userObject.password.content)
      db.session.add(user)
      db.session.commit()

      return redirect(f'/home/{user.name}') # redirecting with the route in the name of the user

@app.route('/about/<string:name>')
def about(name):
  """
  This route is for render
  the about page.
  """

  # selecting only the name for send to about page
  user = Users.query.filter_by(name = name).first()

  return render_template('about.html', user = user)


@app.route('/mycount/<string:name>', methods = ['GET'])
def my_acount(name):
  """
  This route is for show the count
  of the user.
  """

  # selecting the id and the name
  user = Users.query.filter_by(name = name).first()

  return render_template('count.html', user = user)

@app.route('/change-password/<string:id>', methods = ['GET'])
def change_password_template(id):
  """
  This is the route for render the template
  for change the password of the user.
  """
  
  user = Users.query.filter_by(id = int(id)).first()

  # return render_template('change-password.html', user = user)
  return render_template('forms/change-password.html', user = user)

@app.route('/validate-password/<string:id>', methods= ['GET'])
def validate_password_template(id):
  """
  This route is for render the page
  for validate the password.
  """

  user = Users.query.filter_by(id = int(id)).first()

  return render_template('forms/validate-password.html', user = user)

@app.route('/validate-password/<string:id>', methods = ['POST'])
def validate_password(id):
  """
  This route is for validate the password
  of the user for change, and render the page for change it.
  """

  # getting for validate the password
  password_to_validate = request.form['password-to-validate'].encode()
  user = Users.query.filter_by(id = int(id)).first()
  passwordObject = Password(user.password.encode())

  if checkpw(password_to_validate, passwordObject.content.encode()):
    return redirect(f'/change-password/{user.id}')

  else:
    flash(MESSAGES_ERRORS['password-incorrect'].format(name = user.name))
    return redirect(f'/validate-password/{user.id}')

@app.route('/validate-password-for-name/<string:id>', methods= ['GET'])
def validate_password_for_name_template(id):
  """
  This route is for render the page
  for validate the password in case the data to change
  is the name.
  """

  user = Users.query.filter_by(id = int(id)).first()

  return render_template('forms/validate-password-for-name.html', user = user)

@app.route('/validate-password-for-name/<string:id>', methods = ['POST'])
def validate_password_for_name(id):
  """
  This route is for validate the password
  in case is the name to change.
  """

  # getting the new password for validate
  password_to_validate = request.form['password-to-validate'].encode()
  user = Users.query.filter_by(id = int(id)).first()
  passwordObject = Password(user.password.encode())

  if checkpw(password_to_validate, passwordObject.content.encode()):
    return redirect(f'/change-name/{user.id}')

  else:
    flash(MESSAGES_ERRORS['password-incorrect'].format(name = user.name))
    return redirect(f'/validate-password-for-name/{user.id}')


@app.route('/change-password/<string:id>', methods = ['POST'])
def change_password(id):
  """
  This route is for
  change the password of the user.

  The route recived the id for change
  the password of the user.
  """

  # getting the new password and the user to update the password
  new_password = request.form['new-password']
  user = Users.query.filter_by(id = int(id)).first()

  print(new_password)

  # validating the new password
  if new_password == '':
    flash(MESSAGES_ERRORS['password-empty'])

    return redirect(f'/change-password/{user.id}')

  elif not len(new_password) > 5:
    # in case less to five
    flash(MESSAGES_ERRORS['less-characters'])
    return redirect(f'/change-password/{user.id}')

  else:
    # hashing
    salt = gensalt()
    new_password = hashpw(new_password.encode(), salt)
    new_password = Password(new_password)

    db.session.execute(
      # updating the password
      update(Users).where(Users.id == user.id).values(password = new_password.content)
    )
    db.session.commit()

    flash('Password Updated')

    return redirect(f'/home/{user.name}')


@app.route('/change-name/<string:id>', methods = ['GET'])
def change_name_template(id):
  """
  This is the route for render the template
  for change the name.
  """

  # the user for send to change-name page
  user = Users.query.filter_by(id = int(id)).first()

  return render_template('forms/change-name.html',  user = user)

@app.route('/change-name/<string:id>', methods = ['POST'])
def change_name(id):
  """
  This route is for
  change the name of the user.

  The route recived the id, for change the name.
  """

  # getting the new name for the user
  new_name = request.form['new-name']
  user = Users.query.filter_by(id = int(id)).first()

  db.session.execute(
    # updating
    update(Users).where(Users.id == user.id).values(name = new_name)
  )
  db.session.commit()

  flash('Name Updated Sucessfully')

  return redirect(f'/home/{user.name}')


if __name__== '__main__':
  # running the server
  app.run(host = '0.0.0.0', port = 3000, debug = True)
