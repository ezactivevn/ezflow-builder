import sys
import os
import requests
import shutil
import json
import paramiko
from scp import SCPClient


app_id = sys.argv[2]


class MyApp:
    def __init__(self, data):
        self.id = data.get("id")
        self.app_name = data.get("app_name")
        self.app_id = data.get("app_id")
        self.app_logo = data.get("app_logo")
        self.color_scheme = data.get("color_scheme")
        self.sport_type = data.get("sport_type")
        self.is_streaming = bool(int(data.get("is_streaming")))
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
class GCloudCopy:
    def __init__(self, local_file_path, remote_file_path, hostname, port=22, username="mchoang98", private_key_path="./id_rsa", private_key_password="Phulata123"):
        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path
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
    
    def _ensure_remote_path_exists(self, ssh_client):
        sftp = ssh_client.open_sftp()
        try:
            sftp.stat(self.remote_file_path)
        except FileNotFoundError:
            sftp.mkdir(self.remote_file_path)
        sftp.close()

    def copy_to_gcloud(self):
        ssh_client = self._connect_ssh()
        self._ensure_remote_path_exists(ssh_client)
        with SCPClient(ssh_client.get_transport()) as scp:
            print(f"Copying {self.local_file_path} to {self.remote_file_path}")
            if os.path.isdir(self.local_file_path):
                scp.put(self.local_file_path, self.remote_file_path, recursive=True)
            else:
                scp.put(self.local_file_path, self.remote_file_path)
        ssh_client.close()

    
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
    
    result =  fetch_data_from_api(ezflow_url, data, headers)
    return result['data'][0]

def replace_config_filepath(filepath, key, value):
    """ Find string @@key to replace"""

    # Find string @@key to replace

    with open(f"{filepath}", "r", encoding="utf-8") as f:
        content = f.read()
        new_content = content.replace("@@" + key, str(value))
        with open(f"{filepath}", "w", encoding="utf-8") as f:
            f.write(new_content)

    

    
def copy_file_to_cache(file_path, project_dir):
    """Copy file to cache"""
    # if filename contains variables
    if "variables" in file_path:
        # Copy file to cache
        shutil.copy(file_path, f"{project_dir}/client/src/assets/scss/variables/_variables.scss")
    elif "app-config" in file_path:
        shutil.copy(file_path, f"{project_dir}/client/src/app/app-config.ts")
    elif "environment" in file_path:
        shutil.copy(file_path, f"{project_dir}/client/src/environments/environment.prod.ts")
    elif "env.txt" in file_path:
        shutil.copy(file_path, f"{project_dir}/server/.env")
    elif "firebase" in file_path:
        shutil.copy(file_path, f"{project_dir}/client/firebase.json")
    elif "capacitor" in file_path:
        shutil.copy(file_path, f"{project_dir}/client/capacitor.config.ts")
    elif "laravel-worker" in file_path:
        shutil.copy(file_path, f"{project_dir}/server/supervisor/laravel-worker.conf")

def check_node_modules():
        is_cached = os.path.isdir("client/node_modules")
        is_cached_in_cache = os.path.exists("~/.npm")
        return is_cached and is_cached_in_cache

def build_client(cache_dir):
    """Build client"""
    # check node_modules exist
    if not check_node_modules():
        os.system(f"cd {cache_dir}/client && npm install --legacy-peer-deps")
    os.system(f"cd {cache_dir}/client && npm run build")

def main(cache_dir):
    # Get info from ezflow
    data = get_info_from_ezflow(app_id)
    my_app = MyApp(data)
    
    app_info = my_app.get_app_info()
    
    # test_cache_dir = '../ezleague-core/replacefiles/'
    if sys.argv[1] == "test":
        cache_dir = '../ezleague-core/'

    test_cache_dir = f'{cache_dir}/replacefiles/'

    # loop in test_cache_dir
    for filename in os.listdir(test_cache_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(test_cache_dir, filename)
            print("File path: ", file_path)
            for key, value in app_info.__dict__.items():
                print(key, ":", value)  
                replace_config_filepath(file_path, key, value)
                copy_file_to_cache(file_path, cache_dir)

    # copying file to server
    server_dir = f"{cache_dir}/server"
    #loop in server_dir
    for filename in os.listdir(server_dir):
        file_path = os.path.join(server_dir, filename)
        local_file_path = file_path
        remote_file_path = f"/var/www/html/{app_id}"
        hostname = "34.150.91.16"
        username = "mchoang98"
        id_rsa = f"{cache_dir}/id_rsa"
        private_key_password = "Phulata123"
        mycloud = GCloudCopy(local_file_path, remote_file_path, hostname, port=22, username=f"{username}", private_key_path=f"{id_rsa}", private_key_password=f"{private_key_password}")
        try :
            mycloud.copy_to_gcloud()
        except Exception as e:
            print(f"Error: {e}")

    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runscript.py <cache_dir>")
        sys.exit(1)
    cache_dir = sys.argv[1]
    main(cache_dir)
    build_client(cache_dir)

