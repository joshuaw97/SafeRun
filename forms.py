from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RunForm(FlaskForm):
    username = StringField('Location',
                           validators=[DataRequired(), Length(min=2, max=20)])
    userpace = StringField('Average Pace',
                        validators=[DataRequired()])

    submit = SubmitField('Go')


