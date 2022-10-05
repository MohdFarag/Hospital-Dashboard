# Imports
import database

import pandas as pd
import math

import os
from shutil import rmtree

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, abort

from log import almaza_logger

#--------------------------------------------------------------------------#

"""Functions"""

# Get services of current month
def services_of_current_month(type):
  today_date = pd.to_datetime("today")

  where_sentence = f"WHERE service_type='{type}' AND year(`scheduled_date`)={today_date.year} AND month(`scheduled_date`)={today_date.month} AND `done_date` IS NULL"
  mycursor.execute(f"""SELECT * FROM service
                        {where_sentence}
                        ORDER BY scheduled_date Asc""")
  data = mycursor.fetchall()

  return data

# Get Request
def get_argument(argName):
  if request.args.get(argName):
    field = request.args.get(argName)
  else:
    field = ""
  
  return field

# Get SQL [IN] sentence for search
def get_sql_for_search(givenName, fieldName):
  given_list = request.form.getlist(givenName)
  output_string = ""

  for item in given_list:
    output_string += f"'{str(item)}'"+","

  if len(given_list) > 0:
    output_string = f"`{fieldName}` IN ({output_string[:-1]}) AND"
  else:
    output_string = ""

  return output_string

# Get stat services
def stat_of_services(service_type):
    mycursor.execute(f""" SELECT 
    service_type, count(service.service_type)
    FROM service
    WHERE `service_type` = "{service_type}" 
    AND year(`scheduled_date`) = year(`done_date`)
    AND month(`scheduled_date`) = month(`done_date`)

    UNION ALL

    SELECT 
    service_type, count(service.service_type)
    FROM service 
    WHERE `service_type` = "{service_type}"
    AND (year(`scheduled_date`) <= year(`done_date`) AND month(`scheduled_date`) < month(`done_date`))
    OR (year(`scheduled_date`) < year(`done_date`) AND month(`scheduled_date`) <= month(`done_date`))

    UNION ALL

    SELECT 
    service_type, count(service.service_type)
    FROM service 
    WHERE `service_type` = "{service_type}" AND isnull(`done_date`) """)
    service_list = mycursor.fetchall()
    
    service_list = list_of_tuples_to_List_of_lists(service_list)
    service_list[0][0] = "On Time"
    service_list[1][0] = "Late"
    service_list[2][0] = "Not Yet"

    return service_list

# List of tuples to list of lists
def list_of_tuples_to_List_of_lists(tuple_objects):
  list_object = list()

  for item in tuple_objects:
    new_list = list(item)
    list_object.append(new_list)

  return list_object

# Get dates in interval given start date and end date with specefic frequency
def get_dates_in_interval(start_date, end_date, freq):
    if(freq == "Monthly"):
        freq = 'M' 
    elif(freq == "3 Months"):
        freq = '3M'
    elif(freq == "6 Months"):
        freq = '6M'
    elif(freq == "Annually"):
        freq = '12M'

    dates_list = pd.date_range(start_date, end_date, freq=freq, inclusive="both")

    return dates_list 

# Check extention of files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_DOC

# Save file
def save_file(list, sn, fileName):
    if list and allowed_file(list.filename):
      filename = secure_filename(fileName + "." + list.filename.rsplit('.', 1)[1])
      path = app.config['UPLOAD_FOLDER'] + sn.replace("/", "") + "/" 
      os.makedirs(path, exist_ok=True)
      list.save(os.path.join(path, filename))
      return path + filename
    else:
      return ""

# Get dashboard statistics
def get_dashboard_stat(field_name):
  mycursor.execute(f""" SELECT 
                    device.{field_name}, count(device.{field_name}) AS `count` 
                    FROM device 
                    GROUP BY device.{field_name}""")
  list_stat = mycursor.fetchall()

  return list_stat

# Insert new service into services
def insert_into_service(start_date, end_date, freq, sn, type_of_list):
  dates = get_dates_in_interval(start_date, end_date, freq)
  for date in dates:
    mycursor.execute(f"""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES 
                                               ({type_of_list}, {sn}, {date.date()}, {None})""")

def select_distinct(searchValue, field_name):
    mycursor.execute(f"""SELECT DISTINCT `{field_name}`
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
    data = mycursor.fetchall()
    return data

#--------------------------------------------------------------------------#

# Connecting with database
mydb, mycursor = database.mysql_connector()

"""Retrive Database Tables"""
try:
  db_tables = database.retrive_tables(mycursor, "*")
  almaza_logger.info('All tables retrieved successfully.')
except Exception as e:
  almaza_logger.info('Field to retrieve all tables.')
  exit()

#--------------------------------------------------------------------------#

"""Our app"""
app = Flask(__name__)
ALLOWED_EXTENSIONS_DOC = set(['pdf', 'png', 'jpg', 'jpeg', 'webp'])

# Configuration
app.config.from_object('config.Config')

# Using a development configuration
app.config.from_object('config.DevConfig')
## Using a production configuration
# app.config.from_object('config.ProdConfig')

almaza_logger.info('Settings are setted successfully.')

#--------------------------------------------------------------------------#

""" Routes of Pages """
# Dashboard
@app.route("/dashboard")
def dashboard():
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor, "device", "equipment")
    devices = db_tables["device"]

    # Equipments Counts
    mycursor.execute(f""" SELECT 
                    equipment.equipment_name, count(device.`equipment_id`) AS `count`
                    FROM device
                    LEFT JOIN equipment
                    ON device.equipment_id = equipment.equipment_id 
                    GROUP BY equipment.equipment_name""")
    equipments = mycursor.fetchall()
    technical_status = get_dashboard_stat("technical_status")
    contracts = get_dashboard_stat("device_contract_type")

    # Inspections Counts
    inspections = stat_of_services('inspection')
    # PPMs Counts
    ppms = stat_of_services('ppm')
    # Calibrations Counts
    calibrations = stat_of_services("calibration")

    need_inspection = len(services_of_current_month("Inspection"))
    need_ppm = len(services_of_current_month("PPM"))
    need_calibration = len(services_of_current_month("Calibration"))

    this_month = {  "need_inspection": need_inspection,
                    "need_ppm": need_ppm,
                    "need_calibration": need_calibration }
    
    
    return render_template("index.html",
                       title="Dashboard",
                       num_of_devices=len(devices),
                       this_month=this_month,
                       equipments=equipments,
                       technical_status=technical_status,
                       contracts=contracts,
                       inspections=inspections,
                       ppms=ppms,
                       calibrations=calibrations)
  else:
    return redirect(url_for('login'))

#-----------Devices-----------#

# Add new device
@app.route("/add-device", methods=['GET', 'POST'])
def add_device(): 
  if 'loggedin' in session and session['loggedin'] == True:
    db_tables = database.retrive_tables(mycursor, "model", "location", "equipment", "manufacturer")

    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    status = -1
    if request.method == 'POST' :
      # Get data from inputs
      sn = request.form['sn']
      sn = sn.replace(" ","")
      equipment = request.form['equipment']
      category = request.form['category']
      model = request.form['model']
      manufacturer = request.form['manufacturer']

      prod_date = request.form["prod-date"]
      if prod_date == '':
        prod_date = None
      supp_date = request.form["supp-date"]
      if supp_date == '':
        supp_date = None
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
      inspection_checklist = request.form['inspection-checklist']

      inspection_freq = request.form['inspection-freq']
      inspection_start_date = request.form['inspection-start-date']
      inspection_end_date = request.form['inspection-end-date']

      ppm_list = request.files['ppm-list']
      ppm_checklist = request.form['ppm-checklist']
      ppm_external = request.form.getlist('ppm-external')
      if ppm_external: ppm_external = True 
      else : ppm_external = False
      ppm_freq = request.form['ppm-freq']
      ppm_start_date = request.form['ppm-start-date']
      ppm_end_date = request.form['ppm-end-date']


      calibration_list = request.files['calibration-list']
      calibration_checklist = request.form['calibration-checklist']
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
      qrcode = request.form['qrcode']

      createdAt = pd.to_datetime("today")
      createdAt = f"{createdAt.year}-{createdAt.month}-{createdAt.day}"

      try:
        # Insertion Process

        # 1) Get id of equipment_name chosen
        mycursor.execute('SELECT equipment_id FROM equipment where equipment_name = %s', (equipment,))
        equipment_id = mycursor.fetchone()

        # 2) Get id of model_name chosen
        mycursor.execute('SELECT model_id FROM model where model_name = %s', (model,))
        model_id = mycursor.fetchone()

        # 3) Get id of manufacturer_id chosen
        mycursor.execute('SELECT manufacturer_id FROM manufacturer where manufacturer_name = %s', (manufacturer,))
        manufacturer_id = mycursor.fetchone()

        # 4) Get id of location_id chosen
        mycursor.execute('SELECT location_id FROM location where location_name = %s', (location,))
        location_id = mycursor.fetchone()

        # 5) Save files
        image_path = save_file(image, sn, "image")
        inspection_path = save_file(inspection_list, sn, "inspection")      
        ppm_path = save_file(ppm_list, sn, 'ppm')
        calibration_path = save_file(calibration_list, sn, 'calibration')      
        description_path = save_file(description_file, sn, 'description')

        # 6) Add the device
        mycursor.execute("""INSERT INTO device (`device_sn`, `category`, `equipment_id`, `model_id`, `manufacturer_id`, `device_production_date`, `device_supply_date`, `location_id`, `device_country`, `image`, `device_contract_type`, `contract_start_date`, `contract_end_date`, `terms`, `terms_file`, `inspection_list`, `inspection_checklist`, `ppm_list`, `ppm_checklist`, `ppm_external`, `calibration_list`, `calibration_checklist`, `calibration_external`, `technical_status`, `problem`, `TRC`, `code`, `qrcode`, `createdAt`, `updatedAt`) VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (sn,category,equipment_id[0],model_id[0],manufacturer_id[0],prod_date,supp_date,location_id[0],country,image_path,contract,contract_start_date,contract_end_date,description,description_path,inspection_path,inspection_checklist,ppm_path,ppm_checklist,ppm_external,calibration_path,calibration_checklist,calibration_external,technical_status[0],problem,trc[0],code,qrcode,createdAt,None))

        
        # 7) Add services of the device
        # Inspection
        insert_into_service(inspection_start_date, inspection_end_date, inspection_freq, sn, "Inspection")
        # PPM
        insert_into_service(ppm_start_date, ppm_end_date, ppm_freq, sn, "PPM")
        # Calibration
        insert_into_service(calibration_start_date, calibration_end_date, calibration_freq, sn, "Calibration")

        status = 1
        mydb.commit() # Process is done
        almaza_logger.info(f'succeded to add new device with sn {sn}.')

      except Exception as e:
        almaza_logger.exception('Failed to add new device.')
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

# Delete device
@app.route("/delete-device")
def delete_device():
  if 'loggedin' in session and session['loggedin'] == True:
    # GET serial number from arguments
    sn = get_argument("sn")
    
    try:
      # Remove device data
      rmtree(app.config['UPLOAD_FOLDER'] + sn ,ignore_errors=True)

      # Execute the delete Process
      mycursor.execute(f"""DELETE FROM Device WHERE device_sn='{sn}';""")
      mydb.commit() # Process is done
      almaza_logger.info(f'Device with sn {sn} deleted successfully.')
    
    except Exception as e:
      almaza_logger.exception(f'Failed to deleted device with sn {sn}')
    
    # Redirect to device page again
    return redirect(url_for('search'))
  else:
    return redirect(url_for('login'))

# Search On Devices
@app.route("/search", methods=['GET', 'POST'])
def search(): 
  if 'loggedin' in session and session['loggedin'] == True:
    per_page = 10
    starts_at = 0
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1
    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    # Get search Value
    searchValue = get_argument('searchValue')

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
                        LIMIT {curr_page},{per_page}""")
    data = mycursor.fetchall()

    # Count the data
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
    num_of_results = mycursor.fetchone()[0]
    
    equipments = select_distinct(searchValue, 'equipment_name')
    models = select_distinct(searchValue, 'model_name')
    manufacturers = select_distinct(searchValue, 'manufacturer_name')
    locations = select_distinct(searchValue, 'location_name')
    countries = select_distinct(searchValue, 'device_country')
    contracts = select_distinct(searchValue, 'device_contract_type')
    technicals_status = select_distinct(searchValue, 'technical_status')
    trcs = select_distinct(searchValue, 'TRC')

    # When search
    if request.method == 'POST' :
      searchValue = request.form['searchValue']
      category = get_sql_for_search('category', 'category')
      equipment = get_sql_for_search('equipment', 'equipment_name')
      model = get_sql_for_search('model', 'model_name')
      manufacturer = get_sql_for_search('manufacturer', 'manufacturer_name')

      location = get_sql_for_search('location', 'location_name')
      country = get_sql_for_search('country', 'device_country')
      contract = get_sql_for_search('contract', 'device_contract_type')

      technical_status = get_sql_for_search('technical-status','technical_status')
      trc = get_sql_for_search('trc','trc')
      
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
                          {trc[:-3]}
                        LIMIT {curr_page},{per_page}""")
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
                          {trc[:-3]}""")
      num_of_results = mycursor.fetchone()[0]

    return render_template("search.html",
                    title="Devices",
                    num_of_results=num_of_results,
                    devices=data,
                    search_value=searchValue,
                    num_of_pages=math.ceil(num_of_results/per_page),
                    curr_page=starts_at+1,
                    equipments=equipments,
                    models=models,
                    manufacturers=manufacturers,
                    locations=locations,
                    countries=countries,
                    contracts=contracts,
                    technicals_status=technicals_status,
                    trcs=trcs)
  else:
    return redirect(url_for('login'))

# Device Profile Page
@app.route("/device", methods=['GET', 'POST'])
def device():
  if 'loggedin' in session and session['loggedin'] == True:
    per_page = 10
    starts_at = 0
    
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1

    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    sn = get_argument('sn')
    mycursor.execute("""SELECT 
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
      inspection_checklist, 
      ppm_list, 
      ppm_checklist,
      ppm_external,
      calibration_list,
      calibration_checklist, 
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

    # If serial number is false flow error
    if device == None:
      abort(404, description="Resource not found")

    mycursor.execute(f"SELECT * FROM service WHERE device_sn='{sn}' ORDER BY scheduled_date Asc LIMIT {curr_page},{per_page} ")
    services = mycursor.fetchall()

    mycursor.execute(f"SELECT COUNT(service_id) FROM service WHERE device_sn='{sn}'")
    num_of_results = mycursor.fetchone()[0]

    title = device[0]
    return render_template("device.html",
                            title=title,
                            services=services,
                            device=device,
                            num_of_results=num_of_results,
                            num_of_pages=int(num_of_results/per_page)+1,
                            curr_page=starts_at+1,)
  else:
    return redirect(url_for('login'))

#-----------Services-----------#

# Services Page
@app.route("/services", methods=['GET', 'POST'])
def services():
  if 'loggedin' in session and session['loggedin'] == True:
    per_page = 10
    starts_at = 0
    
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1

    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    type = get_argument("type")
    sentence = ""
    today = pd.to_datetime("today")

    if type != "":
      sentence = f"WHERE service_type='{type}' AND year(`scheduled_date`)={today.year} AND month(`scheduled_date`)={today.month} AND `done_date` IS NULL"

    mycursor.execute(f"""SELECT * FROM service
                         {sentence}
                         ORDER BY scheduled_date Asc 
                         LIMIT {curr_page},{per_page}""")
    data = mycursor.fetchall()

    mycursor.execute(f"""SELECT COUNT(service_id) FROM service {sentence}""")
    num_of_results = mycursor.fetchone()[0]

    return render_template("services.html",
                          title="Services",
                          num_of_results=num_of_results,
                          num_of_pages=int(num_of_results/per_page)+1,
                          services=data,
                          curr_page=starts_at+1,
                          type=type)
  else:
    return redirect(url_for('login'))

# Delete Service 
@app.route("/delete-service")
def delete_service():
  # GET Serial Number from arguments
  id = get_argument("id")
  page = get_argument("page") 
  type = get_argument("type")
  come = get_argument("come")
  sn = get_argument("sn")
  
  # Execute the DELETE process
  try:
    mycursor.execute(f"""DELETE FROM service WHERE service_id='{id}';""")
    mydb.commit() # Process is done
    almaza_logger.info(f'Service with sn {id} deleted successfully.')
    
  except Exception as e:
    almaza_logger.exception(f'Failed to delete service with sn {id}')

  if come == 'device':
    # Redirect to device page again
    return redirect(f"/device?page={page}&sn={sn}#services")
  elif come == 'services':
    # Redirect to services page again
    return redirect(f"/services?page={page}&type={type}")
    
# Complete Service
@app.route("/complete-service")
def complete_service():
  if 'loggedin' in session and session['loggedin'] == True:
    # GET sn&type from arguments
    id = get_argument("id")
    type = get_argument("type")
    come = get_argument("come")
    page = get_argument("page")
    sn = get_argument("sn")

    today = pd.to_datetime("today")

    # Execute the DELETE Process
    try:
      mycursor.execute(f"""UPDATE service
                          SET `done_date` = '{today.date()}'
                          WHERE service_id='{id}';""")
      mydb.commit() # Process is done
      almaza_logger.info(f'Service with sn {id} completed successfully.')
    
    except Exception as e:
      almaza_logger.exception(f'Failed to complete service with sn {id}')
      
    if come == 'device':
      # Redirect to page page again
      return redirect(f"/device?page={page}&sn={sn}#services")
    elif come == 'services':
    # Redirect to services page again
      return redirect(f"/services?page={page}&type={type}")

    # Redirect to device page again
    return redirect(f"/services?type={type}")
  else:
    return redirect(url_for('login'))

# Service Order
@app.route("/service-order")
def service_order():
  if 'loggedin' in session and session['loggedin'] == True:
    # GET sn from arguments
    id = get_argument("id")
    mycursor.execute(f"""SELECT service_id,
                                service_type,
                                service.device_sn
                                scheduled_date,
                                equipment_name,
                                model_name,
                                manufacturer_name,
                                device_production_date,
                                device_supply_date,
                                location_name,
                                device_contract_type,
                                contract_start_date,
                                contract_end_date,
                                inspection_list,
                                inspection_checklist, 
                                ppm_list, 
                                ppm_checklist,
                                calibration_list,
                                calibration_checklist, 
                                technical_status,
                                TRC,
                                Code,
                                qrcode
                         FROM service
                         left Join device 
                         on service.device_sn = device.device_sn
                         Join equipment 
                         on device.equipment_id = equipment.equipment_id
                         Join model 
                         on device.model_id = model.model_id
                         Join manufacturer 
                         on device.manufacturer_id = manufacturer.manufacturer_id 
                         Join location 
                         on device.location_id = location.location_id 
                         Where service_id={id}""")
    service = mycursor.fetchone()
    if service == None:
      abort(404, description="Resource not found")

    today = pd.to_datetime("today")
    return render_template("serviceOrder.html",
                            title="Service Order",
                            service=service,
                            today=today)
  else:
    return redirect(url_for('login'))

#-----------Settings-----------#

# Settings
@app.route("/settings", methods=['GET', 'POST'])
def settings():
  if 'loggedin' in session and session['loggedin'] == True:
    status = -1 # Default
    if request.method == 'POST' :
      if request.form['settings'] == 'SAVE':   
        # Insert equipments
        statments = request.form['statments']
        statmentsList = statments.split(";")

        try:
          # Update Libraries
          for statment in statmentsList:
            mycursor.execute(statment)
            mydb.commit()
          
          status = 1
          almaza_logger.info('Libraries in settings updated successfully.')

        except Exception as e:
          almaza_logger.exception('Failed to update libraries in settings.')
          status = 0


      elif request.form['settings'] == 'CHANGE':
        username = request.form['username']
        old_password = request.form['old-password']
        password = request.form['password']
        try:
          # Check if account exists using MySQL
          mycursor.execute(f"SELECT * FROM admin WHERE `passwd` = '{old_password}'")
          # Fetch one record and return result
          account = mycursor.fetchone()
          if account :
            # Update information
            mycursor.execute(f"""UPDATE `admin` SET username='{username}', passwd='{password}' WHERE admin_id=0""")
            mydb.commit()
            
            status = 1
            almaza_logger.info('Admin information updated successfully.')

            return redirect(url_for('logout'))
          else:
            status = 0

        except Exception as e:
          almaza_logger.exception('Failed to update admin information.')
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
                          manufacturers=manufacturers)
  else:
    return redirect(url_for('login'))

#-----------Login & Logout-----------#

# Login
@app.route("/", methods=['GET', 'POST'])
def login():
  if 'loggedin' in session and session['loggedin'] == True:
    return redirect(url_for('dashboard'))
  else:
    status = True
    if request.method == 'POST':
      username  = request.form['username']
      password  = request.form['password']

      # Check if account exists using MySQL
      mycursor.execute(f"SELECT * FROM admin WHERE `username` = '{username}' AND `passwd` = '{password}'")

      # Fetch one record and return result
      account = mycursor.fetchone()

      # If account exists in accounts table in out database
      if account:
          # Create session data, we can access this data in other routes
          session['loggedin'] = True
          session['id'] = account[0]
          session['username'] = account[1]
          status = True
          # Redirect to dashboard page
          return redirect(url_for('dashboard'))
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

#-----------Error Handler-----------#

# Page 404
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Page 500
@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

#--------------------------------------------------------------------------#

#-----------__main__-----------#

# Run the app in debug mode
if __name__ == "__main__":  
  app.run(debug=True,port=9000)

