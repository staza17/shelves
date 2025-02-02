from flask import Blueprint, render_template
from flask_login import current_user

from webapp.boards.models import Boards

blueprint = Blueprint("home", __name__)

@blueprint.route("/")
def index():
    title = "Онлайн-доска"
    if current_user.is_authenticated:
        boards_list = Boards.query.filter_by(user_id=current_user.id).all()
        return render_template("home/index.html", page_title=title, boards_list=boards_list)
    return render_template("home/index.html", page_title=title)
