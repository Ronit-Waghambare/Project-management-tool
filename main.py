import json
from implementation.usermanager import UserManager
from implementation.teammanager import TeamManager
from implementation.boardmanager import BoardManager

def main():
    # Initialize all APIs
    user_api = UserManager()
    team_api = TeamManager()
    board_api = BoardManager()

    while True:
        print("\n" + "="*30)
        print("  TEAM PROJECT PLANNER MENU")
        print("="*30)
        print("1. Manage Users (Create/List)")
        print("2. Manage Teams (Create/List/Add Members)")
        print("3. Manage Boards (Create/List/Export)")
        print("4. Manage Tasks (Add/Update Status)")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")

        try:
            if choice == '1':
                sub_choice = input("1a. Create User\n1b. List Users\nChoice: ")
                if sub_choice == '1a':
                    name = input("Username: ")
                    d_name = input("Display Name: ")
                    resp = user_api.create_user(json.dumps({"name": name, "display_name": d_name}))
                    print(f"Created! ID: {json.loads(resp)['id']}")
                elif sub_choice == '1b':
                    print(user_api.list_users())

            elif choice == '2':
                sub_choice = input("2a. Create Team\n2b. Add User to Team\n2c. List Teams\nChoice: ")
                if sub_choice == '2a':
                    name = input("Team Name: ")
                    desc = input("Description: ")
                    admin = input("Admin User ID: ")
                    resp = team_api.create_team(json.dumps({"name": name, "description": desc, "admin": admin}))
                    print(f"Team Created! ID: {json.loads(resp)['id']}")
                elif sub_choice == '2b':
                    t_id = input("Team ID: ")
                    u_ids = input("Enter User IDs (comma separated): ").split(",")
                    team_api.add_users_to_team(json.dumps({"id": t_id, "users": [uid.strip() for uid in u_ids]}))
                    print("Users added!")

            elif choice == '3':
                sub_choice = input("3a. Create Board\n3b. Close Board\n3c. Export Board\nChoice: ")
                if sub_choice == '3a':
                    name = input("Board Name: ")
                    desc = input("Description: ")
                    t_id = input("Team ID: ")
                    resp = board_api.create_board(json.dumps({
                        "name": name, "description": desc, "team_id": t_id, 
                        "creation_time": "2024-01-01 00:00:00"
                    }))
                    print(f"Board Created! ID: {json.loads(resp)['id']}")
                elif sub_choice == '3c':
                    b_id = input("Board ID to Export: ")
                    resp = board_api.export_board(json.dumps({"id": b_id}))
                    print(f"Exported to: {json.loads(resp)['out_file']}")

            elif choice == '4':
                sub_choice = input("4a. Add Task\n4b. Update Task Status\nChoice: ")
                if sub_choice == '4a':
                    b_id = input("Board ID: ")
                    title = input("Task Title: ")
                    desc = input("Task Description: ")
                    u_id = input("Assignee User ID: ")
                    resp = board_api.add_task(json.dumps({
                        "board_id": b_id, "title": title, 
                        "description": desc, "user_id": u_id,
                        "creation_time": "2024-01-01 00:00:00"
                    }))
                    print(f"Task Added! ID: {json.loads(resp)['id']}")
                elif sub_choice == '4b':
                    t_id = input("Task ID: ")
                    stat = input("New Status (OPEN/IN_PROGRESS/COMPLETE): ")
                    board_api.update_task_status(json.dumps({"id": t_id, "status": stat}))
                    print("Status Updated!")

            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid Choice!")

        except Exception as e:
            print(f"\n[ERROR]: {e}")

if __name__ == "__main__":
    main()