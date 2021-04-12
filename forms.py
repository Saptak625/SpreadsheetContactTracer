from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

from dbFunctions import queryByName

class CreateNewClassroomForm(FlaskForm):
    name = StringField('Name Of Class: ',
                        validators=[DataRequired()])
    physicalName = StringField('Room Name: ',
                        validators=[DataRequired()])
    numOfSeats = IntegerField('Number of Seats: ', validators=[DataRequired(), NumberRange(min=1, message="Number of Seats must be at least 1")])
    submit = SubmitField('Submit')   

    def validate_name(form, field):
        queryResults=queryByName(field.data)
        if queryResults != None:
            raise ValidationError("Name must be unique")