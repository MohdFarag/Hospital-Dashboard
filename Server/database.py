import mysql.connector

# Connecting with Database
def mysql_connector():

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="01140345493",
    database="almazadb"
)

    # Initialize our cursor
    mycursor = mydb.cursor(buffered=True)

    return mydb, mycursor


# Retrive all data in the database
def retrive_tables(mycursor) :
    AllTables = dict()
    return AllTables