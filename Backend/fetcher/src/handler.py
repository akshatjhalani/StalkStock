try:
    import unzip_requirements
except ImportError:
    pass

import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def hello(event, context):
    DB = os.environ['DB_HOST']
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!!",
        "input": event,
        "DB": DB
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def rate(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info(f"Your function {name} ran at {str(current_time)}")