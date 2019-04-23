import os
import unittest
 
from app import app, db, BASEDIR
from models import User, Recipe, Category, Course, Cuisine, Author, Country, Measurement, Quantity, Ingredient, Method
 
 
class TestCase(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'test.db') 
        app.config['SECRET_KEY'] = 'secret key'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
 
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    

    ########################
    #### helper methods ####
    ########################

    def register(self, username, password, password2):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, password2=password2),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')

    def register_user2(self):
        self.app.get('/register', follow_redirects=True)
        self.register('user2@email.com', 'FlaskIsGood', 'FlaskIsGood')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user@email.com', 'FlaskIsAmazing')

    def login_user2(self):
        self.app.get('/login', follow_redirects=True)
        self.login('user2@email.com', 'FlaskIsGood') 

    def add_static_data(self):
        with app.app_context():
            category1 = Category('Test Category 1')
            category2 = Category('Test Category 2')
            db.session.add(category1)
            db.session.add(category2)
            course1 = Course('Test Course 1')
            course2 = Course('Test Course 2')
            db.session.add(course1)
            db.session.add(course2)
            cuisine1 = Cuisine('Test Cuisine 1')
            cuisine2 = Cuisine('Test Cuisine 2')
            db.session.add(cuisine1)
            db.session.add(cuisine2)
            country1 = Country('Test Country 1')
            country2 = Country('Test Country 2')
            db.session.add(country1)
            db.session.add(country2)
            author_country1 = Country.query.filter_by(country_name='Test Country 1').first()
            author1 = Author('Test Author 1')
            author_country1.authors.append(author1)
            db.session.add(author_country1)
            author_country2 = Country.query.filter_by(country_name='Test Country 2').first()
            author2 = Author('Test Author 2')
            author_country2.authors.append(author2)
            db.session.add(author_country2)
            measurement1 = Measurement('Test Measurement 1')
            measurement2 = Measurement('Test Measurement 2')
            db.session.add(measurement1)
            db.session.add(measurement2)
            ingredient1 = Ingredient('Test Ingredient 1')
            ingredient2 = Ingredient('Test Ingredient 2')
            db.session.add(ingredient1)
            db.session.add(ingredient2)
            db.session.commit()

    def add_test_data(self):
        with app.app_context():
            self.register_user()
            self.register_user2()
            self.add_static_data()
            
            user1 = User.query.filter_by(username='user@email.com').first()
            user2 = User.query.filter_by(username='user2@email.com').first()
            
            category1 = Category.query.filter_by(category_name='Test Category 1').first()
            course1 = Course.query.filter_by(course_name='Test Course 1').first()
            cuisine1 = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            author1 = Author.query.filter_by(author_name='Test Author 1').first()

            category2 = Category.query.filter_by(category_name='Test Category 2').first()
            course2 = Course.query.filter_by(course_name='Test Course 2').first()
            cuisine2 = Cuisine.query.filter_by(cuisine_name='Test Cuisine 2').first()
            author2 = Author.query.filter_by(author_name='Test Author 2').first()
            
            image_filename = None
            image_url = None
            recipe1 = Recipe(user1, 'Test Recipe Name 1', 'Test Recipe Description 1', 15, 25, 4, category1, course1, cuisine1, author1, image_filename, image_url)
            recipe2 = Recipe(user2, 'Test Recipe Name 2', 'Test Recipe Description 2', 30, 60, 8, category2, course2, cuisine2, author2, image_filename, image_url)
            db.session.add(recipe1)
            db.session.add(recipe2)
            
            recipeA = Recipe.query.filter_by(recipe_name='Test Recipe Name 1').first()
            measurement1 = Measurement.query.filter_by(measurement_name='Test Measurement 1').first()
            ingredient1 = Ingredient.query.filter_by(ingredient_name='Test Ingredient 1').first()
            quantity1 = Quantity(1, recipeA, ingredient1, measurement1)
            db.session.add(quantity1)
            method1 = Method(recipeA, 'Test Method 1')
            db.session.add(method1)

            recipeB = Recipe.query.filter_by(recipe_name='Test Recipe Name 2').first()
            measurement2 = Measurement.query.filter_by(measurement_name='Test Measurement 2').first()
            ingredient2 = Ingredient.query.filter_by(ingredient_name='Test Ingredient 2').first()
            quantity2 = Quantity(2, recipeB, ingredient2, measurement2)
            db.session.add(quantity2)
            method2 = Method(recipeB, 'Test Method 2')
            db.session.add(method2)
            
            db.session.commit()

 
    ###############
    #### test views ####
    ###############
 
    def test_index_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_my_recipes_page(self):
        response = self.app.get('/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_my_saved_recipes_page(self):
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_manage_categories_page(self):
        response = self.app.get('/manage_static_data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Manage Categories', response.data)
    
    def test_dashboard_page(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_page(self):
        response = self.app.get('/add_recipe', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ###############
    #### test user auth ####
    ###############
    
    def test_valid_user_registration(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsAmazing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        #check if user has actually been created
        with app.app_context():
            user = User.query.filter_by(username='user@email.com').first()
            self.assertTrue(user is not None)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('user@email.com', 'FlaskIsAmazing', 'FlaskIsNotAmazing')
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_username(self):
        self.register_user()
        response = self.register('user@email.com', 'FlaskIsReallyAmazing', 'FlaskIsReallyAmazing')
        self.assertIn(b'Username already taken, please use a different username.', response.data)

    def test_valid_user_login(self):
        self.register_user()
        response = self.login('user@email.com', 'FlaskIsAmazing')
        self.assertIn(b'Success, you are now logged in!', response.data)

    def test_invalid_user_login_incorrect_username(self):
        self.register_user()
        response = self.login('person@gmail.com', 'FlaskIsAmazing')
        self.assertIn(b'Invalid username', response.data)

    def test_invalid_user_login_incorrect_password(self):
        self.register_user()
        response = self.login('user@email.com', 'FlaskIsOK')
        self.assertIn(b'Invalid password', response.data)

    def test_user_logout(self):
        self.register_user()
        self.login_user()
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout successful', response.data)

    ###############
    #### test CRUD functions (database integration tests)####
    ###############

    def test_recipe_list(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)

    def test_recipe_detail(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/recipe_detail/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        self.assertIn(b'Submitted by: user@email.com', response.data)
        self.assertIn(b'Test Category 1', response.data)
        self.assertIn(b'Test Course 1', response.data)
        self.assertIn(b'Test Cuisine 1', response.data)
        self.assertIn(b'Test Author 1', response.data)
        self.assertIn(b'15 Minutes', response.data)
        self.assertIn(b'25 Minutes', response.data)
        self.assertIn(b'6', response.data)
        self.assertIn(b'1.0 Test Measurement 1 Test Ingredient 1', response.data)
        self.assertIn(b'Test Method 1', response.data)

    def test_my_recipes(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Recipes', response.data)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)

    def test_save_recipe(self):
        self.add_test_data()
        self.login_user()
        # user1 add recipe1 to saved recipes
        response = self.app.get('/save_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe added to Saved Recipes', response.data)
        # check that recipe1 that has been saved by user1 shows up on saved recipes list
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertIn(b'Saved Recipes', response.data)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        # user1 tries to add recipe1 (already saved) to saved recipes again
        response = self.app.get('/save_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe already added to Saved Recipes', response.data)
        # check that recipe1 that has not been added to saved recipes list twice
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertIn(b'Recipe count: 1', response.data)
        self.logout()
        self.login_user2()
        # user2 add recipe2 to saved recipes
        response = self.app.get('/save_recipe/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # check that only recipe2 that has been saved by user2 shows up on saved recipes list
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 2', response.data)
        self.assertNotIn(b'Test Recipe Name 1', response.data)

    def test_delete_saved_recipe(self):
        self.add_test_data()
        self.login_user2()
        # add recipe to saved recipes
        response = self.app.get('/save_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # check that recipe that has been saved shows up on saved recipes list
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertIn(b'Saved Recipes', response.data)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        # remove recipe from saved recipes
        response = self.app.get('/delete_saved_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # check that recipe that has been removed no longer shows up on saved recipes list
        response = self.app.get('/my_saved_recipes', follow_redirects=True)
        self.assertIn(b'Saved Recipes', response.data)
        self.assertIn(b'Recipe count: 0', response.data)
        self.assertNotIn(b'Test Recipe Name 1', response.data)
        self.assertNotIn(b'Test Recipe Description 1', response.data)

    def test_recipe_search(self):
        self.add_test_data()
        # check for partial match only one result
        response = self.app.post('/recipe_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': '1',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertNotIn(b'Test Recipe Name 2', response.data)
        # check for partial match multiple results
        response = self.app.post('/recipe_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 2', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Name 2', response.data)
        # check for no match no results
        response = self.app.post('/recipe_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test Recipe Name 3',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 0', response.data)
        self.assertNotIn(b'Test Recipe Name 1', response.data)
        self.assertNotIn(b'Test Recipe Name 2', response.data)

    def test_ingredient_search(self):
        self.add_test_data()
        # check for partial match only one result
        response = self.app.post('/ingredient_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'ingredient_name': '2',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 1', response.data)
        self.assertIn(b'Test Recipe Name 2', response.data)
        self.assertNotIn(b'Test Recipe Name 1', response.data)
        # check for partial match multiple results
        response = self.app.post('/ingredient_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'ingredient_name': 'Test',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 2', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Name 2', response.data)
        # check for no match no results
        response = self.app.post('/ingredient_search',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'ingredient_name': 'Test Ingredient Name 3',
                                            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe count: 0', response.data)
        self.assertNotIn(b'Test Recipe Name 1', response.data)
        self.assertNotIn(b'Test Recipe Name 2', response.data)

    def test_recipe_list_filtered(self):
        with app.app_context():
            self.add_test_data()
            # check all options left unselected returns all recipes (unfiltered)
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 2', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertIn(b'Test Recipe Name 2', response.data)
            # check all filters work together
            category = Category.query.filter_by(category_name='Test Category 1').first()
            course = Course.query.filter_by(course_name='Test Course 1').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            author= Author.query.filter_by(author_name='Test Author 1').first()
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={'recipe_category': category.id,
                                        'recipe_course': course.id,
                                        'recipe_cuisine': cuisine.id,
                                        'recipe_author': author.id
                                        }
                                        , follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 1', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertNotIn(b'Test Recipe Name 2', response.data)
            # check category only
            category = Category.query.filter_by(category_name='Test Category 1').first()
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={'recipe_category': category.id
                                                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 1', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertNotIn(b'Test Recipe Name 2', response.data)
            # check course only
            course = Course.query.filter_by(course_name='Test Course 1').first()
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={'recipe_course': course.id
                                                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 1', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertNotIn(b'Test Recipe Name 2', response.data)
            # check cuisine only
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={'recipe_cuisine': cuisine.id
                                                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 1', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertNotIn(b'Test Recipe Name 2', response.data)
            # check author only
            author = Author.query.filter_by(author_name='Test Author 1').first()
            response = self.app.post('/recipe_list_filtered',
                                        buffered=True,
                                        content_type='multipart/form-data',
                                        data={'recipe_author': author.id
                                                }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Recipe count: 1', response.data)
            self.assertIn(b'Test Recipe Name 1', response.data)
            self.assertNotIn(b'Test Recipe Name 2', response.data)
            
    '''Recipe'''
    def test_add_recipe(self):
        with app.app_context():
            self.add_static_data()
            category = Category.query.filter_by(category_name='Test Category 1').first()
            course = Course.query.filter_by(course_name='Test Course 1').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 1').first()
            author = Author.query.filter_by(author_name='Test Author 1').first()
            self.register_user()
            self.login_user()
            response = self.app.post('/add_recipe',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test Recipe Name A',
                                            'recipe_description': 'Test Recipe Description A',
                                            'preparation_time': 30,
                                            'cooking_time': 60,
                                            'servings': 8,
                                            'recipe_category': category.id,
                                            'recipe_course': course.id,
                                            'recipe_cuisine': cuisine.id,
                                            'recipe_author' : author.id
                                            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Recipe Name A', response.data)

    def test_edit_recipe(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/edit_recipe/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Recipe', response.data)
        self.assertIn(b'Test Recipe Name 1', response.data)
        self.assertIn(b'Test Recipe Description 1', response.data)
        self.assertIn(b'Test Category 1', response.data)
        self.assertIn(b'Test Course 1', response.data)
        self.assertIn(b'Test Cuisine 1', response.data)
        self.assertIn(b'Test Author 1', response.data)
        self.assertIn(b'15', response.data)
        self.assertIn(b'25', response.data)
        self.assertIn(b'4', response.data)
        self.logout()
        self.login_user2()
        response = self.app.get('/edit_recipe/1', follow_redirects=True)
        self.assertIn(b'You do not have permission to edit this recipe', response.data)

    def test_update_recipe(self):
        with app.app_context():
            self.add_test_data()
            category = Category.query.filter_by(category_name='Test Category 2').first()
            course = Course.query.filter_by(course_name='Test Course 2').first()
            cuisine = Cuisine.query.filter_by(cuisine_name='Test Cuisine 2').first()
            author = Author.query.filter_by(author_name='Test Author 2').first()
            self.login_user()
            response = self.app.post('/update_recipe/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'recipe_name': 'Test Recipe Name B',
                                            'recipe_description': 'Test Recipe Description B',
                                            'preparation_time': 16,
                                            'cooking_time': 26,
                                            'servings': 5,
                                            'recipe_category': category.id,
                                            'recipe_course': course.id,
                                            'recipe_cuisine': cuisine.id,
                                            'recipe_author' : author.id
                                            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Recipe Name B', response.data)
            self.assertIn(b'Test Recipe Description B', response.data)
            self.assertIn(b'Test Category 2', response.data)
            self.assertIn(b'Test Course 2', response.data)
            self.assertIn(b'Test Cuisine 2', response.data)
            self.assertIn(b'Test Author 2', response.data)
            self.assertIn(b'16 Minutes', response.data)
            self.assertIn(b'26 Minutes', response.data)
            self.assertIn(b'5', response.data)

    def test_delete_recipe(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.get('/delete_recipe/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test Recipe Name 1', response.data)
            response = self.app.get('/delete_recipe/2', follow_redirects=True)
            self.assertIn(b'You do not have permission to delete this recipe', response.data)

    '''Quantity'''
    def test_add_quantity(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            measurement = Measurement.query.filter_by(measurement_name='Test Measurement 2').first()
            response = self.app.post('/add_quantity/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'quantity': 2,
                                          'quantity_ingredient': 'Test Ingredient A',
                                          'quantity_measurement': measurement.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'2.0 Test Measurement 2 Test Ingredient A', response.data)
            # check user access 
            response = self.app.get('/add_quantity/2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You do not have permission to add ingredients to this recipe', response.data)

    def test_edit_quantity(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/edit_quantity/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Ingredient', response.data)
        self.assertIn(b'1.0', response.data)
        self.assertIn(b'Test Measurement 1', response.data)
        self.assertIn(b'Test Ingredient 1', response.data)
        # check user access 
        response = self.app.get('/edit_quantity/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You do not have permission to edit this ingredient', response.data)
    
    def test_update_quantity(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            measurement = Measurement.query.filter_by(measurement_name='Test Measurement 2').first()
            response = self.app.post('/update_quantity/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'quantity': 2,
                                          'quantity_ingredient': 'Test Ingredient 1 Updated',
                                          'quantity_measurement': measurement.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'2.0 Test Measurement 2 Test Ingredient 1 Updated', response.data)

    def test_delete_quantity(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.get('/delete_quantity/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'1.0 Test Measurement 1 Test Ingredient 1', response.data)
            # check user access
            response = self.app.get('/delete_quantity/2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You do not have permission to delete this ingredient', response.data)

    '''Method'''
    def test_add_method(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_method/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'method': 'Test Method A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Method A', response.data)
            # check user access 
            response = self.app.get('/add_method/2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You do not have permission to add methods to this recipe', response.data)

    def test_edit_method(self):
        self.add_test_data()
        self.login_user()
        response = self.app.get('/edit_method/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Method', response.data)
        self.assertIn(b'Test Method 1', response.data)
        # check user access 
        response = self.app.get('/edit_method/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You do not have permission to edit this method', response.data)
    
    def test_update_method(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_method/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'method': 'Test Method B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Method B', response.data)

    def test_delete_method(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.get('/delete_method/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'Test Method 1', response.data)
            # check user access
            response = self.app.get('/delete_method/2', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You do not have permission to delete this method', response.data)

    '''Static Data: Category'''
    def test_add_category(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_category',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'category': 'Test Category A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Category A', response.data)
    
    def test_update_category(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_category/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'category': 'Test Category B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Category B', response.data)

    '''Static Data: Course'''
    def test_add_course(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_course',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'course': 'Test Course A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Course A', response.data)
    
    def test_update_course(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_course/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'course': 'Test Course B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Course B', response.data)

    '''Static Data: Cuisine'''
    def test_add_cuisine(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_cuisine',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'cuisine': 'Test Cuisine A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Cuisine A', response.data)
    
    def test_update_cuisine(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_cuisine/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'cuisine': 'Test Cuisine B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Cuisine B', response.data)

    '''Static Data: Country'''
    def test_add_country(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_country',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'country': 'Test Country A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Country A', response.data)
    
    def test_update_country(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_country/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'country': 'Test Country B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Country B', response.data)

    '''Static Data: Author'''
    def test_add_author(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            author_country = Country.query.filter_by(country_name='Test Country 1').first()
            response = self.app.post('/add_author',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'author': 'Test Author A',
                                          'author_country': author_country.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Author A, Test Country 1', response.data)
    
    def test_update_author(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            author_country = Country.query.filter_by(country_name='Test Country 2').first()
            response = self.app.post('/update_author/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'author': 'Test Author B',
                                          'author_country': author_country.id
                                          }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Author B, Test Country 2', response.data)

    '''Static Data: Measurement'''
    def test_add_measurement(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/add_measurement',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'measurement': 'Test Measurement A'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Measurement A', response.data)
    
    def test_update_measurement(self):
        with app.app_context():
            self.add_test_data()
            self.login_user()
            response = self.app.post('/update_measurement/1',
                                    buffered=True,
                                    content_type='multipart/form-data',
                                    data={'measurement': 'Test Measurement B'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Measurement B', response.data)

 
if __name__ == "__main__":
    unittest.main()