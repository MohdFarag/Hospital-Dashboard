# Imports
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import json
import database
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
@website.route("/", methods =['GET', 'POST'])
def HomePage():
  return "Hi"


# Run app
if __name__ == "__main__":  
  # Run
  website.run(debug=True,port=9000)