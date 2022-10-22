from flask import request,jsonify
from flask_restx import Resource,fields,Namespace
from model import Recipe
from flask_jwt_extended import jwt_required

recipe_ns = Namespace("recipe",description="Recipe namespace")

recipe_model = recipe_ns.model(
    "Recipe",
    {   
        "id": fields.Integer(),
        "title": fields.String(),
        "description": fields.String()
    },
)

@recipe_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"Message":"Hello World"}


@recipe_ns.route('/recipes')
class RecipesResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return recipes

    @jwt_required()
    @recipe_ns.marshal_with(recipe_model)
    def post(self):
        data = request.get_json()

        new_recipe = Recipe(
            title = data.get('title'),
            description = data.get('description')
        )
        new_recipe.save()
        return new_recipe

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def get(self,id):
        recipe = Recipe.query.get_or_404(id)
        return recipe

    @jwt_required()    
    @recipe_ns.marshal_with(recipe_model)
    def put(self,id):
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'),data.get('description'))
        return recipe_to_update
    
    @jwt_required()
    @recipe_ns.marshal_with(recipe_model)
    def delete(self,id):
        recipe_to_delete = Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete
