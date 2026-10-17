import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SmartCommute-Routes')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    # Get route from query string, default to BUS-101
    params = event.get('queryStringParameters') or {}
    route_id = params.get('route', 'BUS-101')

    response = table.query(
        KeyConditionExpression=Key('route_id').eq(route_id),
        ScanIndexForward=False,
        Limit=1
    )

    items = response.get('Items', [])
    latest = items[0] if items else {}

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(latest, cls=DecimalEncoder)
    }
