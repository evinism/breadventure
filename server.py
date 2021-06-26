"""Server for bread journal app."""

from flask import Flask, render_template, request, redirect, flash, session
from model import connect_to_db
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') # autogenerated and in secrets.sh
app.jinja_env.undefined = StrictUndefined

@app.route('/')
@app.route('/home')
def view_home():
    """View home."""
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    """Process users login form."""
    # login page is not rendered, only redirects either 
    # back to home page or to user page- is slower but 
    # is cleaner; speed is negligible

    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)
    if user and user.password == password: 
        session["user_id"] = user.id
        return redirect('/user')
    else:
        flash('There was an error logging in! Please try again or make an account.')
        return redirect('/')


@app.route('/user')
def user_page():
    
    user = crud.get_user_by_id(session["user_id"])
    recipes = crud.get_recipes_by_user(session["user_id"])

    return render_template('user.html', username=user.username, recipes=recipes)

@app.route('/new-user')
def new_user():
    """View form to register new user."""

    return render_template('new_user.html')

@app.route('/register-user', methods=['GET', 'POST'])
def register_new_user():
    """Process form from new user."""

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # check if user already exists, flash message + redirect to top
    # how to handle unique fields
    new_user = crud.create_user(username, email, password)

    flash('Success! Account made. Please log in.')

    return redirect('/home')
    

@app.route('/make-recipe')
def make_recipe():
    """View form for user to input new recipe details."""

    return render_template('recipe_form.html')

# one route to show form, one route to process form

@app.route('/create-recipe', methods=['GET', 'POST'])
def create_new_recipe():
    """Process details from new recipe form, add to database."""
    # function arguments are usually query parameters

    # get user id from session
    # get recipe attributes from form
        # conditional attributes? if they exist, set them

    # commit to database 

    # return redirect 

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)