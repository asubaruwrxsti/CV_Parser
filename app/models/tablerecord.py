from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import HTTPException
from app.dependencies import Database
from psycopg2 import sql, errors
from abc import ABC

class TableRecord(BaseModel, ABC):
    table_name: str
    fields: Dict[str, str]
    field_types: Dict[str, str]

    def __init__(self, **data):
        super().__init__(**data)
        for field in self.fields:
            if field in data:
                self.fields[field] = data[field]
        self._create_table(Database())

    async def create_record(self, db: Database):
        await self._create_query(db, "INSERT INTO {} ({}) VALUES ({})", self.fields)

    async def get_records(self, db: Database, record_id: Optional[int] = None):
        if record_id is not None:
            records = await self._create_query(db, "SELECT * FROM {} WHERE id = %s", {'id': record_id})
        else:
            records = await self._create_query(db, "SELECT * FROM {}", {})
        return records
    
    async def update_record(self, db: Database, record_id: int, fields: Dict[str, str]):
        set_clause = ', '.join(f'{field} = %s' for field in fields.keys())
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
        fields['id'] = record_id  # move this line here
        await self._create_query(db, query, fields)
    
    async def delete_record(self, db: Database, record_id: int):
        await self._create_query(db, "DELETE FROM {} WHERE id = %s", {'id': record_id})

    async def _create_query(self, db: Database, query_template: str, fields: Dict[str, str]):
        placeholders = sql.SQL(', ').join(sql.Placeholder() * len(fields))
        query = sql.SQL(query_template).format(
            sql.Identifier(self.table_name),
            sql.SQL(', ').join(map(sql.Identifier, fields.keys())),
            placeholders
        )
        query = await self._execute_query(db, query, tuple(fields.values()))
        return query

    async def _execute_query(self, db: Database, query: str, values: tuple):
        try:
            result = db.query(query, values)
            db.commit()
            # Assuming self.fields is a dictionary where keys are field names
            # Add 'id' as the first key
            keys = ['id'] + list(self.fields.keys())
            if result is not None:
                result_dict = [dict(zip(keys, row)) for row in result]
            else:
                result_dict = []
            return result_dict
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
                sql.SQL('{} {} DEFAULT NULL').format(sql.Identifier(key), sql.SQL(self.field_types[key]))
                for key in self.field_types.keys()
            )
        )
        db.query(query, None)