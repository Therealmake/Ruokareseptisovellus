import db

def add_recipe(recipe_name, ingredients, instructions, user_id):
    sql = """INSERT INTO recipes (recipe_name, ingredients, instructions, user_id)
                VALUES (?, ?, ?, ?)"""
    db.execute(sql, [recipe_name, ingredients, instructions, user_id])

def get_recipes():
    sql = "SELECT id, recipe_name FROM recipes ORDER BY id"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT R.recipe_name, R.ingredients, R.instructions, U.username
            FROM recipes R, users U
            WHERE R.user_id = U.id AND R.id = ?"""
    return db.query(sql, [recipe_id])[0]