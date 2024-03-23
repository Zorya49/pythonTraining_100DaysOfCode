import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_DB_BEARER_TOKEN = os.getenv('MOVIE_DB_BEARER_TOKEN')
headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {MOVIE_DB_BEARER_TOKEN}"
        }

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies_collection.db"
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    review: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


class EditForm(FlaskForm):
    rating = FloatField('Your rating out of 10 (e.g. 7.5):', validators=[DataRequired(), NumberRange(0, 10)])
    review = StringField('Your review:', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddForm(FlaskForm):
    title = StringField('Movie title:', validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = db.session.query(Movie).order_by(Movie.rating.asc()).all()

    for idx, movie in enumerate(movies):
        movie.ranking = len(movies) - idx
    db.session.commit()

    top_10_movies = movies[-10:]
    return render_template("index.html", movies=top_10_movies)


@app.route("/edit/<movie_title>", methods=['GET', 'POST'])
def edit_movie_rating(movie_title):
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        movie_id = db.session.query(Movie.id).filter_by(title=movie_title).scalar()
        if movie_id:
            movie = db.get_or_404(Movie, movie_id)
            if movie:
                movie.rating = edit_form.rating.data
                movie.review = edit_form.review.data
                db.session.commit()
            else:
                pass
        else:
            pass
        return redirect(url_for("home"))
    return render_template("edit.html", form=edit_form)


@app.route("/delete/<movie_title>", methods=['GET', 'POST'])
def delete_movie(movie_title):
    movie_id = db.session.query(Movie.id).filter_by(title=movie_title).scalar()
    if movie_id:
        movie = db.get_or_404(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        else:
            pass
    else:
        pass
    return redirect(url_for("home"))


@app.route("/add", methods=['GET', 'POST'])
def add_movie():
    add_form = AddForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, headers=headers, params={"query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=add_form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, headers=headers, params={"language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add_movie(new_movie)
        db.session.commit()

        # Redirect to /edit route
        return redirect(url_for("edit_movie_rating", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
