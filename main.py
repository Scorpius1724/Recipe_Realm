from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# Load the recipes from the CSV file
recipes = pd.read_csv("recipes.txt")

@app.route("/")
def home():
    # Display the home page
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").lower()
    # Filter recipes based on NER
    filtered_recipes = recipes[recipes['NER'].str.contains(query, case=False, na=False)]
    recipe_list = filtered_recipes["title"].tolist()
    return render_template("recipe_list.html", recipes=recipe_list)

@app.route("/recipe-list")
def recipe_list():
    # Display a list of recipe titles with links to their details
    recipe_list = recipes["title"].tolist()
    return render_template("recipe_list.html", recipes=recipe_list)

@app.route("/recipe/<int:index>")
def recipe(index):
    # Get the recipe details based on the index
    if index < len(recipes):
        recipe_details = recipes.iloc[index]
        # Parse the ingredients and directions from JSON strings
        ingredients = json.loads(recipe_details['ingredients'])
        directions = json.loads(recipe_details['directions'])
        return render_template("recipe.html", recipe=recipe_details, ingredients=ingredients, directions=directions)
    else:
        return "Recipe not found", 404

if __name__ == "__main__":
    app.run(debug=True)