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


def save_memory(key, value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO memories(memory_key, memory_value)
    VALUES (%s, %s)
    ON CONFLICT (memory_key)
    DO UPDATE SET
        memory_value = EXCLUDED.memory_value
    """, (key, value))

    conn.commit()

    cur.close()
    conn.close()


def get_memory(key):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT memory_value FROM memories WHERE memory_key=%s",
        (key,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return None
