try:
    import unzip_requirements
except ImportError:
    pass

import datetime
import logging
import os
import boto3
from botocore.exceptions import ClientError
import json
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client("s3")
eventbridge = boto3.client('events')

BUCKET_NAME = os.environ['S3_BUCKET']
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    symbols = ["UNH", "GS", "HD", "MSFT", "MCD", "AMGN", "CRM", "V", "BA", "CAT", "HON", "AXP", "TRV", "AAPL", "JNJ", "CVX", "PG", "DIS", "MMM", "JPM", "WMT", "NKE", "IBM", "MRK", "KO", "DOW", "CSCO", "VZ", "INTC", "WBA"]
    # symbols = ["UNH", "GS"]

    from boto3.dynamodb.conditions import Key
    try:
        for symbol in symbols:
            table = dynamodb.Table(os.environ.get('DAILY_DYNAMODB_TABLE'))
            response = table.query(
                KeyConditionExpression=Key('symbol').eq(symbol),
                ScanIndexForward=True,
            )

            data = response['Items']
            indexes = [dic['date'] for dic in data]
            prices = [float(dic['close']) for dic in data]
            table = pd.DataFrame(prices, index=indexes, columns=['Close'])
            # print(table)

            FILE_PREFIX = "." if os.environ.get('IS_LOCAL') else "/tmp"
            FILE_NAME = f"{FILE_PREFIX}/{symbol}.csv"
            table.to_csv(FILE_NAME)

            try:
                response = s3.upload_file(FILE_NAME, BUCKET_NAME, f"raw/{symbol}.csv")
                logger.info(f"Uploaded {FILE_NAME} to {BUCKET_NAME}, with response {response}")
            except ClientError as e:
                logging.error(f"Failed to upload file {FILE_NAME} to s3 bucket {BUCKET_NAME}: {e}")

        body = {
            # "last_fetched": f"{last_fetched}",
            # "items": cnt
        }
        response = eventbridge.put_events(
            Entries=[
                {
                    'Time': datetime.datetime.now().isoformat(),
                    'Source': 'stalkstock.stockprice-api.exporter',
                    'DetailType': 'Export Succeed',
                    'Detail': '{"content": "hello"}',
                    'EventBusName': EVENT_BUS_NAME,
                },
            ]
        )
        logger.info(f"Put events response: {response}")
        return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        context.serverless_sdk.capture_exception(e)
        logger.error(f"Failed to export data: {e}")
        return {"statusCode": 500, "body": f"Failed to export data: {e}"}