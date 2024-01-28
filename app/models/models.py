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

class Users(TableRecord):
    table_name: str = 'users'
    fields: Dict[str, str] = {
        'username': None,
        'password': None,
        'projects': None,
        'group_id': None,
    }
    field_types: Dict[str, str] = {
        'username': 'VARCHAR(255)',
        'password': 'VARCHAR(255)',
        'projects': 'VARCHAR(255)',
        'group_id': 'VARCHAR(255)',
    }

    def __init__(self, username: str = None, password: str = None, projects: str = None, group_id: str = None, **data):
        super().__init__(**data)
        self.fields['username'] = username
        self.fields['password'] = password
        self.fields['projects'] = projects
        self.fields['group_id'] = group_id

class Group(TableRecord):
    table_name: str = 'groups'
    fields: Dict[str, str] = {
        'name': None,
        'users': None # JSON
    }
    field_types: Dict[str, str] = {
        'name': 'VARCHAR(255)',
        'users': 'VARCHAR(255)'
    }

    def __init__(self, name: str = None, users: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['users'] = users

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

    def __init__(self, name: str = None, group_id: str = None, permissions: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['group_id'] = group_id
        self.fields['permissions'] = permissions

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

    def __init__(self, name: str = None, description: str = None, leader: str = None, participants: str = None, status: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['description'] = description
        self.fields['leader'] = leader
        self.fields['participants'] = participants
        self.fields['status'] = status

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

    def __init__(self, name: str = None, phone: str = None, email: str = None, personal_description: str = None, previous_experiences: str = None, education: str = None, skills: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['phone'] = phone
        self.fields['email'] = email
        self.fields['personal_description'] = personal_description
        self.fields['previous_experiences'] = previous_experiences
        self.fields['education'] = education
        self.fields['skills'] = skills

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

    def __init__(self, name: str = None, cv_id: str = None, status: str = None, project_id: str = None, **data):
        super().__init__(**data)
        self.fields['name'] = name
        self.fields['cv_id'] = cv_id
        self.fields['status'] = status
        self.fields['project_id'] = project_id
