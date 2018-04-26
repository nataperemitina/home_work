CREATE TABLE IF NOT EXISTS task_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL
) 

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    due_date DATETIME NOT NULL,
    task_status_id INTEGER,
    FOREIGN KEY (task_status_id) REFERENCES task_status (id)
)

