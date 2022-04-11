import functools
from error_handler.sas_error import SasCustomError


def sas_handle_exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            print (error)
            # log the exception
            err = "There was an exception in "
            err += function.__name__
            print (err)
            # create a response and return
            if hasattr(error, 'create_response_json'):
                return error.create_response_json()
            else:
                print (error)
                message = error.__class__.__name__ + ": " + str(error)
                return SasCustomError(message).create_response_json()
    return wrapper
