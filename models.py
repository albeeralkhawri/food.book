from flask import Flask
from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, SmallInteger, String, Text, text, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from extensions import db, migrate
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password_input):
        if password_input == self.password:
            return True
        else:
            return False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return '<Category %r>' % self.category_name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, course_name):
        self.course_name = course_name

    def __repr__(self):
        return '<Course %r>' % self.course_name

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, cuisine_name):
        self.cuisine_name = cuisine_name

    def __repr__(self):
        return '<Cuisine %r>' % self.cuisine_name

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(String(150), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('authors', lazy=True))

    def __init__(self, author_name):
        self.author_name = author_name
    
    def __repr__(self):
        return '<Author %r>' % self.author_name

class Country(db.Model):
    id = Column(db.Integer, primary_key=True)
    country_name = db.Column(String(150), nullable=False, unique=True)
    
    def __init__(self, country_name):
        self.country_name = country_name
    
    def __repr__(self):
        return '<Country %r>' % self.country_name

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('methods', cascade="all,delete", lazy=True))
    method_description = db.Column(Text)

    def __init__(self, recipe, method_description):
        self.recipe = recipe
        self.method_description = method_description
        
    def __repr__(self):
        return '<Method %r>' % self.method_description

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))

    recipe_name = db.Column(String(150), nullable=False, unique=True)
    recipe_description = db.Column(Text)
    preparation_time = db.Column(db.Integer)
    cooking_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('recipes', lazy=True))
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('recipes', lazy=True))
    
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    cuisine = db.relationship('Cuisine', backref=db.backref('recipes', lazy=True))

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('recipes', lazy=True))

    image_filename = db.Column(db.String, default=None, nullable=True)
    image_url = db.Column(db.String, default=None, nullable=True)

    def __init__(self, user, recipe_name, recipe_description, preparation_time, cooking_time, servings, category, course, cuisine, author, image_filename, image_url):
        self.user = user
        self.recipe_name = recipe_name
        self.recipe_description = recipe_description
        self.preparation_time = preparation_time
        self.cooking_time = cooking_time
        self.servings = servings
        self.category = category
        self.course = course
        self.cuisine = cuisine
        self.author = author
        self.image_filename = image_filename
        self.image_url = image_url

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(String(150), nullable=False)

    def __init__(self, ingredient_name):
        self.ingredient_name = ingredient_name
    
    def __repr__(self):
        return '<Ingredient %r>' % self.ingredient_name


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_name = db.Column(String(150), nullable=False, unique=True)

    def __init__(self, measurement_name):
        self.measurement_name = measurement_name
    
    def __repr__(self):
        return '<Measurement %r>' % self.measurement_name


class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('quantities', cascade="all,delete", lazy=True))
    
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient = db.relationship('Ingredient', backref=db.backref('quantities', lazy=True))
    
    measurement_id = db.Column(db.Integer, db.ForeignKey('measurement.id'), nullable=False)
    measurement = db.relationship('Measurement', backref=db.backref('quantities', lazy=True))

    def __init__(self, quantity, recipe, ingredient, measurement):
        self.quantity = quantity
        self.recipe = recipe
        self.ingredient = ingredient
        self.measurement = measurement
    
    def __repr__(self):
        return '<Quantity %r>' % self.quantity


class SavedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('savedrecipes', lazy=True))

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)
    recipe = db.relationship('Recipe', backref=db.backref('savedrecipes', lazy=True))

    UniqueConstraint('user_id', 'recipe_id', name='savedrecipe_user_recipe_uc')

    def __init__(self, user, recipe):
        self.user = user
        self.recipe = recipe