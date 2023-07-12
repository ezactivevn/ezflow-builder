import requests
import mysql.connector
from mysql.connector import Error
import sys


app_name = sys.argv[1]
status = sys.argv[2]

def update_db(app_name):
    """Update database"""
    connection = mysql.connector.connect(
        host='35.241.69.119',
        user='ezactive.phu',
        password='wuA7Ms^F%1at',
        auth_plugin='mysql_native_password',
        database = 'ezactive_ezflow'
    )

    cursor = connection.cursor()

    # update table customer field status
    cursor.execute("UPDATE customer SET status = 0 WHERE app_name = '"+app_name+"'")
    connection.commit()
    cursor.close()
    connection.close()

    print("Database updated")

update_db(app_name)

    


    
