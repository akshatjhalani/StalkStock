import json


class SasBaseError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def create_response_json(self):
        response = {
            'httpStatus': self.status_code,
            'message': self.message
        }
        print (response)
        raise Exception(json.dumps(response, default=datetime_handler))


class SasCustomError(SasBaseError):
    def __init__(self, message):
        super(SasCustomError, self).__init__(message, 400)


class UnauthorizedError(SasBaseError):
    def __init__(self, message):
        super(UnauthorizedError, self).__init__(message, 401)


class NotFoundError(SasBaseError):
    def __init__(self, message):
        super(NotFoundError, self).__init__(message, 400)

def datetime_handler(x):
    from datetime import datetime, date
    import decimal

    if isinstance(x, (datetime, date)):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return float(x)
    if hasattr(x, 'get_as_json'):
        return x.get_as_json()
