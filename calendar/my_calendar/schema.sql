CREATE TABLE IF NOT EXISTS task_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL
);

INSERT INTO task_status (status) VALUES ("Открыто");
INSERT INTO task_status (status) VALUES ("Завершено");

CREATE TABLE IF NOT EXISTS calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    due_date DATETIME NOT NULL,
    status_id INTEGER DEFAULT 1,
    FOREIGN KEY (status_id) REFERENCES task_status (id)
);

