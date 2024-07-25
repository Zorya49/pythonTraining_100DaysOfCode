from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import requests
import os


API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = os.getenv('RAPIDAPI_HOST')
URL_LANG_ENDPOINT = 'https://lecto-translation.p.rapidapi.com/v1/translate/languages'
URL_TRANSLATE_ENDPOINT = 'https://lecto-translation.p.rapidapi.com/v1/translate/text'

HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST,
    'Content-Type': "application/json"
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sasdasdKR6b'
Bootstrap5(app)


def get_languages():
    response = requests.get(url=URL_LANG_ENDPOINT, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def translate(source_text: str, source_lang: str, destination_lang: str) -> str:
    payload = {
        'texts': [source_text],
        'to': [destination_lang],
        'from': source_lang
    }
    response = requests.post(URL_TRANSLATE_ENDPOINT, json=payload, headers=HEADERS)
    response.raise_for_status()
    translated_text = response.json()['translations'][0]['translated'][0]
    return translated_text


SRC_LANGUAGE_CHOICES = []
DEST_LANGUAGE_CHOICES = []
languages = get_languages()
for language in languages['languages']:
    if language['support_source']:
        SRC_LANGUAGE_CHOICES.append((language['language_code'], language['display_name']))
    if language['support_target']:
        DEST_LANGUAGE_CHOICES.append((language['language_code'], language['display_name']))


class TranslateForm(FlaskForm):
    source_text = StringField('Source Text', validators=[DataRequired()])
    source_language = SelectField(u'Source language', choices=SRC_LANGUAGE_CHOICES, validators=[DataRequired()])
    destination_language = SelectField(u'Destination language', choices=DEST_LANGUAGE_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Translate!')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = TranslateForm()
    if form.validate_on_submit():
        destination_text = translate(form.source_text.data, form.source_language.data, form.destination_language.data)
        return render_template('index.html', form=form, destination_text=destination_text)
    destination_text = ''
    return render_template('index.html', form=form, destination_text=destination_text)


if __name__ == '__main__':
    app.run(debug=False)
