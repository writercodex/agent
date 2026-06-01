import time

from memory import init_db, save_memory, get_memory

print("Initializing memory system...")

init_db()

save_memory("owner_name", "Jhon")

name = get_memory("owner_name")

print(f"Memory result: {name}")

time.sleep(60)
