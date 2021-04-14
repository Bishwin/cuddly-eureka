import json
import urllib.parse
import boto3
import re
print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        parse(key, response)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


def parse(key, res):
    coffee_count = _parse_body(res['Body'].read().decode('utf-8'))
    _write_to_dynamodb(key, coffee_count)


def _parse_body(body):
    res = [m.start() for m in re.finditer('I just want coffee', body)]
    return len(res)
    

def _write_to_dynamodb(key, coffee_count):
    client = boto3.client('dynamodb')

    response = client.put_item(
        TableName='coffee-count',
        Item={
            'filename': {
                'S': key
            },
            'count': {
                'N': str(coffee_count)
            },
        })
