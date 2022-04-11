class EventUtility:
    def __init__(self, event):
        self.event = event
        self.user_id = None
        # self.user_name = event['context']['username']
        # self.email = event['context']['email']

    def get_data(self):
        return self.event['body-json']['data']

    def get_body(self):
        return self.event['body-json']

    def get_params(self):
        return self.event['params']

    def get_query_string(self):
        return self.event['params']['querystring']

