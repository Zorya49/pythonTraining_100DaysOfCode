import os
import smtplib
import atexit
import requests
import signal
from flask import Flask, render_template, request
from post import Post

POSTS_URL = "https://api.npoint.io/674f5423f73deab1e9a7"

my_email = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
connection = smtplib.SMTP("smtp-mail.outlook.com", port=587)

app = Flask(__name__)

posts_response = requests.get(POSTS_URL).json()
post_objects = []
for post in posts_response:
    post_object = Post(post["id"], post["title"], post["subtitle"], post["body"], post["image_url"])
    post_objects.append(post_object)


def send_mail(data):
    connection.sendmail(from_addr=my_email,
                        to_addrs=my_email,
                        msg=f"New message from {data["name"]}!\n\n"
                            f"From: {data["name"]}\n"
                            f"Email: {data["email"]}\n"
                            f"Phone: {data["phone"]}\n"
                            f"Message:\n{data["message"]}")


def handle_exit():
    print("Gracefully close mail server connection at exiting script.")
    connection.close()


@app.route('/')
def home():
    return render_template("index.html", blog_posts=post_objects)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        mail_data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "message": request.form['message']
        }
        send_mail(mail_data)
        return render_template("contact.html", page_heading="Message sent successfully!")
    return render_template("contact.html", page_heading="Contact Me")


@app.route('/post/<post_id>')
def get_post(post_id):
    requested_post = next((p for p in post_objects if p.id == int(post_id)), None)
    if requested_post:
        return render_template("post.html", post=requested_post)
    else:
        return f"Post with ID {post_id} not found!"


if __name__ == "__main__":
    connection.starttls()
    connection.login(user=my_email, password=password)
    app.run(debug=True)
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
