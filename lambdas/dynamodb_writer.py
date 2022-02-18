import os
import boto3



def handler(event, contex):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    for record in event['Records']:
        payload = record["body"]
        response = table.put_item(
        Item={
            'id': str(payload)
        }
    )
    print("PutItem succeeded:")
 

    return   {
        'statusCode': 200,
        'records': event["Records"]
    }