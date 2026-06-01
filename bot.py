from memory import init_db, save_memory, get_memory

print("STEP 1")

init_db()

print("STEP 2")

save_memory("owner_name", "Jhon")

print("STEP 3")

name = get_memory("owner_name")

print(f"RESULT = {name}")

print("STEP 4")
