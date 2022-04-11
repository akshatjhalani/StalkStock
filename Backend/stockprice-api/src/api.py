try:
    import unzip_requirements
except ImportError:
    pass

import json
import logging
import boto3
import os
import datetime
import psycopg2
import botocore
import pandas as pd

BUCKET_NAME = os.environ['S3_BUCKET']

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if os.environ.get('IS_LOCAL'):
    dbhost = 'localhost'
    dbname = 'postgres'
    dbuser = 'rasp'
    dbpassword = '2333'
else:
    dbhost = os.environ.get('DB_HOST')
    dbname = os.environ.get('DB_NAME')
    dbuser = os.environ.get('DB_USER')
    dbpassword = os.environ.get('DB_PASSWORD')

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)


def price(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    query_params = event.get('queryStringParameters', {})
    path_params = event.get('pathParameters', None)
    if path_params is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Bad request'})
        }

    symbol = path_params.get('symbol', None)
    if symbol is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'symbol is required'})
        }

    interval = query_params.get('interval', 'D')
    if interval not in ['h', 'D']:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'invalid interval {interval}'})
        }

    start = query_params.get('start', None)
    if start is not None:
        try:
            start = datetime.datetime.fromisoformat(start)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'invalid start {start}, start time must be ISO8601 format'})
            }
    else:
        if interval == 'D':
            start = datetime.datetime.now() - datetime.timedelta(days=365)
        else:
            start = datetime.datetime.now() - datetime.timedelta(days=30)

    end = query_params.get('end', None)
    if end is not None:
        try:
            end = datetime.datetime.fromisoformat(end)
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'invalid end {end}, end time must be ISO8601 format'})
            }

    logger.info(f"start: {start}, end: {end}, interval: {interval}")
    response = query_gte(symbol, start, interval) if end is None else query(symbol, start, end, interval)
    items = response['Items']

    body = {
        "prices": items
    }
    return {"statusCode": 200, "body": json.dumps(body)}


def list_stocks(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    with psycopg2.connect(
            host=dbhost,
            dbname=dbname,
            user=dbuser,
            password=dbpassword
    ) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM fetcher_meta f;")
        data = cur.fetchall()
        symbols = [d[0] for d in data]

        body = {
            "symbols": symbols
        }
        return {"statusCode": 200, "body": json.dumps(body)}


def query_gte(symbol, start, interval):
    if interval == 'D':
        table = dynamodb.Table(os.environ['DAILY_DYNAMODB_TABLE'])
        start = start.strftime('%Y-%m-%d')
    else:
        table = dynamodb.Table(os.environ['HOURLY_DYNAMODB_TABLE'])
        start = start.strftime('%Y-%m-%dT%H:%M:%S')
    logger.info(f"Querying {table.name} for {symbol} from {start}")

    from boto3.dynamodb.conditions import Key
    response = table.query(
        KeyConditionExpression=Key('symbol').eq(symbol) & Key('date').gte(start)
    )
    # logger.info(f"Query result: {response}")

    for item in response['Items']:
        if 'open' in item:
            item['open'] = float(item['open'])
        if 'high' in item:
            item['high'] = float(item['high'])
        if 'low' in item:
            item['low'] = float(item['low'])
        if 'close' in item:
            item['close'] = float(item['close'])
        if 'volume' in item:
            item['volume'] = int(item['volume'])
    return response


def query(symbol, start, end, interval):
    if interval == 'D':
        table = dynamodb.Table(os.environ['DAILY_DYNAMODB_TABLE'])
        start = start.strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d')
    else:
        table = dynamodb.Table(os.environ['HOURLY_DYNAMODB_TABLE'])
        start = start.strftime('%Y-%m-%dT%H:%M:%S')
        end = end.strftime('%Y-%m-%dT%H:%M:%S')
    logger.info(f"Querying {table.name} for {symbol} from {start} to {end}")

    from boto3.dynamodb.conditions import Key
    response = table.query(
        KeyConditionExpression=Key('symbol').eq(symbol) & Key('date').between(start, end)
    )
    # logger.info(f"Query result: {response}")

    for item in response['Items']:
        if 'open' in item:
            item['open'] = float(item['open'])
        if 'high' in item:
            item['high'] = float(item['high'])
        if 'low' in item:
            item['low'] = float(item['low'])
        if 'close' in item:
            item['close'] = float(item['close'])
        if 'volume' in item:
            item['volume'] = int(item['volume'])
    return response


def predict(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    path_params = event.get('pathParameters', None)
    if path_params is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Bad request'})
        }

    symbol = path_params.get('symbol', None)
    if symbol is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'symbol is required'})
        }

    # load data from S3 bucket
    try:
        bucket.download_file(f'result/macd/{symbol}.csv', f'/tmp/{symbol}_macd.csv')
        bucket.download_file(f'result/price/{symbol}.csv', f'/tmp/{symbol}_price.csv')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logger.info(f"The symbol {symbol} does not exist.")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'The symbol {symbol} does not exist.'})
            }
        else:
            raise
    except Exception as e:
        context.serverless_sdk.capture_exception(e)
        logger.error(f"Failed to load data from S3 bucket: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to load data from S3 bucket: {e}'})
        }

    # load csv to pandas
    try:
        macd_df = pd.read_csv(f'/tmp/{symbol}_macd.csv', index_col=0, parse_dates=True)
        price_df = pd.read_csv(f'/tmp/{symbol}_price.csv', index_col=0, parse_dates=True)
    except Exception as e:
        context.serverless_sdk.capture_exception(e)
        logger.error(f"Failed to load csv to pandas: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to load predict price: {e}'})
        }

    dt = macd_df.index[0]
    price_df = price_df.loc[dt:]
    prices = []
    macds = []
    for dt, row in price_df.iterrows():
        prices.append({
            'date': dt.strftime('%Y-%m-%d'),
            **{head: row[head] for head in price_df.head()}
        })
    for dt, row in macd_df.iterrows():
        macds.append({
            'date': dt.strftime('%Y-%m-%d'),
            **{head: row[head] for head in macd_df.head()}
        })

    body = {
        "prices": prices,
        "macd_hists": macds
    }
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
