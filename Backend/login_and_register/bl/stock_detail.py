from db_helper import DbHelper
from model.stock_model import Stock


def get_stock_details(db: DbHelper, stock):
    try:
        response = db.query(Stock).filter_by(stock=stock).one()
        return response
    except Exception as e:
        print(e)
        raise Exception("Unauthorized")
