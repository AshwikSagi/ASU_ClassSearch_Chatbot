import os

db_path = os.path.abspath("../database/class_search_bot.db")
print(f"Database path: {db_path}")
print(f"Exists: {os.path.exists(db_path)}")