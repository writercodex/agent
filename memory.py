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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversation_history (
        id SERIAL PRIMARY KEY,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id SERIAL PRIMARY KEY,
        summary_text TEXT
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


def delete_memory(key):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM memories WHERE memory_key=%s",
        (key,)
    )

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


def get_all_memories():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT memory_key, memory_value
    FROM memories
    ORDER BY memory_key
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def save_message(role, content):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO conversation_history(role, content)
    VALUES (%s, %s)
    """, (role, content))

    conn.commit()

    cur.close()
    conn.close()


def get_recent_messages(limit=100):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT role, content
    FROM conversation_history
    ORDER BY id DESC
    LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    rows.reverse()

    messages = []

    for role, content in rows:
        messages.append({
            "role": role,
            "content": content
        })

    return messages


def save_summary(summary_text):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM summaries")

    cur.execute(
        "INSERT INTO summaries(summary_text) VALUES (%s)",
        (summary_text,)
    )

    conn.commit()

    cur.close()
    conn.close()


def get_summary():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT summary_text
    FROM summaries
    LIMIT 1
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return ""
