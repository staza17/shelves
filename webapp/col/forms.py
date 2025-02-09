from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class EditColName(FlaskForm):
    name = StringField("Название", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Применить", render_kw={"class": "btn btn-dark-brown"})