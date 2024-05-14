import sys
import os
import subprocess
import requests
import urllib.request
import shutil
import json
import pusher
import json
from datetime import datetime as dt
import mysql.connector
from mysql.connector import Error


'''
    Element: Argument
    Description: This class is used to store arguments

    Attributes:
        arg1 : project_name
        arg2 : pat_token
        arg3 : firebase_token
        arg4 : username
        arg5 : email
'''
class Pusher:

    def __init__(self, app_id, key, secret, cluster, ssl):
        self.app_id = app_id
        self.key = key
        self.secret = secret
        self.cluster = cluster
        self.ssl = ssl

    def auth(self):
        return pusher.Pusher(app_id=self.app_id, key=self.key, secret=self.secret, cluster=self.cluster, ssl=self.ssl)
    
    def loading(self, app_id, percent, _msg=""):
        self.auth().trigger('manage-customer', 'deploy', {
        'message': 'Finish loading',
        'title': _msg,
        'id': app_id,
        'step' : percent
     }),


my_pusher = Pusher('1764419', 'b82e6e4504e08d436c41', 'd923f53e1b98e0e15948', 'ap1', True)


class Argument:
    project_name = "unknown"
    firebase_token = "unknown"
    pat_token = "unknown"
    username = "unknown"
    email = "unknown"

    def __init__(self, project_name, pat_token="unknown", firebase_token="unknown",  username="unknown", email="unknown"):
        self.project_name = project_name
        self.firebase_token = firebase_token
        self.pat_token = pat_token
        self.username = username
        self.email = email
       

   

# Get arguments
args = Argument("unknown", "unknown", "unknown", "unknown", "unknown")
if len(sys.argv) > 1:
    args = Argument(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])



project_name = args.project_name

print("Project name: ", project_name)

my_pusher.loading(project_name, 5, "getting project info...")



if project_name == "unknown":
    print("Job stopped: Project name is required")
    sys.exit()


class Payment:
    def __init__(self, isValidationRequired, isValidateControl, isTrialRequired, paymentMethod):
        self.isValidationRequired = isValidationRequired
        self.isValidateControl = isValidateControl
        self.isTrialRequired = isTrialRequired
        self.paymentMethod = paymentMethod


class Display:
    def __init__(self, displayField, email):
        self.displayField = displayField
        self.email = email


class Logo:
    def __init__(self, app_logo):
        self.app_logo = app_logo

class MyApp:
    # init
    color_scheme = "#ffff"
    payment = Payment(False, False, False, "Unknown")
    display = Display("Unknown", "Unknown")
    logo = Logo("Unknown")
    app_id = "Unknown"
    app_name = "Unknown"
    sport_type = "Unknown"
    payment_method = "Unknown"

    def __init__(self) -> None:
        pass

    def set_payment(self, isValidationRequired, isValidateControl, isTrialRequired, paymentMethod):
        self.payment = Payment(
            isValidationRequired, isValidateControl, isTrialRequired, paymentMethod)



    def set_display(self, displayField, email):
        self.display = Display(displayField, email)

    def set_logo(self, app_logo):
        self.logo = Logo(app_logo)

    def set_app_info(self, app_id, app_name, sport_type, app_title="Unknown"):
        self.app_id = app_id
        self.app_name = app_name
        self.sport_type = sport_type

    def display_app_info(self):
        # print multiple lines
        print(f"App name: {self.app_name}" + "\n" +
                f"App id: {self.app_id}" + "\n" +
                f"Sport type: {self.sport_type}" + "\n" +
                f"Color scheme: {self.color_scheme}" + "\n" +
                f"Payment: {self.payment.paymentMethod}" + "\n" +
                f"Display: {self.display.displayField}" + "\n" +
                f"Email: {self.display.email}" + "\n" +
                f"Logo: {self.logo.app_logo}" + "\n"
                )
        

    def fetch_data_from_api(self, api_url, data, headers):
        """Fetch data from API"""

        # Fetch data from API
        response = requests.post(api_url, data=data, headers=headers, verify=False)

        # Check if response is successful
        if response.status_code == 200:
            # Return the response
            # Print response
            response_json = response.json()
            print(response_json)
            # If response is not successful
            if (response_json["status"] == "OK"):
                # Print response
                datas = response_json["data"]
                for data in datas:


                    self.set_payment(
                        data["isValidationRequired"],
                        data["isValidateControl"],
                        data["isTrialRequired"],
                        data["paymentMethod"]
                    )

                    self.set_display(
                        data["displayField"],
                        data["email"]
                    )

                    self.color_scheme = data["color_scheme"]

                    self.set_logo(
                        data["app_logo"],
                    )

                    self.set_app_info(
                        data["app_id"],
                        data["app_name"],
                        data["sport_type"],
                    )

                return True
            else:
                print(response_json["message"])
                return False
        else:
            # Return None
            return None

    def send_email_to_client(self, email, subject, message):
        """Send email"""
        response = requests.post("https://www.ezactive.com/ezflow/server/admin/user/sendMailToUser",
                                 {'email': email, 'subject': subject,
                                     'message': message},
                                 {'Content-Type': 'application/x-www-form-urlencoded'}
                                 , verify=False)

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

    def update_customer_info(self, api_url, data, headers):
        """Update customer info"""
        response = requests.post(api_url, data=data, headers=headers)

        # Check if response is successful
        if response.status_code == 200:
            # Return the response
            # Print response
            response_json = response.json()
            print(response_json)
            # If response is not successful
            if (response_json["status"] == "OK"):
                # Print response
                return True
            else:
                print(response_json["message"])
                return False
        else:
            # Return None
            return None

    def create_database(self, db_name):

      
        print ("Current IP: ", requests.get('https://checkip.amazonaws.com').text.strip())
        """Create database"""
        try:
            connection = mysql.connector.connect(
                host='35.241.69.119',
                user='ezactive.phu',
                password='wuA7Ms^F%1at',
                auth_plugin='mysql_native_password'

            )

        except Error as e:
            print("Error while connecting to MySQL", e)

        

        user = f"ezactive.{db_name}"

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS "+db_name)
        cursor.execute("CREATE USER IF NOT EXISTS '"+user+"'@'%' IDENTIFIED BY 'wuA7Ms^F%1at'")
        cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, ALTER, REFERENCES, EXECUTE, CREATE TEMPORARY TABLES, LOCK TABLES ON *.* TO '"+user+"'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        cursor.close()
        connection.close()
        return True

    def delete_database(self, db_name):
        """Delete database"""
        connection = mysql.connector.connect(
            host='35.241.69.119',
            user='ezactive.phu',
            password='wuA7Ms^F%1at',
            auth_plugin='mysql_native_password'

        )
        

        user = f"ezactive.{db_name}"
        '''Delete database'''
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE "+db_name)
        cursor.execute("DROP USER '"+user+"'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        cursor.close()
        connection.close()
        return True
    
    def push_to_github(self, repository, owner, token, path):
        print("path ", path)
        username = owner
        response = requests.get('https://api.github.com/user', auth=(username, token))

        if response.status_code == 200:
            print('Successfully authenticated')
        else:
            print('Error authenticating', response.status_code)
            return False
    
        # Repository details
        repo_name = repository

        # Create repo
        response = requests.post('https://api.github.com/user/repos', auth=(username, token), json={
            'name': repo_name,
            'private': True
        })

        if response.status_code == 201:
            print('Successfully created repository')
            #Get repo url
            repo_url = response.json()['clone_url']

            #Create a new directory
            os.mkdir(repo_name)

            #Copy all files to new directory without .git and repo_name
            shutil.copytree(path, repo_name, ignore=shutil.ignore_patterns('.git', repo_name), dirs_exist_ok=True, copy_function=shutil.copy, ignore_dangling_symlinks=True, symlinks=True)

            #Change directory

            os.chdir(repo_name)

            #set default branch to main
            os.system('git config --global init.defaultBranch main')

            #Initialize git

            os.system('git init')

            #Add all files to git

            os.system('git add .')

            #Commit to git

            os.system('git commit -m "Initial commit"')

            #Add remote origin

            os.system('git remote add origin '+repo_url)

            #Push to git

            os.system('git push -u origin main')

            return repo_url
        
        else:
            print('Error creating repository', json.dumps(response.json(), indent=4))
            return False
    

    def dispatch_workflow(self, owner, repo, workflow_id, branch, app_id, personal_access_token, dispatch_url):
        github_api_url = "https://api.github.com"
        url = f"{github_api_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {personal_access_token}"
        }

        payload = {
            'ref': branch,
            'inputs': {
                'app_id': app_id,
                'repo_url': dispatch_url
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 204:
            print("Successfully dispatched workflow")
            return True
        else:
            print("Error dispatching workflow")
            return False
        
 
class ClientConfig:
    # init
    def __init__(self) -> None:
        pass

    # private method
    def __get_config(self, path):
        with open(path,  'r', encoding='utf-8') as file:
            ts_code = file.read()
            return ts_code

    # public method
    def replace_config(self, path, data, value):
        """Replace config file"""
        # call get_config method
        ts_code = self.__get_config(path)

        # find and replace all data in ts_code
        ts_code = ts_code.replace(data, value)

        # write to file

        with open(path, 'w', encoding='utf-8') as file:
            file.write(ts_code)

        return ts_code

my_pusher.loading(project_name, 10, "Init client config...")
my_app = MyApp()

fetch_data = my_app.fetch_data_from_api("https://www.ezactive.com/ezflow/server/admin/customer/getCustomerByName",
                                        {'app_id': project_name},
                                        {'Content-Type': 'application/x-www-form-urlencoded'})
clientConfig = ClientConfig()
app_config_path = "client/src/app/app-config.ts"
client_enviroment_path = "client/src/environments/environment.prod.ts"
env_path = "server/env.txt"
server_settings_path = "server/base_data/settings.sql"
firebase_path = "client/firebase.json"
init_path = "server/base_data/init.sql"
color_path = "client/src/assets/scss/variables/_variables.scss"
capacitor_path = "client/capacitor.config.ts"
index_path = "client/src/index.html"
supervisor_path = "server/supervisor/laravel-worker.conf"
json_path = "client/dist/build/assets/json/environment.json"

if fetch_data == True:
    # replace config

    def checkJsonPath():
        return os.path.exists(json_path)

    my_pusher.loading(project_name, 15, "Replacing client config...")

    
    # copy app-config.ts to client/src/app
    shutil.copyfile("client/src/app/app-config-copy.txt", app_config_path)

    # copy firebase.json to client
    shutil.copyfile("client/firebase_copy.txt", firebase_path)

    # copy init copy.sql to init.sql
    shutil.copyfile("server/init_copy.txt", init_path)

    # copy environment.prod.ts to client/src/environments
    shutil.copyfile("client/src/environments/environment.prod-copy.txt", client_enviroment_path)

    # copy variables.scss to client/src/assets/scss/variables
    shutil.copyfile("client/src/assets/scss/variables/_variables-copy.txt", color_path)

    # copy capacitor.config.ts to client
    shutil.copyfile("client/capacitor.config-copy.txt", capacitor_path)

    # copy environment.txt to json_path
    if checkJsonPath():
        shutil.copyfile("client/src/assets/json/environment.txt", json_path)

    time_string = dt.now().strftime("%Y%m%d%H%M%S")
    site_id = my_app.app_id+"-"+time_string

    my_logo = my_app.logo.app_logo
    # replace config
    ts_code = clientConfig.replace_config(
        app_config_path, "@@app_id", my_app.app_id)
    ts_code = clientConfig.replace_config(
        app_config_path, "@@app_name", my_app.app_name)
    ts_code = clientConfig.replace_config(
        app_config_path, "@@app_logo", my_logo)
    ts_code = clientConfig.replace_config(
        color_path, "@@color_scheme", my_app.color_scheme)
    ts_code = clientConfig.replace_config(
        env_path, "@@app_id", my_app.app_id)
    ts_code = clientConfig.replace_config(
        env_path, "@@app_name", my_app.app_name)
    ts_code = clientConfig.replace_config(
        env_path, "@@app_email", my_app.display.email)
    ts_code = clientConfig.replace_config(
        env_path, "@@db_host", "database")
    ts_code = clientConfig.replace_config(
        capacitor_path, "@@app_id", my_app.app_id)
    ts_code = clientConfig.replace_config(
        index_path, "@@app_logo", my_logo)

    # init.sql
    ts_code = clientConfig.replace_config(
        init_path, "@@app_id", my_app.app_id)
    # environment.prod.ts
    ts_code = clientConfig.replace_config(
        client_enviroment_path, "@@app_id", my_app.app_id)
    
    ts_code = clientConfig.replace_config(
        supervisor_path, "@@app_id", my_app.app_id)
    
    if checkJsonPath():
        # replace json environment
        ts_code = clientConfig.replace_config(
            json_path, "@@app_id", my_app.app_id)

    display_fields = my_app.display.displayField
    # Parse the JSON data
    data = json.loads(display_fields)

    # Convert it to a string with single backslashes
    string_with_single_backslash = json.dumps(data).replace('"', r'\"')
    ts_code = clientConfig.replace_config(
            server_settings_path, "@@settings", string_with_single_backslash)

    firebase_code = clientConfig.replace_config(
        firebase_path, "@@site-id", site_id)
    image_url = "https://www.ezactive.com/ezflow/images/product/"
    logo_url = image_url+my_logo
    image_path = "client/src/assets/images/logo/"
    urllib.request.urlretrieve(logo_url, image_path+my_logo)
    print("=====================================")

else:
    print("Error")

def run_script(script):
    subprocess.call(script, shell=True)

current_path = os.getcwd()

# generate repository name
repository = my_app.app_id+"-app"+"-"+time_string

run_script('pwd')
run_script('whoami')

firebase_token= "1//0g_6A8LA7OyDACgYIARAAGBASNwF-L9IrfVaLu8CT35gXv33YxIpUKETPED5B45oUmSUA8fZHiJy5zKbD4gm-N_-ecN1jLa8K4Lo"

my_pusher.loading(project_name, 20, "Checking dependencies...")

class FirebaseDeployer:
    dispatch_url = "unknown"
    def __init__(self, firebase_token, site_id):
        self.firebase_token = firebase_token
        self.site_id = site_id

    def check_node_modules(self):
        is_cached = os.path.isdir("client/node_modules")
        is_cached_in_cache = os.path.exists("~/.npm")
        return is_cached and is_cached_in_cache

    def check_firebase_tools(self):
        return os.path.exists("~/.cache/firebase-tools")

    def check_dist_build(self):
        return os.path.exists("client/dist")

    def install_dependencies(self):
        if not self.check_node_modules():
            os.system("cd client && npm install --legacy-peer-deps")

    def install_firebase_tools(self):
        if not self.check_firebase_tools():
            os.system("npm install -g firebase-tools")

    def install_dist_build(self):
        if not self.check_dist_build():
            os.system("cd client && npm run build")

    
    def push_to_github(self, repository, owner, token, path):
        result = my_app.push_to_github(repository, owner, token, path)
                # format is owner/repository
        self.dispatch_url = f"{owner}/{repository}"
    def build_if_needed(self):
            self.install_dependencies()
            self.install_firebase_tools()
            self.install_dist_build()

            
    def build_script(self, command):
        os.system(command)

    def deploy(self):
        my_pusher.loading(project_name, 25, "Installing dependencies...")
        self.build_if_needed()
        my_pusher.loading(project_name, 30, "Building website...")
        os.system(f"cd client && firebase hosting:sites:create {self.site_id} --token {self.firebase_token}")
        my_pusher.loading(project_name , 35, "Deploying website to firebase...")
        os.system(f"cd client && firebase target:apply hosting {self.site_id} {self.site_id} --token {self.firebase_token}")
        os.system(f"cd client && firebase deploy --only hosting:{self.site_id} --token {self.firebase_token}")
        my_pusher.loading(project_name, 40, "Deployed firebase successfully!")

# Example usage:
firebase_token = "1//0g_6A8LA7OyDACgYIARAAGBASNwF-L9IrfVaLu8CT35gXv33YxIpUKETPED5B45oUmSUA8fZHiJy5zKbD4gm-N_-ecN1jLa8K4Lo"
deployer = FirebaseDeployer(firebase_token, site_id)
deployer.deploy()

#update database
my_app.update_customer_info("https://www.ezactive.com/ezflow/server/admin/customer/updateCustomerByAppID",
    {'app_id': project_name, 'app_url': site_id, 'status': '2'},
    {'Content-Type': 'application/x-www-form-urlencoded'}
)

my_pusher.loading(project_name, 50, "Deploying to Github...")

dispatch_url = deployer.dispatch_url 

my_pusher.loading(project_name, 60, "Dispatching to deploy the server...")
# dispatch event
my_app.dispatch_workflow('ezactivevn', 'ezflow-builder', "62452693", "main", my_app.app_id, args.pat_token, dispatch_url)

