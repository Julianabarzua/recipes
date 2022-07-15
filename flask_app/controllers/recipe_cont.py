from flask import flash, render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe_mod import Recipe
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/recipes")
def logedin():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    recipes = Recipe.get_all()
    usuarioLogeado = User.logedUser(data)
    return render_template("recipes.html", usuarioLogeado = usuarioLogeado, recipes = recipes)


@app.route("/recipes/new")
def new_recipe():
    print(session['user_id'])

    return render_template("new_recipe.html")

@app.route("/add_recipe", methods=['POST'])
def add_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date" : request.form["date"],
        "under30" : request.form["under30"],
        "owner_id" : session['user_id']
    }
    Recipe.save(data)
    return redirect("/recipes")

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    Recipe.delete(id=recipe_id)
    return redirect("/recipes")

@app.route("/recipes/<recipe_id>")
def show_recipe(recipe_id):
    
    recipe=Recipe.getonebyid(recipe_id)
    print(recipe)
    
    data = {
        "id":session['user_id']
    }
    usuarioLogeado = User.logedUser(data)

    return render_template("show.html", recipe=recipe, usuarioLogeado = usuarioLogeado)

@app.route("/recipes/edit/<recipe_id>")
def edit_recipe(recipe_id):
    recipe=Recipe.getonebyid(recipe_id)
    return render_template("edit.html", recipe=recipe)

@app.route("/recipes/update/<recipe_id>", methods=['POST'])
def update_recipe(recipe_id):

    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/edit/"+recipe_id)


    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date" : request.form["date"],
        "under30" : request.form["under30"],
    }
    Recipe.update_recipe(data, recipe_id)
    return redirect("/recipes")



