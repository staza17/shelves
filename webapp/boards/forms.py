from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user

from webapp.boards.models import Boards

class CreateBoard(FlaskForm):
    board_name = StringField("Название доски", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Создать", render_kw={"class": "btn btn-primary"})

    def validate_board_name(self, board_name):
        name_count = 0
        boards = Boards.query.filter_by(user_id=current_user.id).all()
        for board in boards:
            if board.board_name == board_name.data:
                name_count += 1
        if name_count > 0:
            raise ValidationError("Доска с таким именем уже существует!")

