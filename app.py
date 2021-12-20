"""
This is the principal file for execute
the server.
"""

from flask import Flask, render_template

app = Flask()

@app.route('/')
@app.route('/home')
def home():
  """
  This route is for the initial 
  route, of the server.
  """

  return render_template('index.html')

if __name__== '__main__':
  app.run(host = '0.0.0.0', port = 4000, debug = True)