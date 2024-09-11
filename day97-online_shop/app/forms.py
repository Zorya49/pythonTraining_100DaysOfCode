from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, IntegerField, FloatField, FileField, SubmitField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    image = FileField('Upload Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    price = FloatField(validators=[DataRequired()])
    stock = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Add product')
