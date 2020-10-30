"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

#Load movies from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so
# we can use them to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie['title'],
                                    movie['overview'],
                                    movie['poster_path'])
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    db_movie = crud.create_movie(title,
                                overview,
                                release_date,
                                poster_path)
    movies_in_db.append(db_movie)


# Create 10 random users with unique email;
# choose 10 movies at random and give random rating between 1 to 5
for n in range(10):
    email = f'user{n}@test.com' # A unique email!
    password = 'test'

    user = crud.create_user(email, password)    # create a user with unique email

    for rating in range(10):                    # create for loop to occur 10 times
        random_movie = choice(movies_in_db)     # randomly select movie from list (movies_in_db)
        score = randint(1,5)                    # randomly choose number 1 - 5 to be score)

        crud.create_rating(user, random_movie, score)   # create a rating using user, random_movie,
                                                        # score variables generated above and create_rating
                                                        # function from crud.py

