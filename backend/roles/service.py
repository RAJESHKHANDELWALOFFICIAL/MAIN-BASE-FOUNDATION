self.database.execute("""
CREATE TABLE IF NOT EXISTS roles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    role_id TEXT UNIQUE,
    role_name TEXT UNIQUE,

    description TEXT,

    level INTEGER,

    status TEXT,

    created_at TEXT,
    updated_at TEXT

)
""")
