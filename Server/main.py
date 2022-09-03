# Imports
from flask import Flask, render_template, request, redirect, url_for, session
import json
import database
import re # REGEX
#--------------------------------------------------------------------------#

"""Functions"""
# //

#--------------------------------------------------------------------------#

# Connecting with Database
mydb, mycursor = database.mysql_connector()

"""Retrive Database Tables"""
db_tables = database.retrive_tables(mycursor)

#--------------------------------------------------------------------------#

"""Our Website"""
website = Flask(__name__)

#--------------------------------------------------------------------------#

""" Routes of Pages """
# Home Page
@website.route("/Dashboard")
def Home():
  
  return render_template("index.html",
                        title="Dashboard")


# Add New device
@website.route("/AddDevice", methods=['GET', 'POST'])
def AddDevice():
  
  return render_template("add.html",
                        title="Add New Device")

# Login
@website.route("/", methods=['GET', 'POST'])
def Login():
  
  return render_template("login.html",
                        title="Login")


# Run app
if __name__ == "__main__":  
  website.run(debug=True,port=9000)