import json
import urllib.request
import boto3
import random
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartCommute-Routes')
sns = boto3.client('sns')

TOPIC_ARN = 'PASTE_YOUR_TOPIC_ARN_HERE'
DELAY_THRESHOLD = 5

ROUTES = {
    'BUS-101': 'Shivajinagar to Hinjewadi',
    'BUS-102': 'Swargate to Wakad',
    'BUS-103': 'Kothrud to Hadapsar',
    'BUS-104': 'Deccan to Pimpri'
}

def lambda_handler(event, context):
    city = "Pune"
    url = f"https://wttr.in/{city}?format=j1"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    temp = data['current_condition'][0]['temp_C']
    desc = data['current_condition'][0]['weatherDesc'][0]['value']

    for route_id, route_name in ROUTES.items():
        delay_min = random.choice([0, 0, 2, 8, 12])

        item = {
            'route_id': route_id,
            'timestamp': datetime.utcnow().isoformat(),
            'city': city,
            'route_name': route_name,
            'temperature': temp,
            'condition': desc,
            'delay_min': delay_min
        }

        table.put_item(Item=item)
        print(f"Saved: {route_id} — delay {delay_min} min")

        if delay_min > DELAY_THRESHOLD:
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=f"⚠️ {route_id} ({route_name}) delayed by {delay_min} min! Weather: {desc}, {temp}°C",
                Subject="SmartCommute Delay Alert"
            )

    return {'statusCode': 200, 'body': 'All routes updated'}
