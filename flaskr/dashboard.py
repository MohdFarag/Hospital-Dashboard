import os
from shutil import rmtree
from werkzeug.utils import secure_filename

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.database import mysql_connector, retrive_tables

import pandas as pd
import math

from flaskr.log import almaza_logger

#--------------------------------------------------------------------------#

bp = Blueprint('dashboard', __name__)

#--------------------------------------------------------------------------#

"""Constants"""
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'webp'])

#--------------------------------------------------------------------------#

"""Functions"""
# Get services of current month
def services_of_current_month(type):
  _,mycursor = mysql_connector()
  today_date = pd.to_datetime("today")

  where_sentence = f"WHERE service_type='{type}' AND year(`scheduled_date`)={today_date.year} AND month(`scheduled_date`)={today_date.month} AND `done_date` IS NULL"
  mycursor.execute(f"""SELECT * FROM service
                        {where_sentence}
                        ORDER BY scheduled_date Asc""")
  data = mycursor.fetchall()

  return data

# Get SQL [IN] sentence for search
def get_sql_for_search(givenName, fieldName):
  given_list = request.form.getlist(givenName)
  output_string = ""

  for item in given_list:
    output_string += f"'{str(item)}'"+","

  if len(given_list) > 0:
    output_string = f"AND `{fieldName}` IN ({output_string[:-1]})"
  else:
    output_string = ""

  return output_string

# Get stat services
def stat_of_services(service_type):
    _,mycursor = mysql_connector()
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

# Check date
def check_date(date_input, name):
  if date_input == '':
      date_input = None

  if date_input != None:
    # Date
    try:
      pd.date_range(date_input, date_input)
    except ValueError as e:
        flash(f"The {name} date is invalid.", "error")
    
  return date_input

# Insert new service into services
def insert_into_service(start_date, end_date, freq, sn, type_of_list):
  _,mycursor = mysql_connector()
  dates = get_dates_in_interval(start_date, end_date, freq)
  for date in dates:
    mycursor.execute("""INSERT INTO `service` (`service_type`, `device_sn`, `scheduled_date`, `done_date`) VALUES (%s, %s, %s, %s)""",
                                              (type_of_list, sn, date.date(), None))

# Check extention of files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Save file
def save_file(list, sn, fileName):
    if list and allowed_file(list.filename):
      filename = secure_filename(fileName + "." + list.filename.rsplit('.', 1)[1])
      path = bp.config['UPLOAD_FOLDER'] + sn.replace("/", "") + "/" 
      os.makedirs(path, exist_ok=True)
      list.save(os.path.join(path, filename))
      return path + filename
    else:
      return ""

# Get dashboard statistics
def get_dashboard_stat(field_name):
  _,mycursor = mysql_connector()
  mycursor.execute(f""" SELECT 
                    device.{field_name}, count(device.{field_name}) AS `count` 
                    FROM device 
                    GROUP BY device.{field_name}""")
  list_stat = mycursor.fetchall()

  return list_stat

# Select Distinct
def select_distinct(search_word, field_name):
    _,mycursor = mysql_connector()
    mycursor.execute(f"""SELECT DISTINCT {field_name}
                      FROM `device`
                      JOIN equipment
                        ON device.equipment_id = equipment.equipment_id
                      JOIN model
                        ON device.model_id = model.model_id
                      JOIN manufacturer
                        ON device.manufacturer_id = manufacturer.manufacturer_id
                      JOIN location
                        ON device.location_id = location.location_id 
                      WHERE
                        device_sn LIKE '%{search_word}%' OR
                        equipment_name LIKE '%{search_word}%' OR
                        model_name LIKE '%{search_word}%' OR
                        manufacturer_name LIKE '%{search_word}%' OR
                        location_name LIKE '%{search_word}%' OR
                        Code LIKE '%{search_word}%'""")
    data = mycursor.fetchall()
    return data

#--------------------------------------------------------------------------#


# Home
@bp.route("/")
@login_required
def Home():
  return redirect(url_for('dashboard.dashboard'))

# Dashboard
@bp.route("/dashboard")
@login_required
def dashboard():
    # Connecting with database
    mydb, mycursor = mysql_connector()
    db_tables = retrive_tables(mycursor, "device", "equipment")
    devices = db_tables["device"]

    # Equipments Counts
    mycursor.execute(f""" SELECT 
                    equipment.equipment_name, count(device.`equipment_id`) AS `count`
                    FROM device
                    LEFT JOIN equipment
                    ON device.equipment_id = equipment.equipment_id 
                    GROUP BY equipment.equipment_name
                    ORDER BY count DESC
                    LIMIT 7""")
    equipments = mycursor.fetchall()
    sum_of_counted_devices = 0
    for equipment in equipments:
      sum_of_counted_devices += equipment[1]
    others_count = len(devices) - sum_of_counted_devices
    other_tuple = ("Others", others_count)
    equipments.append(other_tuple)


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
    
    
    return render_template("dashboard.html",
                       title="Dashboard",
                       num_of_devices=len(devices),
                       this_month=this_month,
                       equipments=equipments,
                       technical_status=technical_status,
                       contracts=contracts,
                       inspections=inspections,
                       ppms=ppms,
                       calibrations=calibrations)

#-----------Devices-----------#

# Add new device
@bp.route("/add-device", methods=['GET', 'POST'])
@login_required
def add_device(): 
    # Connecting with database
    mydb, mycursor = mysql_connector()
    db_tables = retrive_tables(mycursor, "model", "location", "equipment", "manufacturer")

    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    if request.method == 'POST' :
      # Get data from inputs
      sn = request.form['sn']
      sn = sn.replace(" ","")

      equipment = request.form['equipment']
      category = request.form['category']
      model = request.form['model']
      manufacturer = request.form['manufacturer']

      prod_date = request.form["prod-date"]
      prod_date = check_date(prod_date, "production")
      supp_date = request.form["supp-date"]
      supp_date = check_date(supp_date, "supply")
      
      location = request.form['location']
      country = request.form['country'].lower()
      image = request.files['image']
      
      contract = request.form['contract-type']
      maintenance_contract_type = request.form['maintenance-contract-type']
      if contract == "Contract of Maintenance":
        contract = contract + " - " + maintenance_contract_type

      contract_start_date = request.form['contract-start-date']
      contract_start_date = check_date(contract_start_date, "start date of contract")
      contract_end_date = request.form['contract-end-date']
      contract_end_date = check_date(contract_end_date, "end date of contract")
      
      inspection_list = request.files['inspection-list']
      inspection_checklist = request.form['inspection-checklist']

      inspection_freq = request.form['inspection-freq']
      inspection_start_date = request.form['inspection-start-date']
      inspection_start_date = check_date(inspection_start_date, "start date of inspection")
      inspection_end_date = request.form['inspection-end-date']
      inspection_end_date = check_date(inspection_end_date, "end date of inspection")

      ppm_list = request.files['ppm-list']
      ppm_checklist = request.form['ppm-checklist']
      ppm_external = request.form.getlist('ppm-external')
      if ppm_external: ppm_external = True 
      else : ppm_external = False
      ppm_freq = request.form['ppm-freq']
      ppm_start_date = request.form['ppm-start-date']
      ppm_start_date = check_date(ppm_start_date, "start date of ppm")
      ppm_end_date = request.form['ppm-end-date']
      ppm_end_date = check_date(ppm_end_date, "end date of ppm")

      calibration_list = request.files['calibration-list']
      calibration_checklist = request.form['calibration-checklist']
      calibration_external = request.form.getlist('calibration-external')
      if calibration_external: calibration_external = True 
      else : calibration_external = False
      calibration_freq = request.form['calibration-freq']
      calibration_start_date = request.form['calibration-start-date']
      calibration_start_date = check_date(calibration_start_date, "start date of calibration")
      calibration_end_date = request.form['calibration-end-date']
      calibration_end_date = check_date(calibration_end_date, "end date of calibration")
          
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

      # Validation
      # S/N
      mycursor.execute(f"SELECT device_sn FROM device WHERE `device_sn` = '{sn}'")
      sn_exist = mycursor.fetchone()
      if sn_exist:
        flash("The Serial Number is used before!", "error")

      # Insertion Process
      try:
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
        mydb.commit() # Process is done
        flash("Device Added successfully.","info")
        
        almaza_logger.info(f'Succeded to add new device with sn {sn}.')
      except Exception as e:
        almaza_logger.exception('Failed to add new device.')
      
    return render_template("add.html",
                          title="Add New Device",
                          equipments=equipments,
                          models=models,
                          locations=locations,
                          manufacturers=manufacturers)

# Delete device
@bp.route("/delete-device")
@login_required
def delete_device():
    # Connecting with database
    mydb, mycursor = mysql_connector() 
    # GET serial number from arguments
    sn = request.args.get("sn", "")
    
    try:
      # Remove device data
      rmtree(bp.config['UPLOAD_FOLDER'] + sn ,ignore_errors=True)

      # Execute the delete Process
      mycursor.execute(f"""DELETE FROM Device WHERE device_sn='{sn}';""")
      mydb.commit() # Process is done
      almaza_logger.info(f'Device with sn {sn} deleted successfully.')
    
    except Exception as e:
      almaza_logger.exception(f'Failed to deleted device with sn {sn}')
    
    # Redirect to device page again
    return redirect(url_for('dashboard.search'))
  
# Delete device
@bp.route("/delete-devices")
@login_required
def delete_devices():
    try:
      # Connecting with database
      mydb, mycursor = mysql_connector() 

      # Remove device data
      rmtree(bp.config['UPLOAD_FOLDER'] ,ignore_errors=True)

      # Execute the delete Process
      mycursor.execute(f"""DELETE FROM Device;""")
      mydb.commit() # Process is done
      almaza_logger.info(f'All devices deleted successfully.')
    
    except Exception as e:
      almaza_logger.exception(f'Failed to delete all deviecs.')
    
    # Redirect to device page again
    return redirect(url_for('dashboard.search'))
  
# Search On Devices
@bp.route("/search", methods=['GET', 'POST'])
@login_required
def search():   
    # Connecting with database
    mydb, mycursor = mysql_connector() 

    per_page = 10
    starts_at = 0
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1
    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    # Get search Value
    search_word = request.args.get("searchValue", "")

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
                          device_sn LIKE '%{search_word}%' OR
                          equipment_name LIKE '%{search_word}%' OR
                          model_name LIKE '%{search_word}%' OR
                          manufacturer_name LIKE '%{search_word}%' OR
                          location_name LIKE '%{search_word}%' OR
                          Code LIKE '%{search_word}%'
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
                          device_sn LIKE '%{search_word}%' OR
                          equipment_name LIKE '%{search_word}%' OR
                          model_name LIKE '%{search_word}%' OR
                          manufacturer_name LIKE '%{search_word}%' OR
                          location_name LIKE '%{search_word}%' OR
                          Code LIKE '%{search_word}%'""")
    num_of_results = mycursor.fetchone()[0]
    
    equipments = select_distinct(search_word, 'equipment_name')
    models = select_distinct(search_word, 'model_name')
    manufacturers = select_distinct(search_word, 'manufacturer_name')
    locations = select_distinct(search_word, 'location_name')
    countries = select_distinct(search_word, 'device_country')
    contracts = select_distinct(search_word, 'device_contract_type')
    technicals_status = select_distinct(search_word, 'technical_status')
    trcs = select_distinct(search_word, 'TRC')

    # When search
    if request.method == 'POST' :
      search_word = request.form['searchValue']
      category = get_sql_for_search('category', 'category')
      equipment = get_sql_for_search('equipment', 'equipment_name')
      model = get_sql_for_search('model', 'model_name')
      manufacturer = get_sql_for_search('manufacturer', 'manufacturer_name')

      location = get_sql_for_search('location', 'location_name')
      country = get_sql_for_search('country', 'device_country')
      contract = get_sql_for_search('contract', 'device_contract_type')

      technical_status = get_sql_for_search('technical-status','technical_status')
      trc = get_sql_for_search('trc','trc')
      
      print(f"""SELECT 
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
                          (device_sn LIKE '%{search_word}%' OR
                          equipment_name LIKE '%{search_word}%' OR
                          model_name LIKE '%{search_word}%' OR
                          manufacturer_name LIKE '%{search_word}%' OR
                          location_name LIKE '%{search_word}%' OR
                          Code LIKE '%{search_word}%')
                          {category}
                          {equipment}
                          {model}
                          {manufacturer}
                          {location}
                          {country}
                          {contract}
                          {technical_status}
                          {trc}
                        LIMIT {curr_page},{per_page}""")
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
                          (device_sn LIKE '%{search_word}%' OR
                          equipment_name LIKE '%{search_word}%' OR
                          model_name LIKE '%{search_word}%' OR
                          manufacturer_name LIKE '%{search_word}%' OR
                          location_name LIKE '%{search_word}%' OR
                          Code LIKE '%{search_word}%') AND
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
                          (device_sn LIKE '%{search_word}%' OR
                          equipment_name LIKE '%{search_word}%' OR
                          model_name LIKE '%{search_word}%' OR
                          manufacturer_name LIKE '%{search_word}%' OR
                          location_name LIKE '%{search_word}%' OR
                          Code LIKE '%{search_word}%') AND
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
                    search_word=search_word,
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
  
# Device Profile Page
@bp.route("/device", methods=['GET', 'POST'])
@login_required
def device(): 
    # Connecting with database
    mydb, mycursor = mysql_connector() 

    per_page = 10
    starts_at = 0
    
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1

    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    sn = request.args.get("sn", "")
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
  
#-----------Services-----------#

# Services Page
@bp.route("/services", methods=['GET', 'POST'])
@login_required
def services():
    # Connecting with database
    mydb, mycursor = mysql_connector() 

    # Get arguments
    per_page = 10
    starts_at = 0
    
    if request.args.get('page'):
      starts_at = int(request.args.get('page')) - 1

    if starts_at <= 0:
      starts_at = 0
    curr_page = starts_at*per_page

    type = request.args.get("type", "")
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
  
# Delete Service 
@bp.route("/delete-service")
@login_required
def delete_service():
  # Connecting with database
  mydb, mycursor = mysql_connector() 

  # GET Serial Number from arguments
  id = request.args.get("id", "")
  page = request.args.get("page", "")
  type = request.args.get("type", "")
  come = request.args.get("come", "")
  sn = request.args.get("sn", "")
  
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
@bp.route("/complete-service")
@login_required
def complete_service():
    # Connecting with database
    mydb, mycursor = mysql_connector()

    # GET SN & type from arguments
    id = request.args.get("id", "")
    type = request.args.get("type", "")
    come = request.args.get("come", "")
    page = request.args.get("page", "")
    sn = request.args.get("sn", "")

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
  
# Service Order
@bp.route("/service-order")
@login_required
def service_order(): 
    # Connecting with database
    mydb, mycursor = mysql_connector()
  
    # GET sn from arguments
    id = request.args.get("id", "")
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
  
#-----------Settings-----------#

# Settings
@bp.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    # Connecting with database
    mydb, mycursor = mysql_connector()
  
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
          flash("Modifications in libraries changed successfully.", "info")
          almaza_logger.info('Libraries in settings updated successfully.')

        except Exception as e:
          flash("Error !", "error")
          flash(e, "error")
          almaza_logger.exception('Failed to update libraries in settings.')

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
            flash('Admin information updated successfully, logout to update information.', "logininfo")
            almaza_logger.info('Admin information updated successfully')
          else:
            flash("Password you entered is wrong.", "loginerror")
        except Exception as e:
          flash("Failed to update admin information.", "loginerror")
          almaza_logger.exception('Failed to update admin information.')

    db_tables = retrive_tables(mycursor, "model", "location", "equipment", "manufacturer")
  
    # Lists
    models = db_tables['model']
    locations = db_tables['location']
    equipments = db_tables['equipment']
    manufacturers = db_tables['manufacturer']

    return render_template("settings.html", 
                          title="Settings",
                          equipments=equipments,
                          models=models,
                          locations=locations,
                          manufacturers=manufacturers)
  
#-----------Error Handler-----------#

# Page 404
@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# Page 500
@bp.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

