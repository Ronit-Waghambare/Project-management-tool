import json
import uuid
import os
from datetime import datetime
from team_base import TeamBase

class TeamManager(TeamBase):
    def __init__(self, db_path="db/teams.json", user_db="db/users.json"):
        self.db_path = db_path
        self.user_db = user_db

        # AUTO-CREATE LOGIC: Ensure db directory and files exist
        for file_path in [self.db_path, self.user_db]:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)

    def _load_data(self):
        try:
            with open(self.db_path, 'r') as f: return json.load(f)
        except: return {}

    def _save_data(self, data):
        with open(self.db_path, 'w') as f: json.dump(data, f, indent=4)

    def create_team(self, request: str) -> str:
        data = json.loads(request)
        teams = self._load_data()
        
        # Constraint: Team name must be unique
        if any(t['name'] == data['name'] for t in teams.values()):
            raise ValueError("Team name must be unique")
        
        # Constraint: Name and description length (assuming 64 and 128 as per standards)
        if len(data['name']) > 64 or len(data['description']) > 128:
            raise ValueError("Name or description exceeds character limit")
        
        team_id = str(uuid.uuid4())
        teams[team_id] = {
            "id": team_id,
            "name": data['name'],
            "description": data['description'],
            "admin": data['admin'],
            "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "users": [data['admin']] # Admin is added as the first member
        }
        self._save_data(teams)
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams = self._load_data()
        # Return summary list as per requirements
        return json.dumps([
            {"name": t["name"], "description": t["description"], "creation_time": t["creation_time"], "admin": t["admin"]}
            for t in teams.values()
        ])

    def describe_team(self, request: str) -> str:
        team_id = json.loads(request)['id']
        team = self._load_data().get(team_id)
        if not team: 
            raise KeyError("Team not found")
        return json.dumps({
            "name": team["name"], 
            "description": team["description"], 
            "creation_time": team["creation_time"], 
            "admin": team["admin"]
        })

    def update_team(self, request: str) -> str:
        req = json.loads(request)
        teams = self._load_data()
        team_id = req['id']
        new_data = req['team']
        
        if team_id not in teams:
            raise KeyError("Team not found")
        
        # Constraint: Name cannot be updated
        if teams[team_id]['name'] != new_data['name']:
            raise ValueError("Team name cannot be updated")
            
        teams[team_id]['description'] = new_data['description']
        teams[team_id]['admin'] = new_data['admin']
        self._save_data(teams)
        return json.dumps({"status": "success"})

    def add_users_to_team(self, request: str):
        req = json.loads(request)
        teams = self._load_data()
        team = teams.get(req['id'])
        if not team:
            raise KeyError("Team not found")
            
        # Constraint: Max 50 users
        if len(team['users']) + len(req['users']) > 50:
            raise ValueError("Max 50 users allowed per team")
            
        team['users'] = list(set(team['users'] + req['users']))
        self._save_data(teams)
        return json.dumps({"status": "success"})

    def remove_users_from_team(self, request: str):
        req = json.loads(request)
        teams = self._load_data()
        team = teams.get(req['id'])
        if not team:
            raise KeyError("Team not found")
            
        # Filter out users to be removed
        team['users'] = [u for u in team['users'] if u not in req['users']]
        self._save_data(teams)
        return json.dumps({"status": "success"})

    def list_team_users(self, request: str):
        team_id = json.loads(request)['id']
        team = self._load_data().get(team_id)
        if not team:
            raise KeyError("Team not found")
            
        try:
            with open(self.user_db, 'r') as f: 
                all_users = json.load(f)
        except: 
            return json.dumps([])
            
        return json.dumps([
            {"id": uid, "name": all_users[uid]["name"], "display_name": all_users[uid]["display_name"]}
            for uid in team['users'] if uid in all_users
        ])