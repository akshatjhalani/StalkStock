from functools import wraps

from aws_service.cognito import Cognito
from config import Config
from db_helper import DbHelper
from event_utility import EventUtility
from model.user_detail import UserDetail


def user_details(db, required_role=None):
    def _user_details(orig_func):
        @wraps(orig_func)
        def get_user_details(self, *args, **kwargs):
            event_obj = _get_user_details(self, db, required_role)
            return orig_func(event_obj, *args, **kwargs)
        return get_user_details
    return _user_details


def _get_user_details(instance, db: DbHelper, required_role=None):
    try:
        event = EventUtility(instance)
        db.rollback()
        user = db.query(UserDetail).filter_by(user_name=event.user_name).one()
        event.user_id = user.id
        if required_role is not None:
            cognito = Cognito(Config())
            is_authorized = cognito.check_user_in_group(event.user_name, required_role)
            if not is_authorized:
                raise Exception("Unauthorized")
        return event
    except Exception as e:
        print(e)
        raise Exception("Unauthorized")
