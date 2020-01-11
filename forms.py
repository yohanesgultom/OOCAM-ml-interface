from flask_wtf import FlaskForm
from wtforms import MultipleFileField, DecimalField, IntegerField, SubmitField, FileField
from wtforms.validators import NumberRange

class TrainForm(FlaskForm):
    images = MultipleFileField("Images: ")
    split = DecimalField("Split: ", [NumberRange(min = 0.0, max = 1.0, message = ("Split must be between 0.0 and 1.0."))])
    epochs = IntegerField("Number of epochs: ", [NumberRange(min = 1, message = ("A minimum of one epoch must be trained."))])
    submit = SubmitField("Submit")

class TestForm(FlaskForm):
    images = MultipleFileField("Images: ")
    model = FileField("Model: ")
    labels = FileField("Labels: ")
    submit = SubmitField("Submit")
