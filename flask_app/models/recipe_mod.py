from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.owner_id = data['owner_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_name = data['owner_name']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes (name, description, instructions, date_cooked, under_30, owner_id, created_at, updated_at ) VALUES (%(name)s,%(description)s,%(instructions)s,%(date)s,%(under30)s,%(owner_id)s, NOW() , NOW() );"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_all(cls):
        query = """SELECT recipes.id, name, description, instructions, date_cooked,  under_30, owner_id, recipes.created_at, recipes.updated_at, users.first_name as owner_name
        from recipes
        join users on owner_id = users.id;
                """
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def delete(cls, id ):
        query = "DELETE FROM recipes WHERE id ="+id+";"
        return connectToMySQL('recipes_schema').query_db( query)

    @classmethod
    def getonebyid(cls, id ):
        query = "SELECT recipes.id, name, description, instructions, date_cooked,  under_30, owner_id, recipes.created_at, recipes.updated_at, users.first_name as owner_name from recipes join users on owner_id = users.id WHERE recipes.id ="+id+";"
        
        recipe = connectToMySQL('recipes_schema').query_db( query)
        print(recipe)
        return recipe

    @classmethod
    def update_recipe(cls,data, id):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date)s,  under_30=%(under30)s, recipes.updated_at = NOW() WHERE recipes.id ="+id+";"
        return connectToMySQL('recipes_schema').query_db( query, data)

    @staticmethod
    def validate_recipe(recipe):

        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False

        return is_valid