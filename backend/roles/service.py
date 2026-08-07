self.database.execute("""
CREATE TABLE IF NOT EXISTS roles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    role_id TEXT UNIQUE NOT NULL,
    role_name TEXT UNIQUE NOT NULL,

    description TEXT,

    level INTEGER DEFAULT 1,

    status TEXT DEFAULT 'ACTIVE',

    created_at TEXT,
    updated_at TEXT

)
""")
