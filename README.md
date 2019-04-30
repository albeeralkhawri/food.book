![picture](https://www.up-00.com/i/00118/ogsr2ldorpyo.jpeg)

### <a href="https://foods-book.herokuapp.com/"> *FooD Book* </a>
***
## UX

Details of the UX design is available in the 'project design' folder. This folder contains documents that illustrate the user interface design by way of wireframe mockups of the main web pages of the application,
>This is a simple example and can be found in the illustration in the folder
![picture](https://www.up-00.com/i/00118/qwr2qr50zzqg.jpg)
***
## Database Design

Details of the Database design is available in the
'Database Scheme' folder. The ERD (Entity Relationship Diagram) document outlines how I approached the design of the Database,
>This is a simple example and can be found in the illustration in the folder
![picture](https://www.up-00.com/i/00118/c8v563j9tixr.png)
***
## What does it do?
_This is a web application which that allows users to store and easily access cooking recipes. It is a  web application  (Create, Read, Update, Delete) functionality to a database hosted in the cloud on Heroku platform as a service._
***
# Features
## Existing Features
### Users can :
- Recipe Search: search by recipe name, search by ingredient and filter recipes by category, course, cuisine and author on the index page. 
- Add Recipe: Add a new recipe and then Add ingredients and methods to the recipe on the recipe detail page.
- Manage Categories: Add new and Edit existing static data like categories, courses, cuisines, authors, measurements etc.
- My Recipes: view a list of recipes submitted by the current logged in user.
- Saved Recipes: view and manage a list of recipes saved by the current logged in user.
- Dashboard: displays interactive dashboard of charts; Categories bar chart, courses pie chart, cuisines row chart and author bar chart. 
- Recipe Detail: Save, Edit and Delete recipes, Edit and Delete ingredients, Edit and Delete methods.

### Features Left to Implement
>Allergens and Dietary

## Demo

A demo of this web application is available <a href="https://foods-book.herokuapp.com/">here</a>.


## Getting started 

- Clone the repo and cd into the project directory.
- Ensure you have Python 3 and Postgres installed and create a virtual environment and activate it.
- Install dependencies: `pip install -r requirements.txt`.


## Technologies Used

>**HTML, CSS, JavaScript (Front End Framework Materialize)  Python, Full Stack Micro Framework Flask, PostgreSQL an object-relational database management system :**

## Testing

Automated tests were carried out and all 47 tests passed satisfactorily (see screenshot in Testing folder). They are located in the file tests.py and can be ran using the command:
`python3 tests.py`

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page
2.	Testing the CRUD functionality
3.	Testing the responsiveness of the application on different browsers and then using different devices.

## Deployment
1. Make sure requirements.txt and Procfile exist:
`pip3 freeze --local requirements.txt`
`echo web: python app.py > Procfile`
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. heroku ps:scale web=1
4. In heroku app settings set the config vars to add DATABASE_URL, IP and PORT

### Credits
#### Content
>_I took recipes from different pages by google_.

### Media
The images for recipes were also taken from the google.

### Acknowledgements
- Image upload to AWS S3 with boto3 info from this [blog](http://zabana.me/notes/upload-files-amazon-s3-flask.html).
Unit testing strategy from this [blog](https://www.patricksoftwareblog.com/unit-testing-a-flask-application/).
- My thanks and appreciation to the [Code Institute](https://courses.codeinstitute.net/program/FullstackWebDeveloper) and to the cadre of teachers
