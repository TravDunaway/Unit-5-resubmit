from flask import Flask, render_template, request, flash, session, redirect
from jinja2 import StrictUndefined

from model import connect_to_db, db

import crud

app = Flask(__name__)

app.secret_key = "SECRET_KEY"

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/users")
def all_users():
    users = crud.get_users()
    return render_template("all_users.html", users=users)
#this is your get_all_users function, essentially. 


@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
#new user information^^^^
    user = crud.get_user_by_email(email)
    if user:
        flash("Email provided is in use or otherwise not available for use.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successfull. Please log in to continue.")
    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

#^^^ user functions/templates





@app.route("/movies")
def all_movies():

    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)
#alling user to see any inputted film.

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)
#Above route will verify information inputted, ^^


@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"Youre newest film rating is a {rating_score}.")

    return redirect(f"/movies/{movie_id}")

###^^^^Movie templates^^^^(primarily, remember to check sesssion)

@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("Email invalid.")
    else:
        session["user_email"] = user.email
        flash(f"Hi there {user.email}, welcome back to the rating app!")
    return redirect("/")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success"
















if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="5432", debug=True)
