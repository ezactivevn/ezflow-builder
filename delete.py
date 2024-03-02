import requests
import mysql.connector
from mysql.connector import Error
import sys
import subprocess
import os


app_id = sys.argv[1]
gcloud_password = sys.argv[2]
customer_email = sys.argv[3]
requester_email = sys.argv[4]

def delete_db(app_id):
    """Delete database"""
    connection = mysql.connector.connect(
        host='35.241.69.119',
        user='ezactive.phu',
        password='wuA7Ms^F%1at',
        auth_plugin='mysql_native_password',
        database = 'ezactive_ezflow'
    )

    cursor = connection.cursor()

    # delete table customer
    cursor.execute("DELETE FROM customer WHERE app_id = '"+app_id+"'")
    connection.commit()
    cursor.close()
    connection.close()

    print("Database deleted")

delete_db(app_id)


def delete_project(app_id, gcloud_password):
    """Delete project"""
    subprocess.run(["sudo", "-S", "rm", "-rf", f"/var/www/html/{app_id}"], input=gcloud_password.encode())

    print(f"Project {app_id} deleted successfully.")


delete_project(app_id, gcloud_password)


def send_email_to_client(email, subject, message):
    """Send email"""
    response = requests.post("https://www.ezactive.com/ezflow/server/admin/user/sendMailToUser",
        {'email': email, 'subject': subject, 'message': message},
        {'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if response is successful
    if response.status_code == 200:
        # Return the response
        # Print response
        response_json = response.json()
        print(response_json)
        # If response is not successful
        if (response_json["status"] == "SUCCESS"):
            # Print response
            return True
        else:
            print(response_json["message"])
            return False
    else:
        # Return None
        return None



email = "vn@ezactive.com"

message = f"Dear {customer_email},<br><br>Your project {app_id} has been deleted.<br><br>Best regards,<br>EZ Active Team"
send_email_to_client( email, "Project Deleted", f"Project {app_id} deleted successfully. Requested by {requester_email}.")
send_email_to_client( customer_email, "Project Deleted", f"Project {app_id} deleted successfully.")
