# Imports
from flask import Flask, render_template, request, redirect, url_for, session
import database
import pandas as pd
import os
from werkzeug.utils import secure_filename
import math
#--------------------------------------------------------------------------#

"""Functions"""

# Get Data Of today month services
def todaymonthServices(type):
  today = pd.to_datetime("today")

  sentenceWhere = f"WHERE service_type='{type}' AND year(`scheduled_date`)={today.year} AND month(`scheduled_date`)={today.month} AND `done_date` IS NULL"
  mycursor.execute(f"""SELECT * FROM service
                        {sentenceWhere}
                        ORDER BY scheduled_date Asc""")
  data = mycursor.fetchall()

  return data

# Get Request
def argsGet(argName):
  if request.args.get(argName):
    field = request.args.get(argName)
  else:
    field = ""
  
  return field

def listToStringWithComma(givenName, fieldName):
  # fieldName IN ({category}) AND
  givenList = request.form.getlist(givenName)
  outputString = ""

  for item in givenList:
    outputString += f"'{str(item)}'"+","

  if len(givenList) > 0:
    outputString = f"`{fieldName}` IN ({outputString[:-1]}) AND"
  else:
    outputString = ""

  return outputString


# Tuple To List
def tupleToList(tupleItem):
  listItem = list()

  for oldtuple in tupleItem:
    newList = list(oldtuple)
    listItem.append(newList)

  return listItem

# Get Dates
def getDates(start_date, end_date, freq):
    if(freq == "Monthly"):
        freq = 'M' 
    elif(freq == "3 Months"):
        freq = '3M'
    elif(freq == "6 Months"):
        freq = '6M'
    elif(freq == "Annually"):
        freq = '12M'

    datesList = pd.date_range(start_date, end_date, freq=freq, inclusive="both")
    

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
      return path + filename
    else:
      return ""

#--------------------------------------------------------------------------#

# Connecting with Database
mydb, mycursor = database.mysql_connector()

"""Retrive Database Tables"""
db_tables = database.retrive_tables(mycursor, "*")

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
@app.route("/Dashboard")
def home():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor, "device", "equipment")
    devices = db_tables["device"]

    # Equipments Counts
    mycursor.execute(""" SELECT 
                    equipment.equipment_name, count(device.`equipment_id`) AS `count`
                    FROM device
                    LEFT JOIN equipment
                    ON device.equipment_id = equipment.equipment_id 
                    GROUP BY equipment.equipment_name""")
    equipments = mycursor.fetchall()

    # Technical Status Counts
    mycursor.execute(""" SELECT 
                    device.technical_status, count(device.technical_status) AS `count` 
                    FROM device 
                    GROUP BY device.technical_status""")
    technicalStatus = mycursor.fetchall()

    # Contract Type Counts
    mycursor.execute(""" SELECT 
                        device.device_contract_type, count(device.device_contract_type) AS `count` 
                        FROM device 
                        GROUP BY device.device_contract_type""")
    contracts = mycursor.fetchall()

    # Inspections Counts
    mycursor.execute(""" SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Inspection" 
    AND year(`scheduled_date`) = year(`done_date`)
    AND month(`scheduled_date`) = month(`done_date`)

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Inspection" 
    AND (year(`scheduled_date`) <= year(`done_date`) AND month(`scheduled_date`) < month(`done_date`))
    OR (year(`scheduled_date`) < year(`done_date`) AND month(`scheduled_date`) <= month(`done_date`))

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Inspection" AND isnull(`done_date`) """)
    Inspections = mycursor.fetchall()
    Inspections = tupleToList(Inspections)
    Inspections[0][0] = "On Time"
    Inspections[1][0] = "Late"
    Inspections[2][0] = "Not Yet"

    # PPMs Counts
    mycursor.execute(""" SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "PPM" 
    AND year(`scheduled_date`) = year(`done_date`)
    AND month(`scheduled_date`) = month(`done_date`)

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "PPM" 
    AND (year(`scheduled_date`) <= year(`done_date`) AND month(`scheduled_date`) < month(`done_date`))
    OR (year(`scheduled_date`) < year(`done_date`) AND month(`scheduled_date`) <= month(`done_date`))

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "PPM" AND isnull(`done_date`) """)
    PPMs = mycursor.fetchall()
    PPMs = tupleToList(PPMs)
    PPMs[0][0] = "On Time"
    PPMs[1][0] = "Late"
    PPMs[2][0] = "Not Yet"

    # Calibrations Counts
    mycursor.execute(""" SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Calibration" 
    AND year(`scheduled_date`) = year(`done_date`)
    AND month(`scheduled_date`) = month(`done_date`)

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Calibration" 
    AND (year(`scheduled_date`) <= year(`done_date`) AND month(`scheduled_date`) < month(`done_date`))
    OR (year(`scheduled_date`) < year(`done_date`) AND month(`scheduled_date`) <= month(`done_date`))

    UNION ALL

    SELECT 
    service_type, count(service.service_type) AS `count` 
    FROM service 
    WHERE `service_type` = "Calibration" AND isnull(`done_date`) """)
    Calibrations = mycursor.fetchall()
    Calibrations = tupleToList(Calibrations)
    Calibrations[0][0] = "On Time"
    Calibrations[1][0] = "Late"
    Calibrations[2][0] = "Not Yet"

    needInspection = len(todaymonthServices("Inspection"))
    needPPM = len(todaymonthServices("PPM"))
    needCalibration = len(todaymonthServices("Calibration"))

    thisMonth = { "needInspection": needInspection,
                  "needCalibration": needCalibration,
                  "needPPM": needPPM }
    
    return render_template("index.html",
                       title="Dashboard",
                       numOfDevices=len(devices),
                       thisMonth=thisMonth,
                       equipmentsList=equipments,
                       technicalStatus=technicalStatus,
                       contracts=contracts,
                       Inspections=Inspections,
                       PPMs=PPMs,
                       Calibrations=Calibrations)
  else:
    return redirect(url_for('login'))

# Add New device
@app.route("/addDevice", methods=['GET', 'POST'])
def addDevice(): 
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor, "model", "location", "equipment", "manufacturer", "settings")

    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    status = -1
    if request.method == 'POST' :
      equipment = request.form['equipment']
      category = request.form['category']
      model = request.form['model']
      manufacturer = request.form['manufacturer']
      sn = request.form['sn']
      prod_date = request.form["prod-date"]
      supp_date = request.form["supp-date"]
      location = request.form['location']
      country = request.form['country']
      image = request.files['image']
      
      contract = request.form['contract-type']
      maintenance_contract_type = request.form['maintenance-contract-type']
      if contract == "Contract of Maintenance":
        contract = contract + " - " + maintenance_contract_type

      contract_start_date = request.form['contract-start-date']
      if contract_start_date == '':
        contract_start_date = None
      contract_end_date = request.form['contract-end-date']
      if contract_end_date == '':
        contract_end_date = None
      
      inspection_list = request.files['inspection-list']
      inspection_freq = request.form['inspection-freq']
      inspection_start_date = request.form['inspection-start-date']
      inspection_end_date = request.form['inspection-end-date']

      ppm_list = request.files['ppm-list']
      ppm_external = request.form.getlist('ppm-external')
      if ppm_external: ppm_external = True 
      else : ppm_external = False
      ppm_freq = request.form['ppm-freq']
      ppm_start_date = request.form['ppm-start-date']
      ppm_end_date = request.form['ppm-end-date']


      calibration_list = request.files['calibration-list']
      calibration_external = request.form.getlist('calibration-external')
      if calibration_external: calibration_external = True 
      else : calibration_external = False
      calibration_freq = request.form['calibration-freq']
      calibration_start_date = request.form['calibration-start-date']
      calibration_end_date = request.form['calibration-end-date']
          
      technical_status = request.form.getlist('technical-status')
      PF_problem = request.form['PF-problem']
      NF_problem = request.form['NF-problem']
      
      problem = ''
      if technical_status == "PF":
        problem = PF_problem
      elif technical_status == "NF":
        problem = NF_problem

      trc = request.form.getlist('trc')

      description = request.form['description']
      description_file = request.files['description-file']

      code = request.form['code']
      qrcode = request.form['qrcode'] ## TODO::QRCode

      createdAt = pd.to_datetime("today")
      createdAt = f"{createdAt.year}-{createdAt.month}-{createdAt.day}"

      #try: 
      # Insert Process
      mycursor.execute('SELECT equipment_id FROM equipment where equipment_name = %s', (equipment,))
      equipment_id = mycursor.fetchone()

      mycursor.execute('SELECT model_id FROM model where model_name = %s', (model,))
      model_id = mycursor.fetchone()

      mycursor.execute('SELECT manufacturer_id FROM manufacturer where manufacturer_name = %s', (manufacturer,))
      manufacturer_id = mycursor.fetchone()

      mycursor.execute('SELECT location_id FROM location where location_name = %s', (location,))
      location_id = mycursor.fetchone()

      image_path = saveFile(image, sn, "image") 
      inspection_path = saveFile(inspection_list, sn, "inspection")      
      ppm_path = saveFile(ppm_list, sn, 'ppm')      
      calibration_path = saveFile(calibration_list, sn, 'calibration')      
      description_path = saveFile(description_file, sn, 'description')

      mycursor.execute("""INSERT INTO device (`device_sn`, `category`,  `equipment_id`, `model_id`, `manufacturer_id`, `device_production_date`, `device_supply_date`, `location_id`, `device_country`, `image`, `device_contract_type`, `contract_start_date`, `contract_end_date`, `terms`, `terms_file`, `inspection_list`, `ppm_list`, `ppm_external`, `calibration_list`, `calibration_external`, `technical_status`, `problem`, `TRC`, `code`, `qrcode`, `createdAt` ,`updatedAt`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                                              (sn, category, equipment_id[0], model_id[0], manufacturer_id[0], prod_date, supp_date, location_id[0], country, image_path, contract, contract_start_date, contract_end_date, description, description_path, inspection_path, ppm_path, ppm_external, calibration_path, calibration_external, technical_status[0], problem, trc[0], code, qrcode, createdAt, None ))

      
      # Inspection
      inspectionsList = getDates(inspection_start_date, inspection_end_date, inspection_freq)
      for date in inspectionsList:
        mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                  ("Inspection", sn, date.date(), None))
      # PPM
      PPMsList = getDates(ppm_start_date, ppm_end_date, ppm_freq)
      for date in PPMsList:
        mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                  ("PPM", sn, date.date(), None))
      # Calibration
      calibrationsList = getDates(calibration_start_date, calibration_end_date, calibration_freq)
      for date in calibrationsList:
        mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                                  ("Calibration", sn, date.date(), None))

      status = 1
      mydb.commit() # Work Is DONE

      # except:
      #   status = 0
      
    return render_template("add.html",
                          title="Add New Device",
                          status=status,
                          equipments=equipments,
                          models=models,
                          locations=locations,
                          manufacturers=manufacturers)
  else:
    return redirect(url_for('login'))

@app.route("/deleteDevice")
def deleteDevice():
  # GET Serial Number from arguments
  sn = argsGet("sn")
  
  # Execute the DELETE Process
  mycursor.execute(f"""DELETE FROM Device WHERE device_sn='{sn}';""")
  mydb.commit() # Work Is DONE

  # Redirect to device page again
  return redirect(url_for('search'))

# Add New device
@app.route("/settings", methods=['GET', 'POST'])
def settings():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor, "model", "location", "equipment", "manufacturer", "settings")
  
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
      statments = request.form['statments']
      statmentsList = statments.split(";")
    
      try:
        # Update Libraries
        for statment in statmentsList:
            mycursor.execute(statment)
        mydb.commit()
        status = 1
        
      except:
        status = 0
    
    db_tables = database.retrive_tables(mycursor, "model", "location", "equipment", "manufacturer")
  
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
  if 'loggedin' in session and session['loggedin'] == True:
    perPage = 10
    startAt = 0
    if request.args.get('page'):
      startAt = int(request.args.get('page')) - 1
    if startAt <= 0:
      startAt = 0
    currpage = startAt*perPage

    searchValue = argsGet('searchValue')

    mycursor.execute(f"""SELECT 
                          device_sn, 
                          equipment_name, 
                          model_name, 
                          manufacturer_name, 
                          device_production_date, 
                          location_name, 
                          device_country, 
                          device_contract_type, 
                          Code
                         FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'
                        LIMIT {currpage},{perPage}""")
    data = mycursor.fetchall()

    mycursor.execute(f"""SELECT COUNT(device_sn)
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    numOfResults = mycursor.fetchone()[0]
    
    mycursor.execute(f"""SELECT DISTINCT `equipment_name` 
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Equipments = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `model_name`
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Models = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `manufacturer_name`
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Manufacturers = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `location_name`
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Locations = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `device_country` FROM `device`
                      LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Countries = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `device_contract_type` FROM `device`
                          LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    Contracts = mycursor.fetchall()

    mycursor.execute(f"""SELECT 
                        MIN(`contract_start_date`), 
                        MAX(`contract_start_date`),
                        MIN(`contract_end_date`), 
                        MAX(`contract_end_date`)
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    contractDates = mycursor.fetchone()

    mycursor.execute(f"""SELECT 
                        MIN(`device_production_date`), 
                        MAX(`device_production_date`),
                        MIN(`device_supply_date`), 
                        MAX(`device_supply_date`)
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    infoDates = mycursor.fetchone()

    mycursor.execute(f"""SELECT DISTINCT `technical_status` FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    TechStatus = mycursor.fetchall()

    mycursor.execute(f"""SELECT DISTINCT `TRC` FROM `device`
                          LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%'""")
    TRCS = mycursor.fetchall()

    if request.method == 'POST' :
      searchValue = request.form['searchValue']
      category = listToStringWithComma('category', 'category')
      equipment = listToStringWithComma('equipment', 'equipment_name')
      model = listToStringWithComma('model', 'model_name')
      manufacturer = listToStringWithComma('manufacturer', 'manufacturer_name')
      
      production_date_start = request.form['production-date-start']
      production_date_end = request.form['production-date-end']
      supply_date_start = request.form['supply-date-start']
      supply_date_end = request.form['supply-date-end']

      location = listToStringWithComma('location', 'location_name')
      country = listToStringWithComma('country', 'device_country')
      contract = listToStringWithComma('contract', 'device_contract_type')

      contract_start_date_start = request.form['contract-start-date-start']
      contract_start_date_end = request.form['contract-start-date-end']
      contract_end_date_start = request.form['contract-end-date-start']
      contract_end_date_end = request.form['contract-end-date-end']

      technical_status = listToStringWithComma('technical-status','technical_status')
      trc = listToStringWithComma('trc','trc')
      

      print(f""" 
          SELECT 
                          device_sn, 
                          equipment_name, 
                          model_name, 
                          manufacturer_name, 
                          device_production_date, 
                          location_name, 
                          device_country, 
                          device_contract_type, 
                          Code
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          (device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%') AND
                          {category}
                          {equipment}
                          {model}
                          {manufacturer}
                          {location}
                          {country}
                          {contract}
                          {technical_status}
                          {trc}
                          device_production_date >= '{production_date_start}' AND device_production_date <= '{production_date_end}' AND
                          device_supply_date >= '{supply_date_start}' AND device_supply_date <= '{supply_date_end}' AND
                          contract_start_date >= '{contract_start_date_start}' AND contract_start_date <= '{contract_start_date_end}' AND
                          contract_end_date >= '{contract_end_date_start}' AND contract_end_date <= '{contract_end_date_end}'""")
      
      mycursor.execute(f"""SELECT 
                          device_sn, 
                          equipment_name, 
                          model_name, 
                          manufacturer_name, 
                          device_production_date, 
                          location_name, 
                          device_country, 
                          device_contract_type, 
                          Code
                        FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          (device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%') AND
                          {category}
                          {equipment}
                          {model}
                          {manufacturer}
                          {location}
                          {country}
                          {contract}
                          {technical_status}
                          {trc}
                          device_production_date >= '{production_date_start}' AND device_production_date <= '{production_date_end}' AND
                          device_supply_date >= '{supply_date_start}' AND device_supply_date <= '{supply_date_end}' AND
                          contract_start_date >= '{contract_start_date_start}' AND contract_start_date <= '{contract_start_date_end}' AND
                          contract_end_date >= '{contract_end_date_start}' AND contract_end_date <= '{contract_end_date_end}'
                        LIMIT {currpage},{perPage}""")
      
      data = mycursor.fetchall()

      mycursor.execute(f"""SELECT COUNT(device_sn) FROM `device`
                        LEFT JOIN equipment
                          ON device.equipment_id = equipment.equipment_id
                        LEFT JOIN model
                          ON device.model_id = model.model_id
                        LEFT JOIN manufacturer
                          ON device.manufacturer_id = manufacturer.manufacturer_id
                        LEFT JOIN location
                          ON device.location_id = location.location_id 
                        WHERE
                          (device_sn LIKE '%{searchValue}%' OR
                          equipment_name LIKE '%{searchValue}%' OR
                          model_name LIKE '%{searchValue}%' OR
                          manufacturer_name LIKE '%{searchValue}%' OR
                          location_name LIKE '%{searchValue}%' OR
                          Code LIKE '%{searchValue}%') AND
                          {category}
                          {equipment}
                          {model}
                          {manufacturer}
                          {location}
                          {country}
                          {contract}
                          {technical_status}
                          {trc}
                          device_production_date >= '{production_date_start}' AND device_production_date <= '{production_date_end}' AND
                          device_supply_date >= '{supply_date_start}' AND device_supply_date <= '{supply_date_end}' AND
                          contract_start_date >= '{contract_start_date_start}' AND contract_start_date <= '{contract_start_date_end}' AND
                          contract_end_date >= '{contract_end_date_start}' AND contract_end_date <= '{contract_end_date_end}'""")
      numOfResults = mycursor.fetchone()[0]

    return render_template("search.html",
                    numOfResults=numOfResults,
                    devices=data,
                    search_value=searchValue,
                    numofPages=math.ceil(numOfResults/perPage),
                    currpage=startAt+1,
                    Equipments=Equipments,
                    Models=Models,
                    Manufacturers=Manufacturers,
                    Locations=Locations,
                    Countries=Countries,
                    Contracts=Contracts,
                    infoDates=infoDates,
                    contractDates=contractDates,
                    TechStatus=TechStatus,
                    TRCS=TRCS)
  else:
    return redirect(url_for('login'))

# Services
@app.route("/services", methods=['GET', 'POST'])
def services():
  if 'loggedin' in session and session['loggedin'] == True:
    perPage = 10
    startAt = 0
    
    if request.args.get('page'):
      startAt = int(request.args.get('page')) - 1

    if startAt <= 0:
      startAt = 0
    currpage = startAt*perPage

    type = argsGet("type")
    sentence = ""
    today = pd.to_datetime("today")

    if type != "":
      sentence = f"WHERE service_type='{type}' AND year(`scheduled_date`)={today.year} AND month(`scheduled_date`)={today.month} AND `done_date` IS NULL"

    mycursor.execute(f"""SELECT * FROM service
                         {sentence}
                         ORDER BY scheduled_date Asc 
                         LIMIT {currpage},{perPage}""")
    data = mycursor.fetchall()

    mycursor.execute(f"""SELECT COUNT(service_id) FROM service {sentence}""")
    numOfResults = mycursor.fetchone()[0]
    print(numOfResults)

    return render_template("services.html",
                          numOfResults=numOfResults,
                          numofPages=int(numOfResults/perPage)+1,
                          services=data,
                          currpage=startAt+1,
                          type=type)
  else:
    return redirect(url_for('login'))

# Device Page
@app.route("/device", methods=['GET', 'POST'])
def device():
  if 'loggedin' in session and session['loggedin'] == True:
    sn = argsGet('sn')
    mycursor.execute("""
    SELECT 
      device_sn, 
      category,
      equipment_name, 
      model_name, 
      manufacturer_name, 
      device_production_date, 
      device_supply_date, 
      location_name, 
      device_country, 
      image,
      device_contract_type, 
      contract_start_date, 
      contract_end_date, 
      terms,
      terms_file, 
      inspection_list, 
      ppm_list, 
      ppm_external,
      calibration_list, 
      calibration_external,
      technical_status, 
      problem, 
      TRC, 
      Code,
      qrCode,
      createdAt, 
      updatedAt  
    FROM device
    left JOIN equipment
    ON device.equipment_id = equipment.equipment_id
    left JOIN model
    ON device.model_id = model.model_id
    left JOIN manufacturer
    ON device.manufacturer_id = manufacturer.manufacturer_id
    left JOIN location
    ON device.location_id = location.location_id    
    WHERE device_sn=%s""",(sn,))

    device = mycursor.fetchone()

    return render_template("device.html",device=device)
  else:
    return redirect(url_for('login'))

# Complete Service
@app.route("/completeService")
def completeService():
  # GET Serial Number from arguments
  id = argsGet("id")
  type = argsGet("type")
  
  today = pd.to_datetime("today")
  print(today.date())
  # Execute the DELETE Process
  mycursor.execute(f"""UPDATE service
                       SET `done_date` = '{today.date()}'
                       WHERE service_id='{id}';""")
  mydb.commit() # Work Is DONE

  # Redirect to device page again
  return redirect(f"/services?type={type}")


# Login
@app.route("/", methods=['GET', 'POST'])
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

# Page 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Run app
if __name__ == "__main__":  
  app.run(debug=True,port=9000)

