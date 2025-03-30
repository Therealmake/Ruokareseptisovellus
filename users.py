from werkzeug.security import generate_password_hash, check_password_hash
import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_recipes(user_id):
    sql = """SELECT R.id, R.recipe_name, COUNT(C.id) comment_count
                FROM recipes R LEFT JOIN comments C ON C.recipe_id = R.id
                WHERE R.user_id = ?
                GROUP BY R.id
                ORDER BY R.id DESC"""
    return db.query(sql, [user_id])

def create_user(username, password1):
    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def validate_user_credentials(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id

    return None
