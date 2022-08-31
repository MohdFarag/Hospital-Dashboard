import mysql.connector

# Connecting with Database
def mysql_connector():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="01140345493",
    database="stomology-dep",
    auth_plugin='mysql_native_password'
)

    # Initialize our cursor
    mycursor = mydb.cursor(buffered=True)

    return mydb, mycursor
