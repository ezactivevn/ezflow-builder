import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import json

# Path to your JSON key file from the environment variable
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Load the credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=[
        'https://www.googleapis.com/auth/firebase.hosting',
    ]
)

# Request a token
request = Request()
credentials.refresh(request)

# Get the access token
access_token = credentials.token
print("Bearer token:", access_token)

url = "https://www.ezactive.com/ezflow/server/admin/customer/getAllCustomers"

result = requests.get(url)
# parse json
json_string = json.loads(result.text)
data = json_string["data"]

except_sites = []

for customer in data:
    except_sites.append(customer["app_url"])

print(except_sites)

url = "https://firebasehosting.googleapis.com/v1beta1/projects/ezactive-ezleague/sites"

# get all sites with access token
result = requests.get(url, headers={"Authorization": "Bearer " + access_token})

print("result", result.json())

for site in result.json()['sites']:
    site_id = site['name'].split("/")[-1]

    if site_id not in except_sites:
        print(f"Deleting site {site_id}")
        url = f"https://firebasehosting.googleapis.com/v1beta1/projects/ezactive-ezleague/sites/{site_id}"
        result = requests.delete(url, headers={"Authorization": "Bearer " + access_token})
        print(result.text)
    else:
        print("Skip site", site_id)
