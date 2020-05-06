from flask_wtf import FlaskForm
from wtforms import MultipleFileField, DecimalField, IntegerField, SubmitField, FileField, RadioField, StringField
from wtforms.validators import ValidationError, NumberRange, InputRequired

class TrainForm(FlaskForm):
    images = MultipleFileField("Images: ", [InputRequired(),])
    width = IntegerField("Width: ", [InputRequired(), NumberRange(min = 100, max = 2000)], default=256)
    height = IntegerField("Height: ", [InputRequired(), NumberRange(min = 100, max = 2000)], default=256)
    split = DecimalField("Split: ", [InputRequired(), NumberRange(min = 0.0, max = 1.0, message = ("Split must be between 0.0 and 1.0."))], default=0.8)
    epochs = IntegerField("Number of epochs: ", [InputRequired(), NumberRange(min = 1, message = ("A minimum of one epoch must be trained."))], default=10)
    submitTrain = SubmitField("Submit")

def required_if_selected_by(select_field):
    message = f'Must be provided if selected by {select_field}'
    def call(form, field):   
        if form[select_field].data == field.name:
            required =  InputRequired(message)
            required(form, field)
    return call

class TestForm(FlaskForm):
    source = RadioField("Source: ", choices=[('images', 'Images'), ('path', 'Path')], default='images')
    path = StringField("Path:", [required_if_selected_by('source')])
    images = MultipleFileField("Images: ", [required_if_selected_by('source')])
    model = FileField("Model: ", [InputRequired(),])
    labels = FileField("Labels: ", [InputRequired(),])
    submitTest = SubmitField("Submit")
    messages = []
