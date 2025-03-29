import db

def get_all_categories():
    sql = "SELECT name FROM categories ORDER BY id"
    result = db.query(sql)
    return result

def get_all_diets():
    sql = "SELECT name FROM diets ORDER BY id"
    result = db.query(sql)
    return result

def add_comment(recipe_id, user_id, comment):
    sql = """INSERT INTO comments (recipe_id, user_id, comment)
                VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, comment])

def get_comments(recipe_id):
    sql = """SELECT C.comment, U.id user_id, U.username, C.id
                FROM comments C, users U 
                WHERE C.user_id = U.id AND C.recipe_id = ?
                ORDER BY C.id DESC"""
    return db.query(sql, [recipe_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_comment(comment_id):
    sql = "SELECT * FROM comments WHERE id = ?"
    result =  db.query(sql, [comment_id])
    return result[0] if result else None

def add_recipe(recipe_name, ingredients, instructions, category, diet, user_id):
    sql = """INSERT INTO recipes (recipe_name, ingredients, instructions, category, diet, user_id)
            VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [recipe_name, ingredients, instructions, category, diet, user_id])

def get_recipes():
    sql = "SELECT id, recipe_name FROM recipes ORDER BY id DESC"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT R.id,
                    R.recipe_name,
                    R.ingredients,
                    R.instructions,
                    R.category,
                    R.diet,
                    U.username,
                    U.id user_id
            FROM recipes R, users U
            WHERE R.user_id = U.id AND R.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def update_recipe(recipe_id, recipe_name, ingredients, instructions, category, diet):
    sql = """UPDATE recipes SET recipe_name = ?,
                                ingredients = ?,
                                instructions = ?,
                                category = ?,
                                diet = ?
                            WHERE id = ?"""
    db.execute(sql, [recipe_name, ingredients, instructions, category, diet, recipe_id])

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