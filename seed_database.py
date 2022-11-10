import os
import json
import crud
import model
import server


from random import choice, randint
from datetime import datetime

os.system("dropdb ratings")
os.system("createdb ratings")





model.connect_to_db(server.app)
model.db.create_all()


with open("data/movies.json") as f:
    movie_data = json.loads(f.read())






movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)





model.db.session.add_all(movies_in_db)
model.db.session.commit()
#commiting() information (inputted)

for i in range(29):
    email = f"user{i}@test.com"
    password = "testing123"
#^^



    user = crud.create_user(email, password)
    model.db.session.add(user)

    for j in range(29):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)

        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.add_all
model.db.session.commit()