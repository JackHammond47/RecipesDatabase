# Overview

This program was created to practice connecting database languages like MySQL to other languages with more options such as  reating functions. I developed a simple recipe database using MySQL connector and python. The program is used by creating a dictionary of ingredients (with ingredient ID, quantity, and unit), a list of instructions, and then calling the add recipe with recipe title, Recipe ID, ingredients dictionary, and instructions list. THe categories, ingredients and functions can be easily changed to adapt to the needs of whatever cook is using the program.

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

I am using MySQL as I am most familiar with the syntax and structure. The database has 5 tables, category, ingredient, ingredientlist, instruction, and recipe. The recipe table includes the name, category_id and recipe_id. The primary key recipe_id links all the tables together. The ingredientlist table contains an ingr_id, quantity and unit with the recipe_id as a foreign key and the instruction table contains step_number, instruction_text and again the recipe_id as a foreign key. The ingredient table contains all the ingredients with their own key same with the category table. The ingredientlist table contains ingr_id's and the recipe table has the category_id's.

# Development Environment

I used python, MySQL, and MySQL connector to execute SQL commands from python. I created a local MySQL server with a generic user "root" and password "password" for demonstration purposes. The program connects to this server and uses the database recipe_db so anyone who wants to try this code out for themselves will need to modify the code on lines 19-22 for whatever server and database they are using.


# Useful Websites

- [w3 schools MySQL connector guide](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- ["Learning SQL", 3rd Edition by Alan Beaulieu](https://www.oreilly.com/library/view/learning-sql-3rd/9781492057604/)

# Future Work

- Look into the cost and difficulty of setting up a dedicated MySQL server so all users can connect without modifying this code.
- Add more recipes to actually use as a virtual cookbook.
- Add user input functionality or research more secure ways to interact with the database.