from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RunForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])
    averagePace = StringField('Average Per Mile', validators=[DataRequired(), ])
    submit = SubmitField('Go')




