# Task Manager (CRUD App)

A minimal full-stack CRUD app.

- **Backend:** Python (Flask) + SQLite — exposes a REST API
- **Frontend:** Plain HTML/CSS/JavaScript (served by Flask, in `templates/index.html`)

## Features
- Create a task (title + optional description)
- Read/list all tasks
- Update a task (mark done / undo)
- Delete a task

## Project structure
```
crud_app/
├── app.py              # Flask backend + API routes
├── requirements.txt
├── templates/
│   └── index.html      # Frontend UI
└── tasks.db            # SQLite database (auto-created on first run)
```

## Setup & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Open your browser at:
   ```
   http://127.0.0.1:5000
   ```

The SQLite database file (`tasks.db`) is created automatically on first run.

## API Reference

| Method | Endpoint            | Description         |
|--------|----------------------|----------------------|
| GET    | `/api/tasks`         | List all tasks       |
| GET    | `/api/tasks/<id>`    | Get one task         |
| POST   | `/api/tasks`         | Create a task        |
| PUT    | `/api/tasks/<id>`    | Update a task        |
| DELETE | `/api/tasks/<id>`    | Delete a task        |

Example create request:
```bash
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2% please"}'
```
