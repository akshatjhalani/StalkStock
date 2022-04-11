from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Json
from model.base_model import Base


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    stock = Column(String)
    data = Column(Json)

    def __repr__(self):
        return "<Stock(id='%s', stock='%s')>" % (self.id, self.stock)
