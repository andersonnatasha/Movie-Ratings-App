"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key = True,
                        autoincrement = True
                        )
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Movie(db.Model):
    """A movie."""

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer,
                         primary_key = True,
                         autoincrement = True
                         )
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    # rating = a list of Ratings objects

    def __repr__(self):
        return f'<Movie movie_id={self.movie_id} title={self.title}>'


class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Interger,
                          primary_key = True,
                          autoincrement = True
                          )
    score = db.Column(db.Interger)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    movie = db.relationship('Movie', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)






# *rating_user_id = Rating.query.get(1).user_id*?

# rating_user = User.query.get(rating.user_id)


# Question: What is the user that wrote the rating of rating #1?

# #Step one: Select the rating you want by the serial ID
# rating_number_one = Rating.query.get(1) # Select rating number one

# # Step 2: Get the user ID of who wrote the rating for rating number one
# # Okay, who wrote rating number one?
# user_id_of_who_wrote_rating_number_one = rating_number_one.user_id

# # Step 3: Get the object info for that User and put it in a variable
# # Okay, lets get the repr info of that User (aka the object info)
# user_entire_object_of_who_wrote_rating_number_one = User.query.get(user_id_of_who_wrote_rating_number_one)

# #Step 4: See whats inside the variable
# >>> user_entire_object_of_who_wrote_rating_number_one
# <User user_id=100 email = jane@doe.com>


# Question: What is the user that wrote the rating of rating #1?
# answer: <User user_id=100 email = jane@doe.com>