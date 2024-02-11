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

class Users(TableRecord):
    table_name: str = 'users'
    fields: Dict[str, str] = {
        'username': None,
        'password': None,
        'email': None,
        'projects': None,
        'group_id': None,
    }
    field_types: Dict[str, str] = {
        'username': 'VARCHAR(255)',
        'password': 'VARCHAR(255)',
        'email': 'VARCHAR(255)',
        'projects': 'VARCHAR(255)',
        'group_id': 'VARCHAR(255)',
    }

class Group(TableRecord):
    table_name: str = 'groups'
    fields: Dict[str, str] = {
        'name': None,
        'users': None, # JSON
        'permissions': None # JSON
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'users': 'VARCHAR(255)',
        'permissions': 'VARCHAR(255)'
    }

class Permissions(TableRecord):
    table_name: str = 'permissions'
    fields: Dict[str, str] = {
        'name': None,
        'group_id': None, # id
        'permissions': None # JSON
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'group_id': 'VARCHAR(255)',
        'permissions': 'VARCHAR(255)'
    }

class Project(TableRecord):
    table_name: str = 'projects'
    fields: Dict[str, str] = {
        'name': None,
        'description': None,
        'leader': None, # id
        'participants': None, # JSON
        'status': None
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'description': 'VARCHAR(255)',
        'leader': 'VARCHAR(255)',
        'participants': 'VARCHAR(255)',
        'status': 'VARCHAR(255)'
    }

class CV(TableRecord):
    table_name: str = 'cv'
    fields: Dict[str, str] = {
        'name': None,
        'phone': None,
        'email': None,
        'personal_description': None, # JSON
        'previous_experiences': None, # JSON
        'education': None, # JSON
        'skills': None, # JSON
    }

    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'phone': 'VARCHAR(255)',
        'email': 'VARCHAR(255)',
        'personal_description': 'VARCHAR(255)',
        'previous_experiences': 'VARCHAR(255)',
        'education': 'VARCHAR(255)',
        'skills': 'VARCHAR(255)',
    }

class Candidate(TableRecord):
    table_name: str = 'candidates'
    fields: Dict[str, str] = {
        'name': None,
        'cv_id': None,
        'status': None,
        'project_id': None
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'cv_id': 'VARCHAR(255)',
        'status': 'VARCHAR(255)',
        'project_id': 'VARCHAR(255)'
    }
