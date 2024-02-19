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

class Router(TableRecord):
    table_name: str = 'router'
    fields: Dict[str, str] = {
        'name': None,
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
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

class Project(TableRecord):
    table_name: str = 'projects'
    fields: Dict[str, str] = {
        'name': None,
        'description': None,
        'tor': None, # JSON
        'participants': None, # JSON
        'status': None,
        'image': None
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'description': 'TEXT',
        'tor': 'TEXT',
        'participants': 'VARCHAR(255)',
        'status': 'VARCHAR(255)',
        'image': 'TEXT'
    }

class CV(TableRecord):
    table_name: str = 'cv'
    fields: Dict[str, str] = {
        'name': None,
        'phone': None,
        'email': None,
    }

    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'phone': 'VARCHAR(255)',
        'email': 'VARCHAR(255)',
    }

class Applicants(TableRecord):
    table_name: str = 'applicants'
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
