import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM comments")

user_count = 1000
recipe_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, recipe_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO recipes (recipe_name, user_id) VALUES (?, ?)",
               ["recipe" + str(i), user_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, recipe_count)
    db.execute("""INSERT INTO comments (recipe_id, user_id, comment)
                  VALUES (?, ?, ?)""",
               [recipe_id, user_id, "message" + str(i)])

db.commit()
db.close()
