from datetime import datetime, date
import decimal


def custom_serializer_json(x):
    if isinstance(x, (datetime, date)):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return float(x)
    if hasattr(x, '__table__'):
        return {col.name: getattr(x, col.name) for col in x.__table__.columns}


def get_json_from_alchemy_obj(x):
    if isinstance(x, list):
        response = []
        for elem in x:
            if hasattr(elem, '__table__'):
                obj = {col.name: getattr(elem, col.name) for col in elem.__table__.columns}
                response.append(obj)
    else:
        response = {col.name: getattr(x, col.name) for col in x.__table__.columns}
    return response


def check_if_string_empty(string):
  if not string.strip():
      return True
  return False
