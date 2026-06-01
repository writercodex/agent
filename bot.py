from database import get_connection

print("Testing database connection...")

conn = get_connection()

print("Database connected!")

conn.close()
