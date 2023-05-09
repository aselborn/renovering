from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Rubrik', validators=[DataRequired()])
    content = TextAreaField('Beskrivning', validators=[DataRequired()])
    date_start = DateField('Startdatum', validators=[DataRequired()])
    date_end = DateField('Slutdatum')
    
    submit = SubmitField('Spara')

