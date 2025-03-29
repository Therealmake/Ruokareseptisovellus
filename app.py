import sqlite3
import db
import config
import recipes
import users

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_category_and_diets(selected_category, selected_diets, categories, diets):
    valid_categories = [category["name"] for category in categories]
    if selected_category and selected_category not in valid_categories:
        abort(403)

    valid_diets = [diet["name"] for diet in diets]
    if selected_diets:
        if any(diet not in valid_diets for diet in selected_diets):
            abort(403)

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)

@app.route("/search_recipe")
def search_recipe():
    query = request.args.get("query")
    if len(query) >= 100:
        abort(403)
    if query:
        results = recipes.search_recipes(query)
    else:
        query = ""
        results = []
    return render_template("search_recipe.html", query=query, results=results)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    comments = recipes.get_comments(recipe_id)
    return render_template("show_recipe.html", recipe=recipe, comments=comments)

@app.route("/image/<int:recipe_id>")
def show_image(recipe_id):
    image = recipes.get_image(recipe_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    comment = request.form.get("comment")
    if not comment:
        abort(403)
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    user_id = session["user_id"]

    recipes.add_comment(recipe_id, user_id, comment)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()
    comment = recipes.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)
    recipe_id = comment["recipe_id"]
    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)
    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_comment(comment_id)
            return redirect("/recipe/" + str(recipe_id))
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/new_recipe")
def new_recipe():
    require_login()
    categories = recipes.get_all_categories()
    diets = recipes.get_all_diets()
    return render_template("new_recipe.html", categories=categories, diets=diets)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    categories = recipes.get_all_categories()
    diets = recipes.get_all_diets()
    recipe_name = request.form["recipe_name"]
    if not recipe_name or len(recipe_name) > 50:
        abort(403)
    ingredients = request.form["ingredients"]
    if not ingredients or len(ingredients) > 200:
        abort(403)
    instructions = request.form["instructions"]
    if not instructions or len(instructions) > 2000:
        abort(403)
    user_id = session["user_id"]
    selected_category = request.form["category"]
    selected_diets = request.form.getlist("diet")
    check_category_and_diets(selected_category, selected_diets, categories, diets)

    diets = ", ".join(request.form.getlist("diet"))
    file = request.files["image"]
    if file and file.filename != "":
        if not file.filename.lower().endswith(".jpg"):
            abort(403)
        image = file.read()
    else:
        image = None
    recipes.add_recipe(recipe_name, ingredients, instructions, selected_category, diets, image, user_id)
    recipe_id = db.last_insert_id()
    return redirect("/recipe/" + str(recipe_id))

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)
    categories = recipes.get_all_categories()
    diets = recipes.get_all_diets()
    selected_category = recipe["category"]
    selected_diets = [diet.strip() for diet in recipe["diet"].split(",")] if recipe["diet"] else []
    return render_template("edit_recipe.html", recipe=recipe, categories=categories,
                           diets=diets, selected_category=selected_category,
                           selected_diets=selected_diets)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    categories = recipes.get_all_categories()
    diets = recipes.get_all_diets()
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if recipe["user_id"] != session["user_id"]:
        abort(403)
    recipe_name = request.form["recipe_name"]
    if not recipe_name or len(recipe_name) > 50:
        abort(403)
    ingredients = request.form["ingredients"]
    if not ingredients or len(ingredients) > 200:
        abort(403)
    instructions = request.form["instructions"]
    selected_category = request.form["category"]
    selected_diets = request.form.getlist("diet")
    check_category_and_diets(selected_category, selected_diets, categories, diets)

    diets = ", ".join(request.form.getlist("diet"))
    image = None
    file = request.files["image"]
    if file and file.filename != "":
        if not file.filename.lower().endswith(".jpg"):
            abort(403)
        image = file.read()
    delete_image = request.form.get("delete_image")
    if delete_image:
        image = None
        recipes.delete_image(recipe_id, image)
    recipes.update_recipe(recipe_id, recipe_name, ingredients,
                          instructions, selected_category, diets, image)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)
    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.validate_user_credentials(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")