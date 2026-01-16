# Project Board Management System

A robust back-end implementation for managing **Users**, **Teams**, and **Project Boards**. This system provides a clean API for team collaboration and task tracking, using a local JSON-based persistence layer.

---

## 🚀 Key Features

* **User Management**: Create, update, and track user profiles with unique name constraints.
* **Team Collaboration**: Organize users into teams (up to 50 members) with designated admins.
* **Task Boards**: Create project boards for teams, add tasks, and manage their lifecycle from `OPEN` to `COMPLETE`.
* **Automated Reporting**: Export detailed text-based board reports to the `out/` directory.
* **Self-Healing Database**: Automatic initialization of JSON storage and directory structures on startup.

---

## 🛠️ Technical Rationale

### **1. Architecture**
The system is built using a **Manager-based pattern**:
* `UserManager`: Handles user lifecycles and team lookups.
* `TeamManager`: Manages team compositions and membership constraints.
* `BoardManager`: Controls task state, board status, and report generation.

### **2. Constraint Enforcement**
To ensure data integrity, the system enforces the following:
* **Uniqueness**: User names, Team names, and Board names (per team) must be unique.
* **Status Guards**: Tasks can only be added to `OPEN` boards.
* **Closure Logic**: A board cannot be closed until all its associated tasks are marked as `COMPLETE`.

---

## 📁 Project Structure

```text
factwise-python/
├── implementation/           # Core logic classes
│   ├── __init__.py           # Package marker (Empty file)
│   ├── user_impl.py          # UserManager implementation
│   ├── team_impl.py          # TeamManager implementation
│   └── board_impl.py         # BoardManager implementation
├── db/                       # Auto-generated JSON databases
├── out/                      # Auto-generated export reports
├── user_base.py              # Provided Abstract Base Class
├── team_base.py              # Provided Abstract Base Class
├── project_board_base.py     # Provided Abstract Base Class
├── main.py                   # Entry point for testing
└── .gitignore                # Excludes cache and local data
```

## HOW TO RUN
Follow these steps to set up and execute the project locally:

## 1. Prerequisites
Ensure you have Python 3.8+ installed.

This project uses only standard Python libraries (json, os, uuid, datetime), so no external pip installations are required.

## 2. Setup (Optional)
It is recommended to use a virtual environment to keep your global Python environment clean:
Create a virtual environment

```text
python -m venv venv
```

Activate it (Windows)

```text
.\venv\Scripts\activate
```

Activate it (macOS/Linux)

```text
source venv/bin/activate
```

## 3. Execution
Run the main integration test script from the root directory:

```text
python main.py
```


