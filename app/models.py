from pydantic import BaseModel
from fastapi import HTTPException
from app.dependencies import Database
from psycopg2 import sql, errors
from abc import ABC, abstractmethod

class TableRecord(BaseModel, ABC):
    table_name: str
    fields: dict

    def __init__(self, **data):
        super().__init__(**data)
        self.fields = self.define_fields()

    @abstractmethod
    def define_fields(self):
        pass

    async def create_query(self, db: Database, query: str, values: tuple):
        try:
            result = db.query(query, values)
            db.commit()
            return result
        except errors.UniqueViolation as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def create_record(self, db: Database):
        await self._execute_query(db, "INSERT INTO {} ({}) VALUES ({})", self.fields)

    async def get_records(self, db: Database, record_id: int = None):
        if record_id is not None:
            records = await self._execute_query(db, "SELECT * FROM {} WHERE id = %s", {'id': record_id})
        else:
            records = await self._execute_query(db, "SELECT * FROM {}", {})
        return records

    async def _execute_query(self, db: Database, query_template: str, fields: dict):
        placeholders = sql.SQL(', ').join(sql.Placeholder() * len(fields))
        query = sql.SQL(query_template).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, fields.keys())),
            placeholders
        )
        query = await self.create_query(db, query, tuple(fields.values()))
        return query

class Visit(TableRecord):
    table_name: str = 'visits'
    fields: dict = {'user_agent': None, 'ip': None}

    def __init__(self, **data):
        # TODO: Create the table if it doesn't exist
        super().__init__(**data)

    def define_fields(self):
        return {'user_agent': None, 'ip': None}