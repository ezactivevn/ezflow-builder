import pusher
import time
import os

# Initialize Pusher client
pusher_client = pusher.Pusher(
    app_id='1764419',
    key='b82e6e4504e08d436c41',
    secret='d923f53e1b98e0e15948',
    cluster='ap1',
    ssl=True
)

# Get duration from environment variable, default to 300 seconds (5 minutes)
duration = int(os.getenv('TIMER_DURATION', 300))

# Get app_id from environment variable
app_id = os.getenv('APP_ID', 'default_app_id')
    
start_time = time.time()

while (time.time() - start_time) < duration:
    pusher_client.trigger('manage-customer', 'deploy', 
        {
        'message': 'Finish loading',
        'title': "Build App...",
        'id': app_id
     })
    time.sleep(3)
