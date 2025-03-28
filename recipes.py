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
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def update_recipe(recipe_id, recipe_name, ingredients, instructions):
    sql = """UPDATE recipes SET recipe_name = ?,
                                ingredients = ?,
                                instructions = ?
                            WHERE id = ?"""
    db.execute(sql, [recipe_name, ingredients, instructions, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def search_recipes(query):
    sql = """SELECT id, recipe_name
            FROM recipes
            WHERE recipe_name LIKE ? OR ingredients LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])