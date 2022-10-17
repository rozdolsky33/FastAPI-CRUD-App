from typing import Optional
from app.config import Config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select
from sqlalchemy.engine import Row


class DatabaseClient():
    def __init__(self, config: Config, tables: Optional[list[str]]):
        self.config = config
        self.engine = create_engine(self.config.postgres_host, feature=True)
        self.session = Session(bind=self.engine)
        self.metadata = MetaData(self.engine)
        self._reflect_metadata()  # metadata.tables["users"]
        if tables:  # does not trigger if tables is None, or len(tables) == 0
            self._set_internal_database_tables(tables)

    def _reflect_metadata(self) -> None:
        self.metadata.reflect()

    def _set_internal_database_tables(self, tables: list[str]):
        # e.g. sets DatabeseClient =
        for table in tables:
            setattr(self, table, self.metadata.tables[table])

    def get_first(self, query: Select) -> Optional[Row]:
        with self.session.begin():
            res = self.session.execute(query).first()
        return res

    def get_all(self, query: Select) -> list[Row]:
        with self.session.begin():
            res = self.session.execute(query).all()
        return res

    def get_paginated(self, query: Select, limit: int, offset: int) -> list[Row]:
        query = query.limit(limit).offset(offset)
        return self.get_all(query)