import pusher
import argparse

# Set up Pusher
pusher_client = pusher.Pusher(
    app_id='your_app_id',
    key='your_key',
    secret='your_secret',
    cluster='your_cluster',
    ssl=True
)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--percent', type=int, required=True, help='Progress percent')
parser.add_argument('--title', type=str, required=True, help='Progress title')
parser.add_argument('--id', type=str, required=True, help='Progress ID')

args = parser.parse_args()

# Trigger Pusher event
pusher_client.trigger('manage-customer', 'deploy', 
    {
    'message': f'Progress at {args.percent}%',
    'title': args.title,
    'id': args.id,
    'percent': args.percent
})
