import requests
import sys

version = sys.argv[1]

response = requests.post("https://www.ezactive.com/ezflow/server/admin/version/updateVersion", {'version': version})

# decode response
response = response.json()

if response["status"] == "OK":
    print(response["message"])
else:
    print(response["message"])

