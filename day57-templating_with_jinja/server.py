import datetime
import random
from flask import Flask, render_template

app = Flask(__name__)


def get_age(name):
    request_url = f"https://api.agify.io/?name={name.lower()}"
    response = requests.get(request_url).text
    response_json = json.loads(response)
    return response_json["age"]


def get_gender(name):
    request_url = f"https://api.genderize.io/?name={name.lower()}"
    response = requests.get(request_url).text
    response_json = json.loads(response)
    return response_json["gender"]


@app.route('/')
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.date.today().year
    return render_template("index.html", number=random_number, current_year=current_year)


@app.route('/<guess_name>')
def guess_age_gender(guess_name):
    try:
        guess = str(guess_name)
    except ValueError or TypeError:
        return "Please input a valid name!"

    params = {
        "name": guess.title(),
        "gender": get_gender(guess),
        "age": get_age(guess)
    }
    return render_template("guess.html", parameters=params)


@app.route('/blog')
def get_blog():
    # Fetch the JSON data from the URL
    request_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(request_url)
    data = json.loads(response.text)
    return render_template("blog.html", blog_posts=data)


if __name__ == "__main__":
    app.run(debug=True)

