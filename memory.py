from database import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id SERIAL PRIMARY KEY,
        memory_key TEXT UNIQUE,
        memory_value TEXT
    )
    """)

    conn.commit()

    cur.close()
    conn.close()
