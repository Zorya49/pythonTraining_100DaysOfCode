from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_bootstrap import Bootstrap5


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Length(min=6),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    submit = SubmitField(label='Log in')


app = Flask(__name__)
app.secret_key = "some secret string"
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@email.com' and login_form.password.data == '12345678':
            return redirect('/success')
        else:
            return redirect('/denied')
    return render_template('login.html', form=login_form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/denied')
def denied():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True)
