import mysql.connector
from mysql.connector import Error

# Author: Jack Hammond
#
# AI Citation for this AI Citationion:
# ChatGPT was used to help populate some of the functions I already wrote. Adding lines to manually run SQL code can get quite
# lengthy and time-consuming so after creating and testing the basic functions and functionality I copied my code 
# to ChatGPT and explained what I wanted with the get_recipe, modify_recipe, and delete_recipe functions and copied over the code.
# I, Jack Hammond, have used my own ideas for the database design and layout and have only used AI to help write some functions I
# already was familiar with to save time.

def create_connection():
    # I created a database named recipe_db on a local MySQL server 8.0
    # Connecting with default user "root" and password "password"
    # Added error handling in case problem connecting to the server
    try:
        connection = mysql.connector.connect(
            #change this for your own database server information
            host='localhost',
            database='recipe_db',
            user='root',
            password='password'
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database:", record)
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


def create_tables(connection):
    """ Create tables in the MySQL database """
    try:
        cursor = connection.cursor()
        
        # Drop existing tables to ensure the new structure
        drop_tables = """
        DROP TABLE IF EXISTS IngredientList, Instruction, Recipe, Ingredient, Category;
        """
        
        cursor.execute(drop_tables)
        
        # Create Category table
        create_category_table = """
        CREATE TABLE IF NOT EXISTS Category (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL
        );
        """
        
        # Create Recipe table
        create_recipe_table = """
        CREATE TABLE IF NOT EXISTS Recipe (
            recipe_id INT AUTO_INCREMENT PRIMARY KEY,
            recipe_name VARCHAR(255) NOT NULL,
            category_id INT,
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        );
        """
        
        # Create Ingredient table
        create_ingredient_table = """
        CREATE TABLE IF NOT EXISTS Ingredient (
            ingr_id INT AUTO_INCREMENT PRIMARY KEY,
            ingredient_name VARCHAR(255) NOT NULL
        );
        """
        
        # Create IngredientList table
        create_ingredient_list_table = """
        CREATE TABLE IF NOT EXISTS IngredientList (
            ingr_list_id INT AUTO_INCREMENT PRIMARY KEY,
            recipe_id INT,
            ingr_id INT,
            quantity DECIMAL(10, 2),
            measurement_unit VARCHAR(50),
            FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
            FOREIGN KEY (ingr_id) REFERENCES Ingredient(ingr_id)
        );
        """
        
        # Create Instruction table
        create_instruction_table = """
        CREATE TABLE IF NOT EXISTS Instruction (
            instruction_id INT AUTO_INCREMENT PRIMARY KEY,
            recipe_id INT,
            step_number INT NOT NULL,
            instruction_text TEXT NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
        );
        """
        
        # Execute table creation statements
        cursor.execute(create_category_table)
        cursor.execute(create_recipe_table)
        cursor.execute(create_ingredient_table)
        cursor.execute(create_ingredient_list_table)
        cursor.execute(create_instruction_table)
        
        connection.commit()
        print("Tables created successfully")
    
    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        cursor.close()

def add_category(connection, category_name):
    try:
        cursor = connection.cursor()
        
        # Check if the category already exists
        cursor.execute("SELECT category_id FROM Category WHERE category_name = %s", (category_name,))
        result = cursor.fetchone()
        
        if result:
            print(f"Category '{category_name}' already exists with ID {result[0]}")
        else:
            # Insert the category if it doesn't exist
            insert_category = "INSERT INTO Category (category_name) VALUES (%s)"
            cursor.execute(insert_category, (category_name,))
            connection.commit()
            print(f"Category '{category_name}' added successfully with ID {cursor.lastrowid}")
    except Error as e:
        print(f"Error adding category: {e}")
    finally:
        cursor.close()



def add_ingredient(connection, ingredient_name):
    try:
        cursor = connection.cursor()
        
        # Check if the ingredient already exists
        cursor.execute("SELECT ingr_id FROM Ingredient WHERE ingredient_name = %s", (ingredient_name,))
        result = cursor.fetchone()
        
        if result:
            print(f"Ingredient '{ingredient_name}' already exists with ID {result[0]}")
        else:
            # Insert the ingredient if it doesn't exist
            insert_ingredient = "INSERT INTO Ingredient (ingredient_name) VALUES (%s)"
            cursor.execute(insert_ingredient, (ingredient_name,))
            connection.commit()
            print(f"Ingredient '{ingredient_name}' added successfully with ID {cursor.lastrowid}")
    except Error as e:
        print(f"Error adding ingredient: {e}")
    finally:
        cursor.close()

def add_recipe(connection, recipe_name, category_id, ingredients, instructions):
    try:
        cursor = connection.cursor()
        # Insert recipe
        insert_recipe = "INSERT INTO Recipe (recipe_name, category_id) VALUES (%s, %s)"
        cursor.execute(insert_recipe, (recipe_name, category_id))
        recipe_id = cursor.lastrowid

        # Insert ingredients
        insert_ingredient = "INSERT INTO IngredientList (recipe_id, ingr_id, quantity, measurement_unit) VALUES (%s, %s, %s, %s)"
        for ingredient in ingredients:
            cursor.execute(insert_ingredient, (recipe_id, ingredient['ingr_id'], ingredient['quantity'], ingredient['measurement_unit']))

        # Insert instructions
        insert_instruction = "INSERT INTO Instruction (recipe_id, step_number, instruction_text) VALUES (%s, %s, %s)"
        for i, instruction in enumerate(instructions):
            cursor.execute(insert_instruction, (recipe_id, i + 1, instruction))

        connection.commit()
        print("Recipe added successfully")
    except Error as e:
        print(f"Error adding recipe: {e}")
    finally:
        cursor.close()

def get_recipe(connection, recipe_id):
    try:
        cursor = connection.cursor()
        
        # Get recipe details
        cursor.execute("SELECT * FROM Recipe WHERE recipe_id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        if recipe:
            print()
            print(f"Recipe ID: {recipe[0]}")
            print(f"Recipe Name: {recipe[1]}")
            print(f"Category ID: {recipe[2]}")
            
            # Get category name
            cursor.execute("SELECT category_name FROM Category WHERE category_id = %s", (recipe[2],))
            category = cursor.fetchone()
            if category:
                print(f"Category Name: {category[0]}")
            
            # Get ingredients with JOIN to get ingredient names
            cursor.execute("""
                SELECT il.ingr_list_id, il.recipe_id, i.ingredient_name, il.quantity, il.measurement_unit
                FROM IngredientList il
                JOIN Ingredient i ON il.ingr_id = i.ingr_id
                WHERE il.recipe_id = %s
            """, (recipe_id,))
            ingredients = cursor.fetchall()
            print("\nIngredients:")
            for ingredient in ingredients:
                print(f"- {ingredient[2]}: {ingredient[3]} {ingredient[4]}")
            
            # Get instructions
            cursor.execute("SELECT * FROM Instruction WHERE recipe_id = %s ORDER BY step_number", (recipe_id,))
            instructions = cursor.fetchall()
            print("\nInstructions:")
            for instruction in instructions:
                print(f"Step {instruction[2]}: {instruction[3]}")
            print()
        else:
            print("Recipe not found")
    except Error as e:
        print(f"Error retrieving recipe: {e}")
    finally:
        cursor.close()

def modify_recipe(connection, recipe_id, new_recipe_name=None, new_category_id=None, new_ingredients=None, new_instructions=None):
    try:
        cursor = connection.cursor()
        # Update recipe details
        if new_recipe_name or new_category_id:
            update_recipe = "UPDATE Recipe SET "
            if new_recipe_name:
                update_recipe += f"recipe_name = '{new_recipe_name}', "
            if new_category_id:
                update_recipe += f"category_id = {new_category_id}, "
            update_recipe = update_recipe.rstrip(', ')  # Remove trailing comma
            update_recipe += f" WHERE recipe_id = {recipe_id}"
            cursor.execute(update_recipe)

        # Update ingredients
        if new_ingredients:
            cursor.execute("DELETE FROM IngredientList WHERE recipe_id = %s", (recipe_id,))
            insert_ingredient = "INSERT INTO IngredientList (recipe_id, ingr_id, quantity, measurement_unit) VALUES (%s, %s, %s, %s)"
            for ingredient in new_ingredients:
                cursor.execute(insert_ingredient, (recipe_id, ingredient['ingr_id'], ingredient['quantity'], ingredient['measurement_unit']))

        # Update instructions
        if new_instructions:
            cursor.execute("DELETE FROM Instruction WHERE recipe_id = %s", (recipe_id,))
            insert_instruction = "INSERT INTO Instruction (recipe_id, step_number, instruction_text) VALUES (%s, %s, %s)"
            for i, instruction in enumerate(new_instructions):
                cursor.execute(insert_instruction, (recipe_id, i + 1, instruction))

        connection.commit()
        print("Recipe modified successfully")
    except Error as e:
        print(f"Error modifying recipe: {e}")
    finally:
        cursor.close()

def delete_recipe(connection, recipe_id):
    try:
        cursor = connection.cursor()
        # Delete from IngredientList
        cursor.execute("DELETE FROM IngredientList WHERE recipe_id = %s", (recipe_id,))
        # Delete from Instruction
        cursor.execute("DELETE FROM Instruction WHERE recipe_id = %s", (recipe_id,))
        # Delete from Recipe
        cursor.execute("DELETE FROM Recipe WHERE recipe_id = %s", (recipe_id,))
        connection.commit()
        print("Recipe deleted successfully")
    except Error as e:
        print(f"Error deleting recipe: {e}")
    finally:
        cursor.close()


def main():
    connection = create_connection()
    if connection:
        create_tables(connection)

        # Add categories
        add_category(connection, "Dessert")
        add_category(connection, "Main Course")
        add_category(connection, "Salad")

        # Add ingredients
        add_ingredient(connection, "Flour")
        add_ingredient(connection, "Sugar")
        add_ingredient(connection, "Butter")

        # Add a recipe
        ingredients = [
            {'ingr_id': 1, 'quantity': 200, 'measurement_unit': 'grams'},
            {'ingr_id': 2, 'quantity': 100, 'measurement_unit': 'grams'},
            {'ingr_id': 3, 'quantity': 50, 'measurement_unit': 'grams'}
        ]
        instructions = [
            "Preheat the oven to 350°F (175°C).",
            "Mix the dry ingredients together.",
            "Add wet ingredients and mix until smooth.",
            "Pour batter into a greased baking pan.",
            "Bake for 30-35 minutes or until a toothpick comes out clean."
        ]
        add_recipe(connection, "Chocolate Cake", 1, ingredients, instructions)

        # Retrieve a recipe
        get_recipe(connection, 1)

        # Modify a recipe
        new_ingredients = [
            {'ingr_id': 1, 'quantity': 250, 'measurement_unit': 'grams'},
            {'ingr_id': 2, 'quantity': 120, 'measurement_unit': 'grams'},
            {'ingr_id': 3, 'quantity': 70, 'measurement_unit': 'grams'}
        ]
        new_instructions = [
            "Preheat the oven to 375°F (190°C).",
            "Combine dry ingredients.",
            "Add wet ingredients and mix thoroughly.",
            "Pour mixture into a greased baking pan.",
            "Bake for 35-40 minutes or until a toothpick comes out clean."
        ]
        modify_recipe(connection, 1, new_recipe_name="Modified Chocolate Cake", new_ingredients=new_ingredients, new_instructions=new_instructions)

        # Retrieve the modified recipe
        get_recipe(connection, 1)

        # Delete a recipe
        delete_recipe(connection, 1)

        connection.close()
        print("MySQL connection is closed")

if __name__ == "__main__":
    main()
