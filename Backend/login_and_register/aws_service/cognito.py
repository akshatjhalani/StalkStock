# import boto3

from config import Config


class Cognito:
    def __init__(self, config: Config):
        self.config = config
        self.client = boto3.client('cognito-idp',
                                            aws_access_key_id=config.aws_access_key,
                                            aws_secret_access_key=config.aws_secret_key,
                                            region_name="us-east-1")

    def sign_up(self, user_name, password, email_address, full_name):
        config = self.config
        response = self.client.sign_up(
            ClientId=config.cognito_client_id,
            Username=user_name,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email_address
                },{
                    'Name': 'custom:fullname',
                    'Value': full_name
                }
            ]
        )
        # then confirm signup
        resp = self.client.admin_confirm_sign_up(
            UserPoolId=config.cognito_user_pool_id,
            Username=user_name
        )
        return response

    def authenticate_and_get_token(self, username: str, password: str):
        config = self.config
        resp = self.client.admin_initiate_auth(
            UserPoolId=config.cognito_user_pool_id,
            ClientId=config.cognito_client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            }
        )

        print("Log in success")
        # print("Access token:", resp['AuthenticationResult']['AccessToken'])
        return resp['AuthenticationResult']['IdToken']

    def check_user_in_group(self, user_name, group_name):
        response = self.client.admin_list_groups_for_user(
            Username=user_name,
            UserPoolId=self.config.cognito_user_pool_id
        )
        if 'Groups' in response:
            groups = response['Groups']
            for group in groups:
                if group_name == group['GroupName']:
                    return True
        return False