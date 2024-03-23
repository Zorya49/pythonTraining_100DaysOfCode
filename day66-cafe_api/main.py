from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from random import randint

API_KEY = "TopSecretAPIKey"
app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns if column.name != "id"}


with app.app_context():
    db.create_all()


def get_random_cafe():
    total_cafes = db.session.query(func.count(Cafe.id)).scalar()
    random_index = randint(0, total_cafes - 1)
    random_cafe = db.session.query(Cafe).offset(random_index).limit(1).first()

    return random_cafe


def str_to_bool(arg_from_url):
    if arg_from_url in ['True', 'true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=['GET'])
def random():
    random_cafe = get_random_cafe()
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all", methods=['GET'])
def get_all():
    cafes = db.session.query(Cafe).all()
    cafe_dicts = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafe=cafe_dicts)


@app.route("/search", methods=['GET'])
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


@app.route("/add", methods=['POST'])
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


@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price_by_cafe_id(cafe_id):
    updated_price = request.args.get("coffee_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = updated_price
        db.session.commit()
        return jsonify(response={
            "Success": "Successfully updated coffe price."
        })
    else:
        return jsonify(error={
            "Not Found": "Sorry, we don't have a cafe with this id."
        })


@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def report_closed_by_cafe_id(cafe_id):
    if request.args.get("api_key") == API_KEY:
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={
                "Success": "Successfully deleted coffe place."
            })
        else:
            return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe with this id."
            })
    else:
        return jsonify(error={
            "Bad Key": "Sorry, you are not allowed to do this. Make sure you have correct api_key."
        })




# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
