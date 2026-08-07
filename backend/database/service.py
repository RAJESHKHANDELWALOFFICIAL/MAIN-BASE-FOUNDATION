CREATE TABLE IF NOT EXISTS master_identity (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    master_id TEXT UNIQUE,
    identity_id TEXT UNIQUE,
    supreme_id TEXT,

    full_name TEXT,
    display_name TEXT,
    username TEXT UNIQUE,

    email TEXT,
    phone TEXT,

    country TEXT,
    state TEXT,
    city TEXT,

    language TEXT,
    timezone TEXT,

    status TEXT,
    verified INTEGER,

    profile_photo TEXT,
    profile_type TEXT,

    version TEXT,

    created_at TEXT,
    updated_at TEXT

)
