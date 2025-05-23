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

def add_recipe(recipe_name, ingredients, instructions, category, diets, image, user_id):
    sql = """INSERT INTO recipes (recipe_name,
                                    ingredients,
                                    instructions,
                                    category,
                                    diet,
                                    image,
                                    user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [recipe_name, ingredients, instructions, category, diets, image, user_id])

def get_recipes(page, page_size):
    sql = """SELECT R.id,
                    R.recipe_name,
                    U.id user_id,
                    U.username,
                    COUNT(C.id) comment_count
                FROM recipes R JOIN users U ON R.user_id = U.id
                    LEFT JOIN comments C ON R.id = C.recipe_id
                GROUP BY R.id
                ORDER BY R.id DESC
                LIMIT ? OFFSET ?"""
    limit = page_size
    offset = (page - 1) * page_size
    return db.query(sql, [limit, offset])

def get_recipe(recipe_id):
    sql = """SELECT R.id,
                    R.recipe_name,
                    R.ingredients,
                    R.instructions,
                    R.category,
                    R.diet,
                    R.image,
                    U.username,
                    U.id user_id
                FROM recipes R, users U
                WHERE R.user_id = U.id AND R.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def get_image(recipe_id):
    sql = "SELECT image FROM recipes WHERE id = ?"
    result = db.query(sql, [recipe_id])
    return result[0][0] if result else None

def update_recipe(recipe_id, recipe_name, ingredients, instructions, category, diets, image):
    if image is not None:
        # Update image
        sql = """UPDATE recipes SET recipe_name = ?,
                                    ingredients = ?,
                                    instructions = ?,
                                    category = ?,
                                    diet = ?,
                                    image = ?
                                WHERE id = ?"""
        db.execute(sql, [recipe_name, ingredients, instructions, category, diets, image, recipe_id])
    else:
        # Don't update image
        sql = """UPDATE recipes SET recipe_name = ?,
                                    ingredients = ?,
                                    instructions = ?,
                                    category = ?,
                                    diet = ?
                                WHERE id = ?"""
        db.execute(sql, [recipe_name, ingredients, instructions, category, diets, recipe_id])

def delete_image(recipe_id, image):
    sql = "UPDATE recipes SET image = ? WHERE id = ?"
    db.execute(sql, [image, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM comments WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def search_recipes(query):
    sql = """SELECT R.id,
                    R.recipe_name,
                    U.id user_id,
                    U.username,
                    COUNT(C.id) comment_count
                FROM recipes R JOIN users U ON R.user_id = U.id
                    LEFT JOIN comments C ON R.id = C.recipe_id
                WHERE R.recipe_name LIKE ? OR R.ingredients LIKE ?
                GROUP BY R.id, U.id, U.username
                ORDER BY R.id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def count_recipes():
    sql = "SELECT count(id) FROM recipes"
    result = db.query(sql)
    return result[0][0]
