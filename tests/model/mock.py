# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session


class MockDatabase(object):
    """ In-memory DB for safer, faster testing """

    def __init__(self, engine):
        self.target_engine = engine
        self.TBase = declarative_base()
        self.TBase.metadata.reflect(bind=self.target_engine)
        self.init()

    def init(self):
        self.url = 'sqlite://'
        self.mock_engine = sqlalchemy.create_engine(self.url)

        self.MBase = declarative_base()
        self.MBase.metadata = self.TBase.metadata
        self.MBase.metadata.bind = self.mock_engine
        self.MBase.metadata.create_all()
        self._Session = scoped_session(sessionmaker(bind=self.mock_engine))

    def tables(self):
        return self.MBase.metadata.tables

    def insert(self, tablename, data):
        table = self.MBase.metadata.tables[tablename]
        s = self._Session()
        s.execute(table.insert().values(**data))
        s.commit()

    def query(self, tablename):
        table = self.MBase.metadata.tables[tablename]
        s = self._Session()
        return s.execute(table.select()).fetchall()