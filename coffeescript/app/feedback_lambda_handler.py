import logging, re, os
import urllib.parse
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

# I just want coffee
COUNT_STRING = os.getenv('OBJECT_COUNT_STRING')
# coffee-count
TABLE_NAME = os.getenv('DYNAMO_TABLE_NAME')

def lambda_handler(event, context):
    try:
        s3_record = parse_record(event)
        s3_response = s3_get_object(**s3_record)
        s3_object_body = s3_response['Body'].read().decode('utf-8')
        return dynamodb_save_count(
            count=count_occurences(COUNT_STRING, s3_object_body),
            key=s3_record['key'],
            table_name=TABLE_NAME
        )
    except Exception as e:
        logger.info("error", exc_info=e)
        raise e

def parse_record(event):
    try:
        record = event['Records'][0]['s3']
        bucket, key = record['s3']['bucket']['name'], record['object']['key']
        return {'bucket': bucket, 'key': urllib.parse.unquote_plus(key, encoding='utf-8')}
    except Exception as e:
        logger.info(f"Error parsing s3 record from event: {event}", exc_info=e)
        raise e

def s3_get_object(bucket, key):
    try:
        return s3.get_object(Bucket=bucket, Key=key)
    except ClientError as e:
        msg = 'Check object/key exist and that bucket/lambda region match'
        logger.info(f"Error getting key: {key}, from bucket {bucket}. {msg}", exc_info=e)
        raise e

def count_occurences(string, text):
    return len([m.start() for m in re.finditer(string, text)])

def dynamodb_save_count(count, key, table_name):
    try:
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
    except ClientError as e:
        logger.info(f"Error writing to dynamodb, key: {key}, count: {count}", exc_info=e)