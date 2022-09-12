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
@app.route("/addDevice", methods=['GET', 'POST'])
def addDevice():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor)

    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    status = -1
    if request.method == 'POST' :

      equipment = request.form['equipment']
      model = request.form['model']
      manufacturer = request.form['manufacturer']
      sn = request.form['sn']
      prod_date = request.form["prod-date"]
      supp_date = request.form["supp-date"]
      location = request.form['location']
      country = request.form['country']
      
      contract = request.form['contract-type']
      maintenance_contract_type = request.form['maintenance-contract-type']
      if contract == "Contract of Maintenance":
        contract = contract + " - " + maintenance_contract_type

      contract_start_date = request.form['contract-start-date']
      contract_end_date = request.form['contract-end-date']
      
      inspection_list = request.files['inspection-list']
      inspection_freq = request.form['inspection-freq']
      inspection_start_date = request.form['inspection-start-date']

      ppm_list = request.files['ppm-list']
      ppm_external = request.form.getlist('ppm-external')
      ppm_freq = request.form['ppm-freq']
      ppm_start_date = request.form['ppm-start-date']

      calibration_list = request.files['calibration-list']
      calibration_external = request.form.getlist('calibration-external')
      calibration_freq = request.form['calibration-freq']
      calibration_start_date = request.form['calibration-start-date']

      technical_status = request.form.getlist('technical-status')
      PF_problem = request.form['PF-problem']
      NF_problem = request.form['NF-problem']
      if technical_status == "FF":
        problem = ''
      elif technical_status == "PF":
        problem = PF_problem
      elif technical_status == "NF":
        problem = NF_problem

      trc = request.form.getlist('trc')
      description = request.form['description']

      code = request.form['code']

      ### Insert Process
      try:
        mycursor.execute('SELECT equipment_id FROM equipment where equipment_name = %s',(equipment))
        equipment_id = mycursor.fetchone()

        mycursor.execute('SELECT model_id FROM model where model_name = %s',(model))
        model_id = mycursor.fetchone()

        mycursor.execute('SELECT manufacturer_id FROM manufacturer where manufacturer_name = %s',(manufacturer))
        manufacturer_id = mycursor.fetchone()

        mycursor.execute('SELECT location_id FROM location where location_name = %s',(location))
        location_id = mycursor.fetchone()

        mycursor.execute("""INSERT INTO device (`device_sn`, `equipment_id`, `model_id`, `manufacturer_id`, `device_production_date`, `device_supply_date`, `location_id`, `device_country`, `device_contract_type`, `contract_start_date`, `contract_end_date`, `terms`, `inspection_list`, `ppm_list`, `calibration_list`, `technical_status`, `problem`, `TRC`, `QRcode`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                                                            (sn, equipment_id, model_id, manufacturer_id, prod_date, supp_date, location_id, country, contract, contract_start_date, contract_end_date, description, inspection_list, ppm_list, calibration_list, technical_status, problem, trc, code ))
        mydb.commit()
        status = 1

      except:
        status = 0
      
    return render_template("add.html",
                          title="Add New Device",
                          status=status,
                          equipments=equipments,
                          models=models,
                          locations=locations,
                          manufacturers=manufacturers)
  else:
    return redirect(url_for('login'))

# Add New device
@app.route("/settings", methods=['GET', 'POST'])
def settings():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor)
  
    # Lists
    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']
    
    status = -1
    if request.method == 'POST' :
      # Insert Equipments
      statments = request.form['statments']
      statmentsList = statments.split(";")
      
      try:
        for statment in statmentsList:
            mycursor.execute(statment)
        mydb.commit()
        status = 1
        
      except:
        status = 0
    
    db_tables = database.retrive_tables(mycursor)
  
    # Lists
    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    return render_template("settings.html", 
                          title="Settings",
                          status=status,
                          equipments=equipments,
                          models=models,
                          locations=locations,
                          manufacturers=manufacturers)
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