import sys
import os
import requests
import shutil
import json

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

def build_client(cache_dir):
    """Build client"""
    # check node_modules exist
    if not os.path.exists(f"{cache_dir}/client/node_modules"):
        os.system(f"cd {cache_dir}/client && npm install")
    os.system(f"cd {cache_dir}/client && npm run build")

def main(cache_dir):
    # Get info from ezflow
    data = get_info_from_ezflow(app_id)
    my_app = MyApp(data)
    
    app_info = my_app.get_app_info()
    
    # test_cache_dir = '../ezleague-core/replacefiles/'
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


    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runscript.py <cache_dir>")
        sys.exit(1)
    cache_dir = sys.argv[1]
    main(cache_dir)
    build_client(cache_dir)

