from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from model.base_model import Base


class UserDetail(Base):
    __tablename__ = 'user_detail'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    is_deleted = Column(Boolean)
    created_at = Column(DateTime)

    def __repr__(self):
        return "<User(id='%s', user_name='%s')>" % (self.id, self.user_name)
