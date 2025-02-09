from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateCard(FlaskForm):
    text = StringField("Текст", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Создать", render_kw={"class": "btn btn-dark-brown"})

class EditCard(FlaskForm):
    text = StringField("Текст", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Применить", render_kw={"class": "btn btn-dark-brown"})