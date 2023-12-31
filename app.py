from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL Server connection config
server = 'sqlserver'
database = 'master'
username = 'SA'
password = 'YourStrong@Passw0rd'
port = 14500

# Initialize cursor globally
conn = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server; SERVER={server};DATABASE={database};UID={username};PWD={password};PORT={port}', autocommit=True)
cursor = conn.cursor()


# Use the logging module to add a log statement
try:
    print("Successfully connected to the database.")
except pyodbc.Error as e:
    print("Error connecting to the database: %s" % str(e))

# Create 'recipe_sharing' database if it doesn't exist
try:
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'recipe_sharing') CREATE DATABASE recipe_sharing")
    print("Successfully created 'recipe_sharing' database.")
except pyodbc.Error as e:
    print("Error creating 'recipe_sharing' database: %s" % str(e))

# Use the 'recipe_sharing' database
cursor.execute("USE recipe_sharing")

# Create 'Recipes' table if it doesn't exist
try:
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Recipes') CREATE TABLE Recipes (recipe_id INT IDENTITY(1,1) PRIMARY KEY, name VARCHAR(50) NOT NULL, ingredients TEXT, steps TEXT, preparation_time INT)")
    print("Successfully created 'Recipes' table.")
except pyodbc.Error as e:
    print("Error creating 'Recipes' table: %s" % str(e))

# Create 'Comments' table if it doesn't exist
try:
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Comments') CREATE TABLE Comments (id INT IDENTITY(1,1) PRIMARY KEY, recipe_id INT, comment_text TEXT, FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id))")
    print("Successfully created 'Comments' table.")
except pyodbc.Error as e:
    print("Error creating 'Comments' table: %s" % str(e))

# Create 'Ratings' table if it doesn't exist
try:
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Ratings') CREATE TABLE Ratings (id INT IDENTITY(1,1) PRIMARY KEY, recipe_id INT, rating_value INT, FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id))")
    print("Successfully created 'Ratings' table.")
except pyodbc.Error as e:
    print("Error creating 'Ratings' table: %s" % str(e))


# API endpoint to add recipes and get recipes
@app.route("/recipes", methods=['POST', 'GET'])
def recipes():
    if request.method == 'POST':
        name = request.json['name']
        ingredients = request.json['ingredients']
        steps = request.json['steps']
        preparation_time = request.json['preparation_time']

        cursor.execute(
            "INSERT INTO Recipes (name, ingredients, steps, preparation_time) VALUES (?, ?, ?, ?)",
            (name, ingredients, steps, preparation_time))
        conn.commit()

        return jsonify({
            "message": "Recipe added successfully!"
        })

    elif request.method == 'GET':
        cursor.execute("SELECT * FROM Recipes ORDER BY recipe_id DESC")
        recipes = cursor.fetchall()

        recipe_list = []
        for recipe in recipes:
            recipe_dict = {
                'recipe_id': recipe.recipe_id,
                'name': recipe.name,
                'ingredients': recipe.ingredients,
                'steps': recipe.steps,
                'preparation_time': recipe.preparation_time
            }
            recipe_list.append(recipe_dict)

        return jsonify(recipe_list)

# API endpoint to update or delete the recipe
@app.route("/recipes/<int:recipe_id>", methods=['GET', 'PUT', 'DELETE'])
def recipe(recipe_id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Recipes WHERE recipe_id = ?", (recipe_id,))
        recipe = cursor.fetchone()

        if recipe:
            recipe_dict = {
                'recipe_id': recipe.recipe_id,
                'name': recipe.name,
                'ingredients': recipe.ingredients,
                'steps': recipe.steps,
                'preparation_time': recipe.preparation_time
            }
            return jsonify(recipe_dict)
        else:
            return jsonify({"message": "Recipe not found"}), 404

    elif request.method == 'PUT':
        name = request.json['name']
        ingredients = request.json['ingredients']
        steps = request.json['steps']
        preparation_time = request.json['preparation_time']

        cursor.execute(
            "UPDATE Recipes SET name=?, ingredients=?, steps=?, preparation_time=? WHERE recipe_id=?",
            (name, ingredients, steps, preparation_time, recipe_id))
        conn.commit()

        return jsonify({"message": "Recipe updated successfully!"})

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM Recipes WHERE recipe_id = ?", (recipe_id,))
        conn.commit()

        return jsonify({"message": "Recipe deleted successfully!"})

# API endpoint to add ratings to the recipe
@app.route("/recipes/<int:recipe_id>/ratings", methods=['POST'])
def add_rating(recipe_id):
    if request.method == 'POST':
        rating_value = request.json['rating_value']

        if not (1 <= rating_value <= 5):
            return jsonify({"message": "Invalid rating. Please provide a rating between 1 and 5"}), 400

        cursor.execute("INSERT INTO Ratings (recipe_id, rating_value) VALUES (?, ?)", (recipe_id, rating_value))
        conn.commit()

        return jsonify({"message": "Rating added successfully!"})

# API endpoint to add and retrieve comments for the recipe
@app.route("/recipes/<int:recipe_id>/comments", methods=['POST', 'GET'])
def recipe_comments(recipe_id):
    if request.method == 'POST':
        comment_text = request.json['comment_text']

        cursor.execute("INSERT INTO Comments (recipe_id, comment_text) VALUES (?, ?)", (recipe_id, comment_text))
        conn.commit()

        return jsonify({"message": "Comment added successfully!"})

    elif request.method == 'GET':
        cursor.execute("SELECT * FROM Comments WHERE recipe_id = ?", (recipe_id,))
        comments = cursor.fetchall()

        comment_list = []
        for comment in comments:
            comment_dict = {
                'id': comment.id,
                'recipe_id': comment.recipe_id,
                'comment_text': comment.comment_text
            }
            comment_list.append(comment_dict)

        return jsonify(comment_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')