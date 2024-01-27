from typing import Dict
from .tablerecord import TableRecord

class Visit(TableRecord):
    table_name: str = 'visits'
    fields: Dict[str, str] = { 'user_agent': None, 'ip': None }
    field_types: Dict[str, str] = {
        'user_agent': 'VARCHAR(255)',
        'ip': 'VARCHAR(255)'
    }

    def __init__(self, **data):
        super().__init__(**data)

    def define_fields(self) -> Dict[str, str]:
        return self.fields
    
    def define_field_types(self) -> Dict[str, str]:
        return self.field_types