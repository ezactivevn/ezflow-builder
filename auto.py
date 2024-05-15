import sys
import os
import requests
import shutil
import json
import paramiko
from scp import SCPClient
from zipfile import ZipFile


app_id = sys.argv[1]


class MyApp:
    def __init__(self, data):
        self.id = data.get("id")
        self.app_name = data.get("app_name")
        self.app_id = data.get("app_id")
        self.app_logo = data.get("app_logo")
        self.color_scheme = data.get("color_scheme")
        self.sport_type = data.get("sport_type")
        self.is_validation_required = bool(int(data.get("isValidationRequired")))
        self.is_validate_control = bool(int(data.get("isValidateControl")))
        self.is_trial_required = bool(int(data.get("isTrialRequired")))
        self.payment_method = data.get("paymentMethod")
        self.email = data.get("email")
        self.status = bool(int(data.get("status")))
        self.app_url = data.get("app_url")
        self.locked = bool(int(data.get("locked")))
        self.user_id = data.get("user_id")

        fields = data.get("displayField")
        fields_dict = json.loads(fields)
        self.display_field = DisplayField(fields_dict)
        
    def get_app_info(self):
        return self
    def get_display_field(self):
        self.display_field.get_self()
        
# child class from MyApp
class DisplayField:
    def __init__(self, data):
        self.color_scheme = data.get("color_scheme")
        self.sport_type = data.get("sport_type")
        self.app_name = data.get("app_name")
        self.email = data.get("email")
        self.app_id = data.get("app_id")
        self.app_logo = data.get("app_logo")
        self.custom_fields = data.get("custom_fields", [])
        self.custom_fields_default = data.get("custom_fields_default", [])
        self.is_streaming = bool(data.get("is_streaming"))
        self.is_validate_required = bool(data.get("is_validate_required"))
        self.is_trial_required = bool(data.get("is_trial_required"))
        self.is_payment_required = bool(data.get("is_payment_required"))
        self.payment_method = data.get("payment_method")

    def get_self(self):
        return self

# copy Gcloud 
class GCloud:
    def __init__(self, hostname, port=22, username="mchoang98", private_key_path="./id_rsa", private_key_password="Phulata123"):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.private_key_path = private_key_path
        self.private_key_password = private_key_password

    def _load_private_key(self):
        return paramiko.RSAKey.from_private_key_file(self.private_key_path, password=self.private_key_password)

    def _connect_ssh(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            pkey=self._load_private_key(),
            timeout=10
        )
        return ssh_client
    
    def _ensure_remote_path_exists(self, ssh_client, remote_file_path):
        sftp = ssh_client.open_sftp()
        try:
            sftp.stat(remote_file_path)
        except FileNotFoundError:
            sftp.mkdir(remote_file_path)
        sftp.close()

    def copy_to_gcloud(self, local_file_path, remote_file_path):
        ssh_client = self._connect_ssh()
        self._ensure_remote_path_exists(ssh_client, remote_file_path)
        with SCPClient(ssh_client.get_transport()) as scp:
            print(f"Copying {local_file_path} to {remote_file_path}")
            if os.path.isdir(local_file_path):
                scp.put(local_file_path, remote_file_path, recursive=True)
            else:
                scp.put(local_file_path, remote_file_path)
        ssh_client.close()

    def extract_zip(self, remote_file_path, destination_path):
        ssh_client = self._connect_ssh()
        # Ensure that the destination directory exists on the remote server
        ssh_client.exec_command(f"mkdir -p {destination_path}")
        with SCPClient(ssh_client.get_transport()) as scp:
            # Download the zip file from the remote server
            scp.get(remote_file_path, destination_path)
        # Execute unzip command on the remote server
        stdin, stdout, stderr = ssh_client.exec_command(f"unzip {remote_file_path} -d {destination_path}")
        # log the output
        print(stdout.read().decode())
        # Wait for the command to finish
        stdout.channel.recv_exit_status()
        # Close the SSH connection after executing the command
        ssh_client.close()
        print(f"Extracted zip file from {remote_file_path} to {destination_path}")   

    def _replace_config_filepath(filepath, key, value):
        """ Find string @@key to replace"""

        # Find string @@key to replace

        with open(f"{filepath}", "r", encoding="utf-8") as f:
            content = f.read()
            new_content = content.replace("@@" + key, str(value))
            with open(f"{filepath}", "w", encoding="utf-8") as f:
                f.write(new_content)

    def _copy_file_to_cache(file_path, project_dir):
        """Copy file to cache"""
        # if filename contains variables
        if "env.txt" in file_path:
            shutil.copy(file_path, f"{project_dir}/server/.env")
    
    def replace_and_copy_files(self, cache_dir, app_info):
        test_cache_dir = os.path.join(cache_dir, 'replacefiles')

        # loop in test_cache_dir
        for filename in os.listdir(test_cache_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(test_cache_dir, filename)
                print("File path:", file_path)
                for key, value in app_info.__dict__.items():
                    print(key, ":", value)  
                    self._replace_config_filepath(file_path, key, value)
                    self._copy_file_to_cache(file_path, cache_dir)

def fetch_data_from_api(api_url, data, headers):
        """Fetch data from API"""

        # Fetch data from API
        response = requests.post(api_url, data=data, headers=headers)

        # Check if response is successful
        if response.status_code == 200:
            
            response_json = response.json()
            
            return response_json
        else:
            print(response_json["message"])

def get_info_from_ezflow(app_id):
    """Get info from ezflow"""
    ezflow_url = "https://www.ezactive.com/ezflow/server/admin/customer/getCustomerByName"
    data = {
        "app_id": app_id
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    result = fetch_data_from_api(ezflow_url, data, headers)
    return result['data'][0]



def main():
    # Get info from ezflow
    data = get_info_from_ezflow(app_id)
    my_app = MyApp(data)
    app_info = my_app.get_app_info()

    my_cloud = GCloud(
        hostname="34.150.91.16"   
    )
    my_cloud.extract_zip("/var/www/html/server.zip", f"/var/www/html/{app_id}")
    my_cloud.replace_and_copy_files(f"/var/www/html/{app_id}", app_info)

   

if __name__ == "__main__":
    if len(sys.argv) <= 0:
        print("Usage: python runscript.py <cache_dir>")
        sys.exit(1)

    main()
    

