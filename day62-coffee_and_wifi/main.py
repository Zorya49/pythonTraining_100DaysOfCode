from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

COFFEE_CHOICES = [('0', '✘'), ('1', '☕️'), ('2', '☕️☕️'), ('3', '☕️☕️☕️'), ('4', '☕️☕️☕️☕️'), ('5', '☕️☕️☕️☕️☕️')]
WIFI_CHOICES = [('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')]
POWER_CHOICES = [('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')]


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Maps link', validators=[DataRequired()])
    open_time = StringField('Opening time', validators=[DataRequired()])
    closing_time = StringField('Closing time', validators=[DataRequired()])
    coffe_rating = SelectField(u'Coffe rating', choices=COFFEE_CHOICES)
    wifi_rating = SelectField(u'WiFi rating', choices=WIFI_CHOICES)
    power_outlet_rating = SelectField(u'Power Outlets rating', choices=POWER_CHOICES)
    submit = SubmitField('Submit')


def add_cafe_to_list(entry_to_add):
    with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_data_writer = csv.writer(csv_file, delimiter=',')
        csv_data_writer.writerow(entry_to_add)


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_entry = [
            form.cafe.data,
            form.location.data,
            form.open_time.data,
            form.closing_time.data,
            dict(COFFEE_CHOICES).get(form.coffe_rating.data),
            dict(WIFI_CHOICES).get(form.wifi_rating.data),
            dict(POWER_CHOICES).get(form.power_outlet_rating.data)
        ]
        add_cafe_to_list(new_entry)

        return home()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
