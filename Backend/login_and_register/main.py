import json
import boto3

from aws_service.cognito import Cognito
from bl.user_detail_bl import user_details
from config import Config
from db_helper import DbHelper
from error_handler.sas_handle_exception import sas_handle_exception
from event_utility import EventUtility
from model.user_detail import UserDetail
from utility import get_json_from_alchemy_obj

config = Config()
# db = DbHelper(config.conn_string)
# db = Db(config)


@sas_handle_exception
def lambda_handler_login(event, context):
    """
    Endpoint for User Login
    """
    event = EventUtility(event)
    body = event.get_body()
    user_name = body['username']
    password = body['password']
    cognito = Cognito(config)
    token = cognito.authenticate_and_get_token(user_name, password)
    return {"username": user_name, "token": token}



@sas_handle_exception
def lambda_handler_register(event, context):
    """
    Endpoint for User Registration
    """
    event = EventUtility(event)
    body = event.get_body()
    user_name = body['username']
    email = body['email']
    password = body['password']
    cognito = Cognito(config)
    result = cognito.sign_up(user_name, password, email, user_name)
    user = UserDetail(user_name=user_name, email=email,
                      is_deleted=False)
    # db.insert(user, commit=True, flush=True)
    return {"username": user_name}


@sas_handle_exception
def lambda_handler_get_stock_details(event, context):
    import yfinance as yf
    event = EventUtility(event)
    body = event.get_body()
    stock = body['stock']

    msft = yf.Ticker(stock)
    print(msft)


if __name__ == "__main__":
    # response = db.query(Order).all()
    # print(Order.generate_response(response))
    event = {'body-json': {'full_name': 'Aditya Jhalani', 'user_name': "aditia",
                           'stock': "AAPL",
                                        'email': "ad@gmail.com", 'password': "Akshat@1234"},
             'context': {'username': '', 'email': ''}}
    # event['context']['username'] = ''
    # event['context']['email'] =''
    lambda_handler_get_stock_details(event, None)
    cognito = Cognito(config)
    print(cognito.authenticate_and_get_token("aditia", "Akshat@1234"))
