from recipes_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from recipes_app.models.users import Users
from recipes_app.models.recipes import Recipe

@app.route('/recipes')
def show_recipes():
    if "logged_in" not in session:
        return redirect ('/login')
    
    user = Users.get_one_by_id(session["logged_in"])

    recipes = Recipe.get_all_with_user()
    return render_template('recipes.html', user=user, recipes=recipes)

@app.route('/recipes/new')
def new_recipe():
    if "logged_in" not in session:
        return redirect ('/login')
    if "errors" in session and session["errors"] == True:
        name  = session.pop("name", None)
        description= session.pop("description", None)
        instructions = session.pop("instructions", None)
        date_made = session.pop("date_made", None)
        under_30 = session.pop("under_30", None)
        session["errors"] = False
        return render_template('new_recipe.html', name=name, description=description, instructions=instructions, date_made=date_made, under_30=under_30)

    return render_template('new_recipe.html')

@app.route('/recipes/new/process', methods=['POST'])
def add_new_recipe():
    if not Recipe.validate_recipe(request.form):
        session["errors"] = True
        session["name"]= request.form["name"]
        session["description"]= request.form["description"]
        session["instructions"]= request.form["instructions"]
        session["date_made"]= request.form["date_made"]
        session["under30"]= request.form["under30"]
        return redirect("/recipes/new")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under30": request.form["under30"],
        "user_id": session["logged_in"]
    }
    Recipe.save(data)
    return redirect('/recipes')

@app.route('/recipes/view/<int:recipe_id>')
def view_recipe(recipe_id):
    if "logged_in" not in session:
        return redirect ('/login')
    data = {
        "id": recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    name = Users.get_one_by_id(session["logged_in"]).first_name
    return render_template('view_recipe.html', recipe=recipe, name=name)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    
    if "logged_in" not in session:
        return redirect ('/login')
    
    data = {
        "id": recipe_id
    }
    recipe = Recipe.get_one_recipe(data)

    if "errors" in session and session["errors"] == True:
        recipe.name = session.pop("name", None)
        recipe.description = session.pop("description", None)
        recipe.instructions = session.pop("instructions", None)
        recipe.date_made = session.pop("date_made", None)
        recipe.under30 = session.pop("under_30", None)
        session["errors"] = False
        return render_template('edit_recipe.html', recipe=recipe)
    
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/edit/<int:recipe_id>/process', methods=['POST'])
def edit_recipe_process(recipe_id):
    if not Recipe.validate_recipe(request.form):
        session["errors"] = True
        session["name"]= request.form["name"]
        session["description"]= request.form["description"]
        session["instructions"]= request.form["instructions"]
        session["date_made"]= request.form["date_made"]
        session["under30"]= request.form["under30"]
        return redirect(f"/recipes/edit/{recipe_id}")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under30": request.form["under30"],
        "id": recipe_id
    }
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data = {"id": recipe_id}
    Recipe.delete(data)
    return redirect('/recipes')