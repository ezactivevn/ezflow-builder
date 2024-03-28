from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import json
import sys

app_id = sys.argv[1]


# Path to your JSON key file
credentials = service_account.Credentials.from_service_account_file(
    'firebase_auth.json',
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


url = "https://firebasehosting.googleapis.com/v1beta1/projects/ezactive-ezleague/sites"

# get all sites with access token

result =requests.get(url, headers={"Authorization": "Bearer " + access_token})

print(result.text)

# delete site name 

except_sites = []

# get data from json file
with open('firebase_sites.json') as json_file:
    data = json.load(json_file)

    for site in data['sites']:
        except_sites.append(site['siteId'])


for site in result.json()['sites']:
    site_id = site['name'].split("/")[-1]
    
    if site_id not in except_sites:
        # if site_id string contains app_id
        if app_id in site_id:
            print(f"Deleting site {site_id}")
            url = "https://firebasehosting.googleapis.com/v1beta1/projects/ezactive-ezleague/sites/" + site_id
            result = requests.delete(url, headers={"Authorization": "Bearer " + access_token})
            print(result.text)
    else:
        print("Skip site", site_id)


    


