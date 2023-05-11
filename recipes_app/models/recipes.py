from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash, get_flashed_messages

class Recipe:
    DB = "recipes_erd"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']

    @classmethod
    def get_all_with_user(cls):
        query = "SELECT * FROM recipes JOIN users on users.id=recipes.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes
    
    @classmethod
    def get_one_recipe(cls, data):
        query  = "SELECT * FROM recipes JOIN users on users.id=recipes.user_id WHERE recipes.id = %(id)s";
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name, description, instructions, date_made, under30, created_at, updated_at, user_id ) VALUES ( %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, NOW() , NOW(), %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
        # the get_one method will be used when we need to retrieve just one specific row of the table
    
    @classmethod
    def update(cls, data):
        query = """UPDATE recipes
                SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under30=%(under30)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if "name" not in data or len(data["name"]) == 0:
            flash("Name field is required")
            is_valid = False
        elif len(data["name"]) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if "description" not in data or len(data["description"]) == 0:
            flash("Description field is required")
            is_valid = False
        elif len(data["description"]) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if "instructions" not in data or len(data["instructions"]) == 0:
            flash("Instructions field is required")
            is_valid = False
        elif len(data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False

        if "date_made" not in data or len(data["date_made"]) == 0:
            flash("Date Made is required")
            is_valid = False

        if "under30" not in data:
            flash("Is your Recipe under 30 minutes?")
            is_valid = False
        
        return is_valid

