# Imports
from flask import Flask, render_template, request, redirect, url_for, session
import json
import database
import pandas as pd
import os
from werkzeug.utils import secure_filename
import re # Regex
#--------------------------------------------------------------------------#

"""Functions"""
# Get Dates
def getDates(start_date, freq, period):
    
    if(freq == "Monthly"):
        freq = 'M' 
        periods = period * 12
    elif(freq == "3 Months"):
        freq = '3M'
        periods = period * 4
    elif(freq == "6 Months"):
        freq = '6M'
        periods = period * 2
    elif(freq == "Annually"):
        freq = '12M'
        periods = period * 1

    datesList = pd.date_range(start_date, periods=periods, freq=freq, inclusive="both")

    return datesList 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_DOC

def saveFile(list, sn, fileName):
  if list and allowed_file(list.filename):
        filename = secure_filename(fileName + "." + list.filename.rsplit('.', 1)[1])
        path = app.config['UPLOAD_FOLDER'] + sn + "/" 
        os.makedirs(path, exist_ok=True)
        list.save(os.path.join(path, filename))
#--------------------------------------------------------------------------#

# Connecting with Database
mydb, mycursor = database.mysql_connector()

"""Retrive Database Tables"""
db_tables = database.retrive_tables(mycursor)

#--------------------------------------------------------------------------#

"""Our app"""
app = Flask(__name__)
app.secret_key = 'hlzgzxpzlllkgzrn' # Your Secret_Key
UPLOAD_FOLDER = "static/UPLOAD/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS_DOC = set(['pdf', 'doc', 'xlsx', 'png', 'jpg', 'jpeg'])


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
      saveFile(inspection_list, sn, "inspection")

      ppm_list = request.files['ppm-list']
      ppm_external = request.form.getlist('ppm-external')
      ppm_freq = request.form['ppm-freq']
      ppm_start_date = request.form['ppm-start-date']
      saveFile(ppm_list, sn, 'ppm')

      calibration_list = request.files['calibration-list']
      calibration_external = request.form.getlist('calibration-external')
      calibration_freq = request.form['calibration-freq']
      calibration_start_date = request.form['calibration-start-date']
      saveFile(calibration_list, sn, 'calibration')
          
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
      description_file = request.files['description-file']
      saveFile(description_file, sn, 'description')

      code = request.form['code']

      createdAt = pd.to_datetime("today")
      createdAt = f"{createdAt.year}-{createdAt.month}-{createdAt.day}"
      
      ## Additional Information
      settings = db_tables['settings']
      service_period = settings[0][1]

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

        print((sn, equipment_id, model_id, manufacturer_id, prod_date, supp_date, location_id, country, contract, contract_start_date, contract_end_date, description, description_file, inspection_list, ppm_list, ppm_external, calibration_list, calibration_external, technical_status, problem, trc, code, createdAt, "" ))
        mycursor.execute("""INSERT INTO device (`device_sn`, `equipment_id`, `model_id`, `manufacturer_id`, `device_production_date`, `device_supply_date`, `location_id`, `device_country`, `device_contract_type`, `contract_start_date`, `contract_end_date`, `terms`, `terms_file`, `inspection_list`, `ppm_list`, `ppm_external`, `calibration_list`, `calibration_external`, `technical_status`, `problem`, `TRC`, `QRcode`, `createdAt` ,`updatedAt`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                                                            (sn, equipment_id, model_id, manufacturer_id, prod_date, supp_date, location_id, country, contract, contract_start_date, contract_end_date, description, description_file, inspection_list, ppm_list, ppm_external, calibration_list, calibration_external, technical_status, problem, trc, code, createdAt, "" ))
       
        # Inspection
        inspectionsList = getDates(inspection_start_date, inspection_freq, service_period)
        for date in inspectionsList:
          mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                    ("Inspection", sn, date, "NOT YET"))
        # PPM
        PPMsList = getDates(ppm_start_date, ppm_freq, service_period)
        for date in PPMsList:
          mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                    ("PPM", sn, date, "NOT YET"))
        # Calibration
        calibrationsList = getDates(calibration_start_date, calibration_freq, service_period)
        for date in calibrationsList:
          mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                    ("Calibration", sn, date, "NOT YET"))

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
    settings = db_tables['settings']
    service_period = settings[0][1]
    
    status = -1
    if request.method == 'POST' :
      # Insert Equipments
      service_period = request.form['service-period']

      statments = request.form['statments']
      statmentsList = statments.split(";")
    
      try:
        # Update Settings
        mycursor.execute("""UPDATE `settings`
                            SET `id`=1, `service_period` = %s
                            WHERE `id`=1""", (service_period,))

        # Update Libraries
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
                          manufacturers=manufacturers,
                          service_period=service_period)
  else:
    return redirect(url_for('login'))

# Add New device
@app.route("/search", methods=['GET', 'POST'])
def search():
  data = list()
  if request.method == 'POST' :
    
    device_sn = request.form['device_sn'],
    equipment = request.form['equipment']
    model = request.form['model']
    manufacturer = request.form['manufacturer']
    device_production_date = request.form['device_production_date']
    device_supply_date = request.form['device_supply_date']
    location = request.form['location'] 
    device_country = request.form['device_country']
    device_contract_type = request.form['device_contract_type'],
    contract_start_date = request.form['contract_start_date'],
    contract_end_date = request.form['contract_end_date'],
    technical_status = request.form['technical_status'],
    TRC = request.form['TRC'],
    Code = request.form['Code']

    equipment_id = 0,
    model_id = 0,
    manufacturer_id = 0
    location_id = 0

    mycursor.execute("""
    SELECT 
      device_sn, 
      equipment_name, 
      model_name, 
      manufacturer_name, 
      device_production_date, 
      device_supply_date, 
      location_name, 
      device_country, 
      device_contract_type, 
      contract_start_date, 
      contract_end_date, 
      terms, 
      inspection_list, 
      ppm_list, 
      ppm_external,
      calibration_list, 
      calibration_external,
      technical_status, 
      problem, 
      TRC, 
      Code
    FROM `device`
    left JOIN equipment
      ON device.equipment_id = equipment.equipment_id
    left JOIN model
      ON device.model_id = model.model_id
    left JOIN manufacturer
      ON device.manufacturer_id = manufacturer.manufacturer_id
    left JOIN location
      ON device.location_id = location.location_id
    WHERE 
      `device_sn` LIKE %s AND
      `equipment_name`LIKE %s AND
      `model_name` LIKE %s AND
      `manufacturer_name` LIKE %s AND
      `device_production_date` LIKE %s AND
      `device_supply_date` LIKE %s AND
      `location_name` LIKE %s AND
      `device_country` LIKE %s AND
      `device_contract_type` LIKE %s AND
      `contract_start_date` LIKE %s AND
      `contract_end_date` LIKE %s AND
      `technical_status` LIKE %s AND
      `TRC` LIKE %s AND
      `Code LIKE %s`
    """,(device_sn,
      equipment_id,
      model_id,
      manufacturer_id,
      device_production_date,
      device_supply_date,
      location_id,
      device_country,
      device_contract_type,
      contract_start_date,
      contract_end_date,
      technical_status,
      TRC,
      Code))

    data = mycursor.fetchall()


  return render_template("search.html",
                  numOfResults=len(data),
                  devices=data)

#  Services
@app.route("/services", methods=['GET', 'POST'])
def services():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor)
    return render_template("services.html",
                          numOfResults=len(db_tables['service']),
                          services=db_tables['service'])
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