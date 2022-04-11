try:
    import unzip_requirements
except ImportError:
    pass

import datetime
import json
import decimal
import logging
import yfinance as yf
import numpy as np
import psycopg2
import os
import utils
import pytz
import boto3

sgtz = pytz.timezone('Asia/Singapore')

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


def run(event, context):
    current_time = datetime.datetime.now(sgtz).time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    try:
        with psycopg2.connect(
                host=dbhost,
                dbname=dbname,
                user=dbuser,
                password=dbpassword
        ) as conn:
            current_date = datetime.date.today()
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM fetcher_meta f ORDER BY f.last_fetched ASC LIMIT 7;")
            data = cur.fetchall()
            if len(data) == 0:
                logger.info(f"No stocks to fetch")
                return {"statusCode": 200, "body": "No stocks to fetch"}

            idx = abs(int(np.random.normal(0, len(data) / 2)))
            idx = len(data)-1 if idx >= len(data) else idx
            logger.info(f"Stock to be fetched: {data[idx]}")

            from dateutil.relativedelta import relativedelta
            symbol = data[idx][0]
            last_fetched = data[idx][1]
            end_date = last_fetched + relativedelta(months=3)

            if current_date < end_date:
                end_date = current_date
            logger.info(f"Fetching data for {symbol} from {last_fetched} to {end_date}")

            data = yf.download(
                tickers=symbol,
                start=last_fetched.isoformat(),
                end=end_date.isoformat(),
                interval="1d",
                auto_adjust=True,
            )

            table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
            cnt = 0
            with table.batch_writer() as batch:
                for idx, row in data.iterrows():
                    fetched_date = row.name.date()
                    from math import isnan, isinf
                    if isnan(row['Open']) or isnan(row['Close']) or isnan(row['High']) or isnan(row['Low']) or \
                            isinf(row['Open']) or isinf(row['Close']) or isinf(row['High']) or isinf(row['Low']):
                        logger.debug(row)
                        logger.warning(f"Skipping {fetched_date} for {symbol} since it contains NaN or Inf")
                        continue
                    item = {
                        'symbol': symbol,
                        'date': fetched_date.isoformat(),
                        'open': decimal.Decimal(format(row['Open'], ".4f")),
                        'high': decimal.Decimal(format(row['High'], ".4f")),
                        'low': decimal.Decimal(format(row['Low'], ".4f")),
                        'close': decimal.Decimal(format(row['Close'], ".4f")),
                        'volume': decimal.Decimal(format(row['Volume'], ".4f"))
                    }
                    if fetched_date > end_date:
                        logger.warning(f"{item} is too new, skipping")
                        continue
                    cnt += 1
                    last_fetched = fetched_date

                    batch.put_item(Item=item)

            logger.info(f"{cnt} items inserted")

            cur.execute(f"UPDATE fetcher_meta SET last_fetched = '{last_fetched}' WHERE symbol = '{symbol}';")
            logger.info(f"{symbol} is updated with last_fetched = {last_fetched}")

            body = {
                "last_fetched": f"{last_fetched}",
                "items": cnt
            }
            return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        context.serverless_sdk.capture_exception(e)
        logger.error(f"Failed to fetch data: {e}")
        return {"statusCode": 500, "body": f"Failed to fetch data: {e}"}


def init_db(event, context):
    current_time = datetime.datetime.now(sgtz).time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    with psycopg2.connect(
            host=dbhost,
            dbname=dbname,
            user=dbuser,
            password=dbpassword
    ) as conn:
        cur = conn.cursor()

        drop_table_query = "DROP TABLE IF EXISTS fetcher_meta;"
        cur.execute(drop_table_query)

        create_table_query = '''CREATE TABLE fetcher_meta (
            symbol varchar(10) PRIMARY KEY,
            last_fetched date NOT NULL
        );'''
        cur.execute(create_table_query)
        conn.commit()


def add_stock(event, context):
    current_time = datetime.datetime.now(sgtz).time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    if 'symbol' not in event or 'last_fetched' not in event:
        logger.error(f"Missing symbol or last_fetched in event {event}")
        return {"statusCode": 400, "body": "'symbol' and 'last_fetched' are required"}

    try:
        symbol = event['symbol']
        last_fetched = datetime.date.fromisoformat(event['last_fetched'])
    except ValueError:
        logger.error(f"Invalid last_fetched in event {event}")
        return {"statusCode": 400, "body": "'last_fetched' must be in ISO format"}

    with psycopg2.connect(
            host=dbhost,
            dbname=dbname,
            user=dbuser,
            password=dbpassword
    ) as conn:
        cur = conn.cursor()

        insert_query = '''INSERT INTO fetcher_meta (symbol, last_fetched)
            VALUES (%s, %s)
            ON CONFLICT (symbol) DO UPDATE SET last_fetched = %s;
        '''
        logger.info(f"Inserting {symbol} with last_fetched {last_fetched}")
        try:
            cur.execute(insert_query, (symbol, last_fetched, last_fetched))
            conn.commit()
        except Exception as err:
            context.serverless_sdk.capture_exception(err)
            logger.error(f"Error inserting into fetcher_meta: {err}")
            logger.error(f"Exception type: {type(err)}")
            return {"statusCode": 500, "body": f"Error inserting into fetcher_meta: {err}"}

    return {"statusCode": 200, "body": "Successfully added stock"}


def add_stocks(event, context):
    current_time = datetime.datetime.now(sgtz).time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")

    if 'symbols' not in event or 'last_fetched' not in event:
        logger.error(f"Missing symbols or last_fetched in event {event}")
        return {"statusCode": 400, "body": "'symbols' and 'last_fetched' are required"}

    for symbol in event['symbols']:
        event = {
            'symbol': symbol,
            'last_fetched': event['last_fetched']
        }
        add_stock(event, context)
    return {"statusCode": 200, "body": "Successfully added stocks"}


def status(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Function {name} ran at {str(current_time)}, with event {event}")
    logger.info(f"DB info: password: {dbpassword} host: {dbhost} dbname: {dbname} user: {dbuser}")

    try:
        with psycopg2.connect(
                host=dbhost,
                dbname=dbname,
                user=dbuser,
                password=dbpassword
        ) as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM fetcher_meta f ORDER BY f.last_fetched ASC;")
            data = cur.fetchall()

            for row in data:
                logger.info(f"{row[0]} {row[1]}")

            body = {
                "status": f"{data}",
            }
            return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        context.serverless_sdk.capture_exception(e)
        logger.error(f"Failed to fetch status: {e}")
        return {"statusCode": 500, "body": f"Failed to fetch status: {e}"}