from flask_wtf import FlaskForm
#two FileField possible, which one to take? wtforms or flask_wtf.file?
#from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SubmitField, FileField, validators
from wtforms.validators import Length, DataRequired

class PostForm(FlaskForm):
    headline = StringField('Headline', validators=[DataRequired()])
    snippet = TextAreaField('Snippet', validators=[DataRequired(), Length(min=6, max=4000)])
    textarea = TextAreaField('Text', validators=[DataRequired(), Length(min=6, max=4000)])
    image = FileField('Image')
    submit = SubmitField("Submit")


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=3, max=4000)]) 
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
