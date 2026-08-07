CREATE TABLE IF NOT EXISTS master_identity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id TEXT UNIQUE,
    full_name TEXT,
    display_name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    status TEXT
)
