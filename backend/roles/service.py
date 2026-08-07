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

def save_role(self, role):

    self.database.execute(
        """
        INSERT OR REPLACE INTO roles
        (
            role_id,
            role_name,
            description,
            level,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            role.role_id,
            role.role_name,
            role.description,
            role.level,
            role.status,
            role.created_at,
            role.updated_at,
        ),
    )
