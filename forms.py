from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CreateNewClassroomForm(FlaskForm):
    name = StringField('Encrypt or Decrypt: ')
    #time = IntegerField('Enter Shift Key(1-26): ', validators=[DataRequired()])
    #message = StringField('Enter Message: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

