from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbHelper:
    def __init__(self, conn_string="postgresql://postgres:akshat@localhost:5432/android_db"):
        db_engine = create_engine(conn_string, pool_pre_ping=True)
        db_session = sessionmaker(bind=db_engine)
        self.db_session = db_session()
        self._query = self.db_session.query
        # self.query = self.db_session.query

    @property
    def query(self):
        return self._query

    def insert(self, model, commit=True, flush=False):
        self.db_session.add(model)
        if flush:
            self.db_session.flush()
        if commit:
            self.db_session.commit()

    def commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()

