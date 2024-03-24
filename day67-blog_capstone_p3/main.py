import datetime
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

ckeditor = CKEditor()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor.init_app(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class CreatePostForm(FlaskForm):
    title = StringField('Blog post title:', validators=[DataRequired()])
    subtitle = StringField('Subtitle:', validators=[DataRequired()])
    author = StringField('Author:', validators=[DataRequired()])
    img_url = StringField('Blog image url:', validators=[DataRequired(), URL()])
    body = CKEditorField('Post content:', validators=[DataRequired()])
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    posts_db = db.session.query(BlogPost).all()
    posts = [post.to_dict() for post in posts_db]
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = db.session.query(BlogPost).get(post_id)
    if post:
        requested_post = post.to_dict()
        return render_template("post.html", post=requested_post)
    else:
        return redirect(url_for("get_all_posts"))


@app.route('/new_post', methods=['GET', 'POST'])
def add_new_post():
    add_form = CreatePostForm()
    if add_form.validate_on_submit():
        try:
            new_post = BlogPost(
                title=add_form.title.data,
                subtitle=add_form.subtitle.data,
                date=datetime.datetime.now().strftime("%B %d, %Y"),
                body=add_form.body.data,
                author=add_form.author.data,
                img_url=add_form.img_url.data
            )
        except KeyError:
            print("KeyError")
            return redirect(url_for("get_all_posts"))
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=add_form)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.session.query(BlogPost).get(post_id)
    if post:
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            author=post.author,
            img_url=post.img_url,
            body=post.body
        )
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.img_url = edit_form.img_url.data
            post.author = edit_form.author.data
            post.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))
        return render_template("make-post.html", form=edit_form, is_edit=True)
    return redirect(url_for("get_all_posts"))


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = db.session.query(BlogPost).get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("get_all_posts"))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
