import json
import uuid
import os
from datetime import datetime
from project_board_base import ProjectBoardBase

class BoardManager(ProjectBoardBase):
    def __init__(self, board_db="db/boards.json"):
        self.board_db = board_db
        
        # 1. Create 'out' folder if missing
        if not os.path.exists('out'): 
            os.makedirs('out')
            
        # 2. Create 'db' folder if missing
        db_dir = os.path.dirname(self.board_db)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # 3. Create 'boards.json' with an empty dictionary {} if missing
        if not os.path.exists(self.board_db):
            with open(self.board_db, 'w') as f:
                json.dump({}, f)

    def _load_boards(self):
        try:
            with open(self.board_db, 'r') as f: return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): return {}

    def _save_boards(self, data):
        with open(self.board_db, 'w') as f: json.dump(data, f, indent=4)

    def create_board(self, request: str) -> str:
        req = json.loads(request)
        boards = self._load_boards()

        if any(b['name'] == req['name'] and b['team_id'] == req['team_id'] for b in boards.values()):
            raise ValueError("Board name must be unique for this team")
        
        board_id = str(uuid.uuid4())
        boards[board_id] = {
            "id": board_id,
            "name": req['name'],
            "description": req['description'],
            "team_id": req['team_id'],
            "status": "OPEN",
            "creation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tasks": {}
        }
        self._save_boards(boards)
        return json.dumps({"id": board_id})

    def list_boards(self, request: str) -> str:
        req = json.loads(request)
        team_id = req.get('id')
        boards = self._load_boards()
        
        output = [
            {"id": bid, "name": b["name"]} 
            for bid, b in boards.items() 
            if b['team_id'] == team_id and b['status'] == "OPEN"
        ]
        return json.dumps(output)

    def add_task(self, request: str) -> str:
        req = json.loads(request)
        boards = self._load_boards()
        board_id = req.get('board_id')
        
        board = boards.get(board_id)
        if not board or board['status'] != "OPEN":
            raise ValueError("Can only add tasks to an OPEN board")
            
        if any(t['title'] == req['title'] for t in board['tasks'].values()):
            raise ValueError("Task title must be unique for this board")

        task_id = str(uuid.uuid4())
        board['tasks'][task_id] = {
            "id": task_id,
            "title": req['title'],
            "description": req['description'],
            "user_id": req['user_id'],
            "status": "OPEN",
            "creation_time": req.get('creation_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        self._save_boards(boards)
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str) -> str:
        req = json.loads(request)
        boards = self._load_boards()
        task_id = req.get('id')
        new_status = req.get('status')
        
        for board in boards.values():
            if task_id in board['tasks']:
                board['tasks'][task_id]['status'] = new_status
                self._save_boards(boards)
                return json.dumps({"status": "success"})
        
        raise KeyError("Task not found")

    def close_board(self, request: str) -> str:
        req = json.loads(request)
        board_id = req.get('id')
        boards = self._load_boards()
        
        if board_id not in boards:
            raise KeyError("Board not found")
            
        board = boards[board_id]
        # Constraint: All tasks must be COMPLETE to close board
        for task in board['tasks'].values():
            if task['status'] != "COMPLETE":
                raise ValueError("All tasks must be COMPLETE before closing the board")
        
        board['status'] = "CLOSED"
        board['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_boards(boards)
        return json.dumps({"status": "success"})

    def export_board(self, request: str) -> str:
        req = json.loads(request)
        board_id = req.get('id')
        boards = self._load_boards()
        
        if board_id not in boards:
            raise KeyError(f"Board with ID {board_id} not found.")
            
        board = boards[board_id]
        file_name = f"board_report_{board['name'].replace(' ', '_')}_{board_id[:8]}.txt"
        file_path = os.path.join('out', file_name)
            
        with open(file_path, "w") as f:
            f.write("="*60 + "\n")
            f.write(f"{'PROJECT BOARD TASK REPORT':^60}\n")
            f.write("="*60 + "\n\n")
            f.write(f"BOARD NAME   : {board.get('name')}\n")
            f.write(f"DESCRIPTION  : {board.get('description')}\n")
            f.write(f"TEAM ID      : {board.get('team_id')}\n")
            f.write(f"STATUS       : {board.get('status')}\n")
            f.write(f"CREATED AT   : {board.get('creation_time')}\n")
            f.write(f"END TIME     : {board.get('end_time', 'N/A (Board still open)')}\n")
            f.write("\n" + "-"*60 + "\n")
            f.write(f"{'TASK TITLE':<25} | {'STATUS':<15} | {'ASSIGNED USER'}\n")
            f.write("-" * 60 + "\n")
            
            tasks = board.get('tasks', {})
            if not tasks:
                f.write("No tasks found on this board.\n")
            else:
                for task in tasks.values():
                    title = (task['title'][:22] + '..') if len(task['title']) > 22 else task['title']
                    f.write(f"{title:<25} | {task['status']:<15} | {task['user_id']}\n")
            
            f.write("="*60 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        return json.dumps({"out_file": file_name})