"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Render homepage."""

    return render_template('homepage.html')


@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', users_jinja=users)


@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form['email']         # changed from solution: request.form.get('email')
    password = request.form['password']   # changed from solution: request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Please use a different email.')
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user_jinja=user)


@app.route('/handle-form-session')
def login():
    """Set value for session[email] to user_id."""

    email = request.args['emailL']
    password = request.args['passwordL']

    user = crud.get_user_by_email(email)

    if  user == None or password != user.password:
        flash("Email and password did not match our records. Please try again.")
    else:
        flash('Successfully logged in!')
        session['user_id'] = user.user_id

    return redirect('/')


# @app.route('/get-name')   ---> from skills assessment 3 for reference
# def set_name_sessions():
#     """Set name sessions"""

#     name = request.args.get('name')
#     session['name'] = name
#     return redirect('/top-melons')


@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies_jinja=movies) # we changed movies_jinja from movies (in solution)


@app.route('/movies/<movie_id>')  #route with a variable URL
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie_jinja=movie) # we changed movies_jinja from movies (in solution)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
