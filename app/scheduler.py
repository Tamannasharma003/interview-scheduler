import sqlite3

# connect to database
conn = sqlite3.connect("interview_scheduler.db")
cursor = conn.cursor()

# create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manager_name TEXT,
    candidate_name TEXT,
    time_slot TEXT
)
""")

# manager slots
manager_slots = ["10 AM", "11 AM", "3 PM"]

print("Available Interview Slots:")

for i, slot in enumerate(manager_slots, start=1):
    print(f"{i}. {slot}")

choice = int(input("Select a slot number: "))

selected_slot = manager_slots[choice - 1]

print("Interview scheduled at:", selected_slot)

# store interview in database
cursor.execute(
    "INSERT INTO interviews (manager_name, candidate_name, time_slot) VALUES (?, ?, ?)",
    ("Rahul", "Tamanna", selected_slot)
)

conn.commit()
conn.close()

print("Interview saved in database!")

