from typing import Dict
from .tablerecord import TableRecord

class Visit(TableRecord):
    table_name: str = 'visits'
    fields: Dict[str, str] = {
        'user_agent': None,
        'ip': None
    }
    field_types: Dict[str, str] = {
        'user_agent': 'VARCHAR(255)',
        'ip': 'VARCHAR(255)'
    }

    def __init__(self, user_agent: str = None, ip: str = None, **data):
        super().__init__(**data)
        self.fields['user_agent'] = user_agent
        self.fields['ip'] = ip

class User(TableRecord):
    table_name: str = 'users'
    fields: Dict[str, str] = {
        'username': None,
        'password': None
    }
    field_types: Dict[str, str] = {
        'username': 'VARCHAR(255)',
        'password': 'VARCHAR(255)'
    }

    def __init__(self, username: str = None, password: str = None, **data):
        super().__init__(**data)
        self.fields['username'] = username
        self.fields['password'] = password

class Project(TableRecord):
    table_name: str = 'projects'
    fields: Dict[str, str] = {
        'name': None,
        'description': None,
        'leader': None,
        'participants': None,
        'status': None
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'description': 'VARCHAR(255)',
        'leader': 'VARCHAR(255)',
        'participants': 'VARCHAR(255)',
        'status': 'VARCHAR(255)'
    }

    def __init__(self, name: str = None, description: str = None, leader: str = None, participants: str = None, status: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['description'] = description
        self.fields['leader'] = leader
        self.fields['participants'] = participants
        self.fields['status'] = status

