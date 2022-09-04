import mysql.connector

# Connecting with Database
def mysql_connector():

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="01140345493",
    database="almazadb"
    )
    print("Connected to database..")

    # Initialize our cursor
    mycursor = mydb.cursor(buffered=True)

    return mydb, mycursor


"""Retrive Database Tables"""

def admin(mycursor) :
    'Retrieve all admin data'
    mycursor.execute("SELECT * FROM admin")
    table = mycursor.fetchall()

    return table

def device(mycursor) :
    'Retrieve all device data'
    mycursor.execute("SELECT * FROM device")
    table = mycursor.fetchall()

    return table

def equipment(mycursor) :
    'Retrieve all equipment data'
    mycursor.execute("SELECT * FROM equipment")
    table = mycursor.fetchall()

    return table

def location(mycursor) :
    'Retrieve all location data'
    mycursor.execute("SELECT * FROM location")
    table = mycursor.fetchall()

    return table

def manufacturer(mycursor) :
    'Retrieve all manufacturer data'
    mycursor.execute("SELECT * FROM manufacturer")
    table = mycursor.fetchall()

    return table

def model(mycursor) :
    'Retrieve all model data'
    mycursor.execute("SELECT * FROM model")
    table = mycursor.fetchall()

    return table

def service(mycursor) :
    'Retrieve all service data'
    mycursor.execute("SELECT * FROM service")
    table = mycursor.fetchall()

    return table


# Retrive all data in the database
def retrive_tables(mycursor) :
    AllTables = dict()
    AllTables["admin"] = admin(mycursor)
    AllTables["device"] = device(mycursor)
    AllTables["equipment"] = equipment(mycursor)
    AllTables["location"] = location(mycursor)
    AllTables["manufacturer"] = manufacturer(mycursor)
    AllTables["model"] = model(mycursor)
    AllTables["service"] = service(mycursor)

    return AllTables