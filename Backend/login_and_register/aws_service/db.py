import boto3

from config import Config


class Db:
    def __init__(self, config: Config):
        self.db = boto3.resource('dynamodb',
                                 aws_access_key_id=config.aws_access_key,
                                 aws_secret_access_key=config.aws_secret_key,
                                 region_name="us-east-1")

    def insert_item(self, table_name, **kwargs):
        table = self.db.Table(table_name)
        # with put_item function we insert data in Table
        response = table.put_item(
            **kwargs
        )
        return response

    def get_item(self, table_name, **kwargs):
        table = self.db.Table(table_name)
        response = table.get_item(
            **kwargs
        )
        if 'Item' in response:
            response = response['Item']
        return response

    def get_all_items(self, table_name):
        table = self.db.Table(table_name)
        response = table.scan()
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            print(response['LastEvaluatedKey'])
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        return items

