from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests


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
    rating: Mapped[float] = mapped_column(nullable=False)
    ranking: Mapped[int] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


class EditForm(FlaskForm):
    rating = FloatField('Your rating out of 10 (e.g. 7.5):', validators=[DataRequired(), NumberRange(0, 10)])
    review = StringField('Your review:', validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()

    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # second_movie = Movie(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=9,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # )
    # db.session.add(second_movie)
    # db.session.commit()


@app.route("/")
def home():
    movies_top10 = db.session.query(Movie).all()
    return render_template("index.html", movies=movies_top10)


@app.route("/edit/<movie_title>", methods=['GET', 'POST'])
def edit(movie_title):
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
        return home()
    return render_template("edit.html", form=edit_form)


@app.route("/delete/<movie_title>", methods=['GET', 'POST'])
def delete(movie_title):
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
    return home()


if __name__ == '__main__':
    app.run(debug=True)
