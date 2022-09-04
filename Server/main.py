# Imports
from flask import Flask, render_template, request, redirect, url_for, session
import json
import database
import re # Regex
#--------------------------------------------------------------------------#

"""Functions"""
# //

#--------------------------------------------------------------------------#

# Connecting with Database
mydb, mycursor = database.mysql_connector()

"""Retrive Database Tables"""
db_tables = database.retrive_tables(mycursor)

#--------------------------------------------------------------------------#

"""Our app"""
app = Flask(__name__)
app.secret_key = 'hlzgzxpzlllkgzrn' # Your Secret_Key

#--------------------------------------------------------------------------#

""" Routes of Pages """
# Home Page
@app.route("/")
def home():
  db_tables = database.retrive_tables(mycursor)

  if 'loggedin' in session and session['loggedin'] == True:
    return render_template("index.html",
                       title="Dashboard")
  else:
    return redirect(url_for('login'))



# Add New device
@app.route("/AddDevice", methods=['GET', 'POST'])
def addDevice():
  db_tables = database.retrive_tables(mycursor)
  if 'loggedin' in session and session['loggedin'] == True:
    return render_template("add.html",
                          title="Add New Device")
  else:
    return redirect(url_for('login'))

# Login
@app.route("/login", methods=['GET', 'POST'])
def login():
  if 'loggedin' in session and session['loggedin'] == True:
    return redirect(url_for('home'))
  else:
    status = True
    if request.method == 'POST':
      username  = request.form['username']
      password  = request.form['password']

      # Check if account exists using MySQL
      mycursor.execute('SELECT * FROM admin WHERE `username` = %s AND `passwd` = %s', (username, password,))

      # Fetch one record and return result
      account = mycursor.fetchone()
      print(username,password)
      print(account)

      # If account exists in accounts table in out database
      if account:
          # Create session data, we can access this data in other routes
          session['loggedin'] = True
          session['id'] = account[0]
          session['username'] = account[1]
          status = True
          # Redirect to home page
          return redirect(url_for('home'))
      else:
          # Account doesnt exist or username/password incorrect
          status = False

    return render_template("login.html",
                          title="Login",
                          status=status)

# Logout
@app.route("/logout")
def logout():
  # Remove session data, this will log the user out
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('username', None)
  # Redirect to login page
  return redirect(url_for('login'))



# Run app
if __name__ == "__main__":  

  app.run(debug=True,port=9000)