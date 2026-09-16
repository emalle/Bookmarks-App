import sqlite3

conn = sqlite3.connect("bookmarks.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS folders(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL DEFAULT 1 REFERENCES users(id),
    parent_id INTEGER REFERENCES folders(id),
    name TEXT NOT NULL,
    UNIQUE(user_id, parent_id, name)
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL DEFAULT 1 REFERENCES users(id),
        folder_id INTEGER REFERENCES folders(id),
        url TEXT NOT NULL,
        title TEXT, 
        description TEXT,
        is_important BOOLEAN DEFAULT 0,
        is_alive BOOLEAN DEFAULT 1,
        last_checked_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, url)
        )
    """)

conn.execute("""
    CREATE TABLE IF NOT EXISTS tags(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL DEFAULT 1 REFERENCES users(id),
        name TEXT NOT NULL, 
        UNIQUE(user_id, name)
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS bookmark_tags(
        bookmark_id INTEGER REFERENCES bookmarks(id)ON DELETE CASCADE,
        tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE, 
        PRIMARY KEY (bookmark_id, tag_id)
    )
""")   

conn.commit()
conn.close()
print("Database and tables created successfully.:)")
