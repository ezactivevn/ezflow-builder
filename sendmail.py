import requests
import pusher
import sys


app_name = sys.argv[1]
status = sys.argv[2]

response = requests.post("https://www.ezactive.com/ezflow/server/admin/customer/updateCustomerByAppID", {'app_id': app_name, 'status': status})


pusher_client = pusher.Pusher(
        app_id='1764419',
        key='b82e6e4504e08d436c41',
        secret='d923f53e1b98e0e15948',
        cluster='ap1',
        ssl=True
        )

pusher_client.trigger('manage-customer', 'warning-update', {
    'message': f"Project {app_name} cannot be build. Failed to deploy. Please try again.",
    })

    


    
