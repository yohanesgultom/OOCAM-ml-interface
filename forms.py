from flask_wtf import FlaskForm
from wtforms import MultipleFileField, DecimalField, IntegerField, SubmitField, FileField
from wtforms.validators import NumberRange, InputRequired

class TrainForm(FlaskForm):
    images = MultipleFileField("Images: ", [InputRequired(),])
    width = IntegerField("Width: ", [InputRequired(), NumberRange(min = 100, max = 2000)], default=256)
    height = IntegerField("Height: ", [InputRequired(), NumberRange(min = 100, max = 2000)], default=256)
    split = DecimalField("Split: ", [InputRequired(), NumberRange(min = 0.0, max = 1.0, message = ("Split must be between 0.0 and 1.0."))], default=0.8)
    epochs = IntegerField("Number of epochs: ", [InputRequired(), NumberRange(min = 1, message = ("A minimum of one epoch must be trained."))], default=10)
    submit = SubmitField("Submit")

class TestForm(FlaskForm):
    images = MultipleFileField("Images: ")
    model = FileField("Model: ")
    labels = FileField("Labels: ")
    submit = SubmitField("Submit")
