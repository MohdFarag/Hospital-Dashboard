# Imports
import mysql.connector
from mysql.connector import errorcode
import click
from flask import current_app, g
from flaskr.log import almaza_logger

config = {
    'user': 'root', 
    'password': '01140345493', 
    'host': '127.0.0.1', 
    'port': '3306', 
    'database': 'almazadb'
}

# Connecting with Database
def mysql_connector():
    try:
        g.db = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            almaza_logger.exception("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            almaza_logger.exception("Database does not exist")
        else:
            almaza_logger.exception(err)
        return
    else:
        # Initialize our cursor
        mycursor = g.db.cursor(buffered=True)
        return g.db, mycursor


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    _,mycursor = mysql_connector()

    with current_app.open_resource('schema.sql') as f:
        mycursor.executemany(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

"""Retrive Database Tables"""
def get_tables_data(mycursor, tableName):

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
        AllTables[arg] = get_tables_data(mycursor, arg)

    return AllTables