import json
import urllib.parse
import boto3
import re


s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

TABLE_NAME = 'coffee-count'
PATTERN = 'I just want coffee'


def lambda_handler(event, context):
    try:
        s3_record = parse_event_record(event)
        s3_object = s3_get_object(**s3_record)
        s3_object_body = s3_object['Body'].read().decode('utf-8')

        coffee_count = count_matches(PATTERN, s3_object_body)

        return write_dynamodb(
            table_name=TABLE_NAME,
            key=s3_record['key'],
            count=coffee_count
        )
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


def parse_event_record(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    return { 'bucket': bucket, 'key': key }


def s3_get_object(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)


def count_matches(pattern, body):
    return len([m.start() for m in re.finditer(pattern, body)])
    

def write_to_dynamodb(table_name, key, count):
    return dynamodb.put_item(
        TableName=table_name,
        Item={
            'filename': {
                'S': key
            },
            'count': {
                'N': str(count)
            },
        })
