import json
import uuid
import os
from datetime import datetime
from user_base import UserBase

class UserManager(UserBase):
    def __init__(self, user_db="db/users.json", team_db="db/teams.json"):
        self.user_db = user_db
        self.team_db = team_db
        
        # --- AUTO-CREATE LOGIC ---
        # Ensure db directory and files exist so the code doesn't crash on load
        for file_path in [self.user_db, self.team_db]:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)

    def _load_users(self):
        try:
            with open(self.user_db, 'r') as f: 
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): 
            return {}

    def _save_users(self, data):
        with open(self.user_db, 'w') as f: 
            json.dump(data, f, indent=4)

    def create_user(self, request: str) -> str:
        req = json.loads(request)
        users = self._load_users()
        
        # Constraints check
        if any(u['name'] == req['name'] for u in users.values()):
            raise ValueError("User name must be unique")
        if len(req['name']) > 64 or len(req['display_name']) > 64:
            raise ValueError("Names must be <= 64 characters")

        user_id = str(uuid.uuid4())
        users[user_id] = {
            "id": user_id,  # Added ID inside the object for easier listing
            "name": req['name'],
            "display_name": req['display_name'],
            "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save_users(users)
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users = self._load_users()
        return json.dumps(list(users.values()))

    def describe_user(self, request: str) -> str:
        user_id = json.loads(request)['id']
        users = self._load_users()
        if user_id not in users: 
            raise KeyError("User not found")
        return json.dumps(users[user_id])

    def update_user(self, request: str) -> str:
        req = json.loads(request)
        users = self._load_users()
        user_id, new_data = req['id'], req['user']
        
        if user_id not in users: 
            raise KeyError("User not found")
        if users[user_id]['name'] != new_data['name']:
            raise ValueError("User name cannot be updated")
            
        users[user_id]['display_name'] = new_data['display_name']
        self._save_users(users)
        return json.dumps({"status": "success"})

    def get_user_teams(self, request: str) -> str:
        user_id = json.loads(request)['id']
        # Load teams database
        try:
            with open(self.team_db, 'r') as f: 
                teams = json.load(f)
        except: 
            return json.dumps([])
            
        user_teams = [
            {"name": t["name"], "description": t["description"], "creation_time": t["creation_time"]}
            for t in teams.values() if user_id in t.get('users', [])
        ]
        return json.dumps(user_teams)