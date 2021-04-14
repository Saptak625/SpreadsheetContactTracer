from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

from dbFunctions import queryByName, checkPhysicalClassroom

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

    def validate_numOfSeats(form, field):
        result = checkPhysicalClassroom(form.physicalName.data)
        if result != None:
            if result[1] != field.data:
                raise ValidationError(f"Num of Seats must match Num of Seats({result[1]}) of other classes in same room.")


class ContactTracingForm(FlaskForm):
    email = StringField('Student Email: ',
                        validators=[DataRequired()])
    startDate = DateField('Start Date', format='%m/%d/%Y')
    submit = SubmitField('Find')