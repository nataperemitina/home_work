CREATE TABLE IF NOT EXISTS calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    due_date DATETIME NOT NULL,
    status TEXT NOT NULL DEFAULT 'Открыто'
);

