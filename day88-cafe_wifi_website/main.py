from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from random import randint
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

SEATS_CHOICES = [("0", "0-9"), ("1", "10-19"), ("2", "20-29"), ("3", "30-39"), ("4", "40-49"), ("5", "50+")]


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns if column.name != "id"}


with app.app_context():
    db.create_all()


def str_to_bool(arg_from_url):
    if arg_from_url in ['True', 'true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField('Maps link', validators=[DataRequired()])
    image_url = URLField('Image link', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField('Has power sockets?')
    has_toilet = BooleanField('Has toilets?')
    has_wifi = BooleanField('Has WiFi?')
    can_take_calls = BooleanField('Can take calls?')
    seats = SelectField(u'Seats available', choices=SEATS_CHOICES, validators=[DataRequired()])
    coffee_price = StringField('Price for regular cappuccino', validators=[DataRequired()])
    submit = SubmitField('Submit')


# All standard Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.image_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=dict(SEATS_CHOICES).get(form.seats.data),
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return home()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafes_db = db.session.query(Cafe).all()
    cafe_list = [["Cafe Name", "Location", "Map", "Image", "Power outlets", "Toilet", "WiFi", "Calls allowed",
                  "Seats", "Regular Cappuccino price"]]

    for cafe in cafes_db:
        sockets = "✔️" if cafe.has_sockets else "❌"
        toilet = "✔️" if cafe.has_toilet else "❌"
        wifi = "✔️" if cafe.has_wifi else "❌"
        calls = "✔️" if cafe.can_take_calls else "❌"
        cafe_info = [f"{cafe.name}", f"{cafe.location}", f"{cafe.map_url}", f"{cafe.img_url}", f"{sockets}",
                     f"{toilet}", f"{wifi}", f"{calls}", f"{cafe.seats}", f"{cafe.coffee_price}"]
        cafe_list.append(cafe_info)

    return render_template('cafes.html', cafes=cafe_list)


# All API routes below
@app.route("/api/all", methods=['GET'])
def get_all():
    cafes_db = db.session.query(Cafe).all()
    cafe_dicts = [cafe.to_dict() for cafe in cafes_db]
    return jsonify(cafe=cafe_dicts)


@app.route("/api/search", methods=['GET'])
def get_cafes_at_location():
    query_location = request.args.get("loc")
    cafes = db.session.query(Cafe).filter(Cafe.location.ilike(f'%{query_location}%'))
    if cafes:
        cafe_dicts = [cafe.to_dict() for cafe in cafes]
        return jsonify(cafe=cafe_dicts)
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe at that location."
        })


@app.route("/api/add", methods=['POST'])
def add_new_cafe():
    try:
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=str_to_bool(request.form.get("sockets")),
            has_toilet=str_to_bool(request.form.get("toilet")),
            has_wifi=str_to_bool(request.form.get("wifi")),
            can_take_calls=str_to_bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
    except KeyError:
        return jsonify(error={
            "Bad Request": "At least one field were incorrect or missing."
        })
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={
        "Success": "Successfully added the new cafe."
    })


if __name__ == '__main__':
    app.run(debug=True)
