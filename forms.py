from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired

class PostForm(FlaskForm):
    headline = StringField('Headline', validators=[DataRequired()])
    textarea = TextAreaField('Text', validators=[DataRequired(), Length(min=6, max=4000)]) 
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), Length(min=3, max=4000)]) 
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
