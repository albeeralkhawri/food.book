# python imports
import os, sys

# local imports
from extensions import db, migrate, login_manager
from models import User
from forms import RegistrationForm, LoginForm

#flask imports
from flask import Flask
from flask_dotenv import DotEnv
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import current_user, login_user, logout_user, login_required
import boto3



# create an instance of flask = app variable
app = Flask(__name__)
env = DotEnv(app)
env.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# grab the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

app.config['SECRET_KEY'] = 'super secret key'


# Configure the image uploading via AWS S3 boto3

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = 'https://s3-eu-west-1.amazonaws.com/{}/'.format(S3_BUCKET)

s3 = boto3.client(
   "s3",
   aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
   aws_secret_access_key=S3_SECRET
)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

login_manager.login_view = 'login'

from models import Recipe, Category, Course, Cuisine, Country, Author, Measurement, Quantity, Ingredient, Method, User, SavedRecipe

#################AWS_S3_file_upload###########################
def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username','error')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password','error')
            return redirect(url_for('login'))
        login_user(user)
        flash('Success, you are now logged in!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#############################DASHBOARD##########################################
@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')
#############################RECIPE JSON DATA ENDPOINT##########################################
@app.route('/get_recipes')
def get_recipes_json():
    recipes = []
    for r in db.session.query(Recipe).all():
        print(r, file=sys.stdout)
        recipes.append({
            'recipe_name': r.recipe_name,
            'recipe_description': r.recipe_description,
            'category': r.category.category_name,
            'cuisine': r.cuisine.cuisine_name,
            'course': r.course.course_name,
            'author': r.author.author_name
        })


    return jsonify(recipes)

#############################INDEX##########################################
@app.route('/')
def index():
    recipe_count = Recipe.query.count()
    categories_list = Category.query.limit(100).all()
    courses_list = Course.query.limit(100).all()
    cuisines_list = Cuisine.query.limit(100).all()
    authors_list = Author.query.limit(100).all()

    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.order_by(Recipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('index', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('index', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('index.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url, categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

#############################MY RECIPES##########################################
@app.route('/my_recipes')
@login_required
def my_recipes():
    recipe_count = Recipe.query.filter_by(user=current_user).count()
    page = request.args.get('page', 1, type=int)
    recipes_list = Recipe.query.filter_by(user=current_user).order_by(Recipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('index', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('index', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('my_recipes.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url)

#############################RECIPE LIST FILTERED##########################################
@app.route('/recipe_list_filtered', methods = ['POST'])
def recipe_list_filtered():
    categories_list = Category.query.limit(100).all()
    courses_list = Course.query.limit(100).all()
    cuisines_list = Cuisine.query.limit(100).all()
    authors_list = Author.query.limit(100).all()
    
    recipe_category = Category.query.filter_by(id=request.form.get('recipe_category')).first()
    recipe_course = Course.query.filter_by(id=request.form.get('recipe_course')).first()
    recipe_cuisine = Cuisine.query.filter_by(id=request.form.get('recipe_cuisine')).first()
    recipe_author = Author.query.filter_by(id=request.form.get('recipe_author')).first()
    queries = []
    if recipe_category is not None:
        queries.append(Recipe.category == recipe_category)
    if recipe_course is not None:
        queries.append(Recipe.course == recipe_course)
    if recipe_cuisine is not None:
        queries.append(Recipe.cuisine == recipe_cuisine)
    if recipe_author is not None:
        queries.append(Recipe.author == recipe_author)
    
    recipes_list = Recipe.query.filter(*queries).all()
    recipe_count = Recipe.query.filter(*queries).count()
    return render_template('index.html', recipe_count=str(recipe_count), recipes_list=recipes_list, categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)
    

#############################RECIPE SEARCH##########################################
@app.route('/recipe_search', methods = ['POST'])
def recipe_search():      
    recipes_list = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).all()
    recipe_count = Recipe.query.filter(Recipe.recipe_name.ilike("%" + request.form['recipe_name'] + "%")).count()
    return render_template('index.html', recipe_count=str(recipe_count), recipes_list=recipes_list)


#############################INGREDIENT SEARCH##########################################
@app.route('/ingredient_search', methods=['POST'])
def ingredient_search():
    recipes = []
    quantity_list = Quantity.query.filter(Quantity.ingredient.has(Ingredient.ingredient_name.ilike("%" + request.form['ingredient_name'] + "%"))).all()
    for quantity in quantity_list:
        recipe_id = quantity.recipe_id
        recipes.append(recipe_id)

    recipes_list = Recipe.query.join(Quantity).filter(Recipe.id.in_(recipes)).all()
    recipe_count = Quantity.query.filter(Quantity.ingredient.has(Ingredient.ingredient_name.ilike("%" + request.form['ingredient_name'] + "%"))).count()
    return render_template('index.html', recipe_count=str(recipe_count), recipes_list=recipes_list)


#############################RECIPE DETAIL##########################################
@app.route('/recipe_detail/<id>')
def recipe_detail(id):

    recipe = Recipe.query.filter_by(id=int(id)).first()
    quantity_list = Quantity.query.filter_by(recipe_id=id)
    method_list = Method.query.filter_by(recipe_id=id)

    return render_template('recipe_detail.html', recipe=recipe, quantity_list=quantity_list, method_list=method_list)

#############################RECIPE##########################################
@app.route('/add_recipe', methods = ['GET','POST'])
@login_required
def add_recipe():
        categories_list = Category.query.limit(100).all()
        courses_list = Course.query.limit(100).all()
        cuisines_list = Cuisine.query.limit(100).all()
        authors_list = Author.query.limit(100).all()
        
        if request.method == 'POST':
            recipe_category = Category.query.filter_by(id=request.form['recipe_category']).first()
            recipe_course = Course.query.filter_by(id=request.form['recipe_course']).first()
            recipe_cuisine = Cuisine.query.filter_by(id=request.form['recipe_cuisine']).first()
            recipe_author = Author.query.filter_by(id=request.form['recipe_author']).first()

            if 'recipe_image' in request.files:
                file = request.files["recipe_image"]
                output  = upload_file_to_s3(file, S3_BUCKET)
                filename = file.filename
                url = str(output)
            else:
                filename = None
                url = None

            recipe = Recipe(current_user,
            request.form['recipe_name'],
            request.form['recipe_description'], 
            request.form['preparation_time'], 
            request.form['cooking_time'], 
            request.form['servings'],
            recipe_category,
            recipe_course,
            recipe_cuisine,
            recipe_author,
            filename,
            url)

            db.session.add(recipe)

            db.session.commit()
            return redirect(url_for('index'))
        
        return render_template('add_recipe.html', categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

@app.route('/edit_recipe/<id>')
@login_required
def edit_recipe(id):
        recipe = Recipe.query.get(id)
        categories_list = Category.query.limit(100).all()
        courses_list = Course.query.limit(100).all()
        cuisines_list = Cuisine.query.limit(100).all()
        authors_list = Author.query.limit(100).all()
        if recipe.user != current_user:
            flash('You do not have permission to edit this recipe')
            return redirect(url_for('index'))
        return render_template('edit_recipe.html', recipe=recipe, categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, authors_list=authors_list)

@app.route('/update_recipe/<id>', methods = ['GET','POST'])
def update_recipe(id):
        
        if request.method == 'POST':
            recipe = Recipe.query.get(id)

            if 'recipe_image' in request.files:
                file = request.files["recipe_image"]
                output  = upload_file_to_s3(file, S3_BUCKET)
                filename = file.filename
                url = str(output)
            elif recipe.image_url is not None:
                filename = recipe.image_filename
                url = recipe.image_url              
            else:
                filename = None
                url = None

            recipe.recipe_name = request.form['recipe_name']
            recipe.recipe_description = request.form['recipe_description']
            recipe.preparation_time = request.form['preparation_time']
            recipe.cooking_time = request.form['cooking_time']
            recipe.servings = request.form['servings']
            recipe.category = Category.query.filter_by(id=request.form['recipe_category']).first()
            recipe.course = Course.query.filter_by(id=request.form['recipe_course']).first()
            recipe.cuisine = Cuisine.query.filter_by(id=request.form['recipe_cuisine']).first()
            recipe.author = Author.query.filter_by(id=request.form['recipe_author']).first()
            recipe.image_filename = filename
            recipe.image_url = url

            db.session.commit()
            return redirect(url_for('recipe_detail', id=recipe.id))
        
        return redirect(url_for('index'))

@app.route('/delete_recipe/<id>')
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe.user != current_user:
        flash('You do not have permission to delete this recipe')
        return redirect(url_for('index'))
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

#############################INGREDIENT##########################################
@app.route('/add_quantity/<id>', methods = ['GET','POST'])
@login_required
def add_quantity(id):
        measurements_list = Measurement.query.limit(100).all()
        quantity_recipe = Recipe.query.get(id)
        if quantity_recipe.user != current_user:
            flash('You do not have permission to add ingredients to this recipe')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            
            quantity_measurement = Measurement.query.filter_by(id=request.form['quantity_measurement']).first()
            
            # check if ingredient has already been created and if so use the existing before creating (same) new ingredient to avoid duplicate data
            existing_ingredient = Ingredient.query.filter_by(ingredient_name=request.form['quantity_ingredient']).first()
            if existing_ingredient is not None:
                quantity_ingredient = existing_ingredient
            else:
                quantity_ingredient = Ingredient(request.form['quantity_ingredient'])

            quantity = Quantity(request.form['quantity'], 
            quantity_recipe, 
            quantity_ingredient, 
            quantity_measurement)

            db.session.add(quantity)

            db.session.commit()
            return redirect(url_for('recipe_detail', id=id))
        
        return render_template('add_quantity.html', measurements_list=measurements_list, recipe=quantity_recipe)

@app.route('/edit_quantity/<id>')
@login_required
def edit_quantity(id):
        quantity = Quantity.query.get(id)
        quantity_recipe = Recipe.query.get(quantity.recipe_id)
        measurements_list = Measurement.query.limit(100).all()
        if quantity_recipe.user != current_user:
            flash('You do not have permission to edit this ingredient')
            return redirect(url_for('index'))
        return render_template('edit_quantity.html', quantity=quantity, measurements_list=measurements_list, recipe=quantity_recipe)

@app.route('/update_quantity/<id>', methods = ['GET','POST'])
def update_quantity(id):
        quantity = Quantity.query.get(id)
        quantity_recipe = Recipe.query.get(quantity.recipe_id)
        measurements_list = Measurement.query.limit(100).all()
        
        if request.method == 'POST':
            quantity = Quantity.query.get(id)
            quantity.quantity = request.form['quantity']
            quantity.recipe = quantity_recipe
            quantity.measurement = Measurement.query.filter_by(id=request.form['quantity_measurement']).first()
            quantity.ingredient.ingredient_name = request.form['quantity_ingredient']

            db.session.commit()
            return redirect(url_for('recipe_detail', id=quantity_recipe.id))
        
        return redirect(url_for('recipe_detail', id=quantity_recipe.id))

@app.route('/delete_quantity/<id>')
@login_required
def delete_quantity(id):
    quantity = Quantity.query.get(id)
    quantity_recipe = Recipe.query.get(quantity.recipe_id)
    if quantity_recipe.user != current_user:
        flash('You do not have permission to delete this ingredient')
        return redirect(url_for('index'))
    db.session.delete(quantity)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=quantity_recipe.id))

#############################METHOD##########################################
@app.route('/add_method/<id>', methods = ['GET','POST'])
@login_required
def add_method(id):       
        method_recipe = Recipe.query.get(id)
        if method_recipe.user != current_user:
            flash('You do not have permission to add methods to this recipe')
            return redirect(url_for('index'))
        if request.method == 'POST':

            method = Method(method_recipe,(request.form['method']))
            db.session.add(method)
            db.session.commit()
            return redirect(url_for('recipe_detail', id=id))
        
        return render_template('add_method.html', recipe=method_recipe)

@app.route('/edit_method/<id>')
@login_required
def edit_method(id):
        method = Method.query.get(id)
        method_recipe = Recipe.query.get(method.recipe_id)
        if method_recipe.user != current_user:
            flash('You do not have permission to edit this method')
            return redirect(url_for('index'))
        return render_template('edit_method.html', method=method, recipe=method_recipe)

@app.route('/update_method/<id>', methods = ['GET','POST'])
def update_method(id):
        method = Method.query.get(id)
        method_recipe = Recipe.query.get(method.recipe_id)
        
        
        if request.method == 'POST':
            method = Method.query.get(id)

            method.method_description = request.form['method']
            method.recipe = method_recipe

            db.session.commit()
            return redirect(url_for('recipe_detail', id=method_recipe.id))
        
        return redirect(url_for('recipe_detail', id=method_recipe.id))

@app.route('/delete_method/<id>')
@login_required
def delete_method(id):
    method = Method.query.get(id)
    method_recipe = Recipe.query.get(method.recipe_id)
    if method_recipe.user != current_user:
        flash('You do not have permission to delete this method')
        return redirect(url_for('index'))
    db.session.delete(method)
    db.session.commit()
    return redirect(url_for('recipe_detail', id=method_recipe.id))

#############################SAVEDRECIPE##########################################
@app.route('/save_recipe/<id>')
@login_required
def save_recipe(id):
    recipe = Recipe.query.get(id)
    existing_saved_recipe = SavedRecipe.query.filter_by(user=current_user, recipe=recipe).first()
    if existing_saved_recipe is None:
        savedrecipe = SavedRecipe(current_user, recipe)
        db.session.add(savedrecipe)
        db.session.commit()
        flash('Recipe added to Saved Recipes')
    else:
        flash('Recipe already added to Saved Recipes')
    return redirect(url_for('recipe_detail', id=id))

@app.route('/delete_saved_recipe/<id>')
@login_required
def delete_saved_recipe(id):
    savedrecipe = SavedRecipe.query.get(id)
    db.session.delete(savedrecipe)
    db.session.commit()
    flash('Recipe deleted from My Saved Recipes')
    return redirect(url_for('my_saved_recipes'))

@app.route('/my_saved_recipes')
@login_required
def my_saved_recipes():
    recipe_count = SavedRecipe.query.filter_by(user=current_user).count()
    page = request.args.get('page', 1, type=int)
    recipes_list = SavedRecipe.query.filter_by(user=current_user).order_by(SavedRecipe.id.desc()).paginate(page, 10, False)
    next_url = url_for('index', page=recipes_list.next_num) \
        if recipes_list.has_next else None
    prev_url = url_for('index', page=recipes_list.prev_num) \
        if recipes_list.has_prev else None
    return render_template('my_saved_recipes.html', recipe_count=str(recipe_count), recipes_list=recipes_list.items, next_url=next_url, prev_url=prev_url)

#############################MANAGE STATIC DATA##########################################
@app.route('/manage_static_data')
@login_required
def manage_static_data():
    categories_list = Category.query.limit(100).all()
    courses_list = Course.query.limit(100).all()
    cuisines_list = Cuisine.query.limit(100).all()
    countries_list = Country.query.limit(250).all()
    authors_list = Author.query.limit(100).all()
    measurements_list = Measurement.query.limit(100).all()
    return render_template('manage_static_data.html', categories_list=categories_list, courses_list=courses_list, cuisines_list=cuisines_list, countries_list=countries_list, authors_list=authors_list, measurements_list=measurements_list)

#############################CATEGORY##########################################
@app.route('/add_category', methods = ['POST'])
def add_category():
    category = Category(request.form['category'])
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_category/<id>', methods = ['POST'])
def update_category(id):
    category = Category.query.get(id)
    category.category_name = request.form['category']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COURSE##########################################
@app.route('/add_course', methods = ['POST'])
def add_course():
    course = Course(request.form['course'])
    db.session.add(course)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_course/<id>', methods = ['POST'])
def update_course(id):
    course = Course.query.get(id)
    course.course_name = request.form['course']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################CUISINE##########################################
@app.route('/add_cuisine', methods = ['POST'])
def add_cuisine():
    cuisine = Cuisine(request.form['cuisine'])
    db.session.add(cuisine)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_cuisine/<id>', methods = ['POST'])
def update_cuisine(id):
    cuisine = Cuisine.query.get(id)
    cuisine.cuisine_name = request.form['cuisine']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################COUNTRY##########################################
@app.route('/add_country', methods = ['POST'])
def add_country():
    country = Country(request.form['country'])
    db.session.add(country)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_country/<id>', methods = ['POST'])
def update_country(id):
    country = Country.query.get(id)
    country.country_name = request.form['country']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################AUTHOR##########################################
@app.route('/add_author', methods = ['POST'])
def add_author():
    author_country = Country.query.filter_by(id=request.form['author_country']).first()
    author = Author(request.form['author'])
    author_country.authors.append(author)
    db.session.add(author_country)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_author/<id>', methods = ['POST'])
def update_author(id):
    author = Author.query.get(id)
    author.author_name = request.form['author']
    author.country = Country.query.filter_by(id=request.form['author_country']).first()
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################MEASUREMENT##########################################
@app.route('/add_measurement', methods = ['POST'])
def add_measurement():
    measurement = Measurement(request.form['measurement'])
    db.session.add(measurement)
    db.session.commit()
    return redirect(url_for('manage_static_data'))

@app.route('/update_measurement/<id>', methods = ['POST'])
def update_measurement(id):
    measurement = Measurement.query.get(id)
    measurement.measurement_name = request.form['measurement']
    db.session.commit()
    return redirect(url_for('manage_static_data'))

#############################HTTP ERRORS##########################################
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)