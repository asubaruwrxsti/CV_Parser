from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import HTTPException
from app.dependencies import Database
from psycopg2 import sql, errors
from abc import ABC, abstractmethod

class TableRecord(BaseModel, ABC):
    table_name: str
    fields: Dict[str, str]

    def __init__(self, **data):
        super().__init__(**data)
        self.fields = self.define_fields()
        self.field_types = self.define_field_types()
        self._create_table(Database())

    @abstractmethod
    def define_fields(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def define_field_types(self) -> Dict[str, str]:
        pass

    async def create_record(self, db: Database):
        await self._execute_query(db, "INSERT INTO {} ({}) VALUES ({})", self.fields)

    async def get_records(self, db: Database, record_id: Optional[int] = None):
        if record_id is not None:
            records = await self._execute_query(db, "SELECT * FROM {} WHERE id = %s", {'id': record_id})
        else:
            records = await self._execute_query(db, "SELECT * FROM {}", {})
        return records
    
    async def update_record(self, db: Database, record_id: int, fields: Dict[str, str]):
        fields['id'] = record_id
        await self._execute_query(db, "UPDATE {} SET {} WHERE id = %s", fields)
    
    async def delete_record(self, db: Database, record_id: int):
        await self._execute_query(db, "DELETE FROM {} WHERE id = %s", {'id': record_id})

    async def _execute_query(self, db: Database, query_template: str, fields: Dict[str, str]):
        placeholders = sql.SQL(', ').join(sql.Placeholder() * len(fields))
        query = sql.SQL(query_template).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, fields.keys())),
            placeholders
        )
        query = await self._create_query(db, query, tuple(fields.values()))
        return query

    async def _create_query(self, db: Database, query: str, values: tuple):
        try:
            result = db.query(query, values)
            db.commit()
            return result
        except errors.UniqueViolation as e:
            raise HTTPException(status_code=409, detail=str(e))
        except errors.UndefinedTable as e:
            raise HTTPException(status_code=400, detail="The table does not exist.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def _create_table(self, db: Database):
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY, {})").format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(
                sql.SQL('{} {}').format(sql.Identifier(key), sql.SQL(self.field_types[key]))
                for key in self.field_types.keys()
            )
        )
        db.query(query, None)