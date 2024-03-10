import requests
from flask import Flask, render_template
from post import Post

POSTS_URL = "https://api.npoint.io/674f5423f73deab1e9a7"

app = Flask(__name__)

posts_response = requests.get(POSTS_URL).json()
post_objects = []
for post in posts_response:
    post_object = Post(post["id"], post["title"], post["subtitle"], post["body"], post["image_url"])
    post_objects.append(post_object)


@app.route('/')
def home():
    return render_template("index.html", blog_posts=post_objects)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<post_id>')
def get_post(post_id):
    requested_post = next((p for p in post_objects if p.id == int(post_id)), None)
    if requested_post:
        return render_template("post.html", post=requested_post)
    else:
        return f"Post with ID {post_id} not found!"


if __name__ == "__main__":
    app.run(debug=True)
