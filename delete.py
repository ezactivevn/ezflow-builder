import requests
import mysql.connector
from mysql.connector import Error
import sys
import subprocess
import os
import pusher


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
    cursor.execute("DELETE FROM customers WHERE app_id = '"+app_id+"'")
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

def rm_alias_in_apache_config(config_file_path, alias_path):
    password = gcloud_password

    # Grant write permissions to the config file
    subprocess.run(f"echo '{password}' | sudo -S chmod +w {config_file_path}", shell=True, check=True)

    # Remove the specified alias and its related lines
    command = (
        f"echo '{password}' | sudo -S sed -i '/# {alias_path} begin/,/# {alias_path} end/d' {config_file_path}"
    )
    subprocess.run(command, shell=True, check=True)

    # Revoke write permissions from the config file
    subprocess.run(f"echo '{password}' | sudo -S chmod -w {config_file_path}", shell=True, check=True)

rm_alias_in_apache_config("/etc/apache2/sites-available/.conf", f"/{app_id}")



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


pusher_client = pusher.Pusher(
        app_id='1764419',
        key='b82e6e4504e08d436c41',
        secret='d923f53e1b98e0e15948',
        cluster='ap1',
        ssl=True
        )

pusher_client.trigger('manage-customer', 'finish-delete', {
    'message': f"Project {app_id} deleted successfully. Requested by {requester_email}.",
    })