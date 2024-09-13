import requests
import json 
import sys
import datetime
import pusher

app_id = sys.argv[1]
status = sys.argv[2] # 1 or 0
side = sys.argv[3] # "server" or "client"


def send_slack_message(token, channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel,
        "text": message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message. Error:", response.text)

# Set your Slack API token
slack_token = "xoxb-4295555892247-7210217828135-jsHe9qsykoAn3jg1EvhaY3sx"
# Set the channel where you want to send the message (e.g., "#general")
slack_channel = "#ezflow"
# Set the message you want to send
success = "SUCCESS" if status == "1" else "FAIL"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fun_text = f":smile::smile::smile: \n Project *{app_id}* has been build *{success}* on *{sys.argv[3]}* at *{now}*"
sad_text = f":sob::sob::sob: \n Project *{app_id}* has been build *{success}* on *{sys.argv[3]}* at *{now}*"

message_text = fun_text if status == "1" else sad_text
# Call the function to send the message
send_slack_message(slack_token, slack_channel, message_text)


pusher_client = pusher.Pusher(
        app_id='1764419',
        key='b82e6e4504e08d436c41',
        secret='d923f53e1b98e0e15948',
        cluster='ap1',
        ssl=True
        )

pusher_client.trigger('manage-customer', 'finish-deploy', {
    'message': message_text,
    'title': message_text,
    'id': app_id,
    })

