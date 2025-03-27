import db

def add_recipe(recipe_name, ingredients, instructions, user_id):
    sql = """INSERT INTO recipes (recipe_name, ingredients, instructions, user_id)
                VALUES (?, ?, ?, ?)"""
    db.execute(sql, [recipe_name, ingredients, instructions, user_id])

def get_recipes():
    sql = "SELECT id, recipe_name FROM recipes ORDER BY id"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT R.id,
                    R.recipe_name,
                    R.ingredients,
                    R.instructions,
                    U.username,
                    U.id user_id
            FROM recipes R, users U
            WHERE R.user_id = U.id AND R.id = ?"""
    return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, recipe_name, ingredients, instructions):
    sql = """UPDATE recipes SET recipe_name = ?,
                                ingredients = ?,
                                instructions = ?
                            WHERE id = ?"""
    db.execute(sql, [recipe_name, ingredients, instructions, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])