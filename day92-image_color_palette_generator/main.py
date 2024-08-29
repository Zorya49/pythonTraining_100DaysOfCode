import atexit
import math
import os
from collections import Counter

from PIL import Image
from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from numpy import asarray
from werkzeug.utils import secure_filename
from wtforms import FileField, SelectField, SubmitField
from wtforms.validators import DataRequired

AMOUNT_CHOICES = [("5", "5"), ("10", "10"), ("25", "25"), ("50", "50"), ("100", "100")]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sasdasdKR6b'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

Bootstrap5(app)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def image_top_colours(image_path, no_top_colors):
    image = Image.open(image_path)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    img_array = asarray(image)
    reshaped_array = img_array.reshape(-1, 3)
    pixels_colors = [rgb_to_hex(pixel) for pixel in reshaped_array]
    color_counts = Counter(pixels_colors)
    pixel_count = color_counts.total()
    top_color_counts = color_counts.most_common(no_top_colors)
    return [[color[0], "{:.5f}%".format(color[1] / pixel_count)] for color in top_color_counts]


class ImageUploadForm(FlaskForm):
    image = FileField('Upload Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    colors_amount = SelectField(u'Amount of top colors to extract', choices=AMOUNT_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ImageUploadForm()
    if form.validate_on_submit():
        colors_amount = form.colors_amount.data
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        session['image_path'] = image_path
        session['colors_amount'] = int(colors_amount)
        return redirect(url_for('generate'))
    return render_template('index.html', form=form)


@app.route('/palette')
def generate():
    image_path = session.pop('image_path', None)
    colors_amount = session.pop('colors_amount', None)
    colors_list = image_top_colours(image_path, colors_amount)
    return render_template('palette.html', colors=colors_list, image_url=image_path)


def delete_all_uploads():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            app.logger.error(f"Failed to delete {file_path}. Reason: {e}")


atexit.register(delete_all_uploads)


if __name__ == '__main__':
    app.run(debug=True)
