print("STEP 1")

from database import get_connection

print("STEP 2")

conn = get_connection()

print("STEP 3")

conn.close()

print("STEP 4")
