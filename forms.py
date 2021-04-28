from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

from dbFunctions import queryByName, checkPhysicalClassroom, checkEmailInDatabase
import datetime

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
    startDate = DateField('Start Date(m/d/yyyy): ', format='%m/%d/%Y', validators=[DataRequired()])
    maxChainLength = IntegerField('Number of Iterations: ', validators=[DataRequired(), NumberRange(min=1, max=5, message="Please choose a number of iterations between 1 to 5.")])
    submit = SubmitField('Find')

    def validate_email(form, field):
        results = checkEmailInDatabase(field.data)
        if results == None:
            raise ValidationError(f"Email doesn't exist in database. Please check again.")

    def validate_startDate(form, field):
        currentDate = datetime.date.today()
        if currentDate - field.data > datetime.timedelta(days=14):
            raise ValidationError(f"Date must be within 14 days.")

class CheckBox(FlaskForm):
    checkbox=BooleanField('Desk', default=True)

class ListOfCheckBoxes(FlaskForm):
    listOfChecks=FieldList(FormField(CheckBox), min_entries=3)

class DeskAssociationsForm(FlaskForm):
    desks=FieldList(FormField(ListOfCheckBoxes), min_entries=3)
    submit = SubmitField('Submit') 