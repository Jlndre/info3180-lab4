from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):

    photo = FileField('Photo', validators=[
        FileRequired(message='File field cannot be empty!'),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only! (jpg, jpeg, png)')
    ])

    # (Optional) Add a submit button if you want
    submit = SubmitField('Upload')

