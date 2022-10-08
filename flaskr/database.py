# Imports
import mysql.connector
from log import almaza_logger

# Constants of DB
HOST = "localhost"
USER = "root"
PASSWD = "01140345493"
DATABASE = "almazadb"

# Connecting with Database
def mysql_connector():
    try:
        mydb = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            database=DATABASE
        )
        almaza_logger.info('Server connected to database successfully.')

    except Exception as e:
        almaza_logger.exception('Server Failed to connect to database.')

    # Initialize our cursor
    mycursor = mydb.cursor(buffered=True)

    return mydb, mycursor

"""Retrive Database Tables"""
def getTableData(mycursor, tableName):

    'Retrieve all table data'

    if tableName == "device" :
        table = device(mycursor)
    elif tableName == "model" :
        table = model(mycursor)
    elif tableName == "service" :
        table = service(mycursor)
    else: 
        mycursor.execute("SELECT * FROM "+ tableName)
        table = mycursor.fetchall()

    return table
    
def device(mycursor) :
    'Retrieve all device data'

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
    ON device.location_id = location.location_id""")
    table = mycursor.fetchall()

    return table

def model(mycursor) :
    'Retrieve all model data'
    mycursor.execute("""SELECT model_id, model_name, equipment_name 
                    FROM model 
                    left JOIN equipment
                    ON model.equipment_id=equipment.equipment_id
                    """)
    modelTable = mycursor.fetchall()
    return modelTable

def service(mycursor) :
    'Retrieve all service data'
    mycursor.execute("SELECT * FROM service")
    table = mycursor.fetchall()

    return table

# Retrive all data in the database
def retrive_tables(mycursor, *args) :

    ## TODO::AUTOMATIC select to tables
    AllTables = dict()
    if "*" in args:
        args = ["admin", "device", "equipment", "location", "manufacturer", "model", "service"]
    
    for arg in args:
        AllTables[arg] = getTableData(mycursor, arg)

    return AllTables