from .tablerecord import TableRecord

class Visit(TableRecord):
    table_name: str = 'visits'
    fields: dict = { 'user_agent': None, 'ip': None }
    field_types: dict = {
        'user_agent': 'VARCHAR(255)',
        'ip': 'VARCHAR(255)'
    }

    def __init__(self, **data):
        super().__init__(**data)

    def define_fields(self):
        return self.fields
    
    def define_field_types(self):
        return self.field_types