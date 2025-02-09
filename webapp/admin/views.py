from flask import Blueprint, render_template

from webapp.user.decorators import admin_required
from webapp.user.models import User
from webapp.boards.models import Boards

blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@blueprint.route("/")
@admin_required
def admin_index():
    title = "Админка"
    users = User.query.all()
    users_boards = {}
    for user in users:
        boards_list = Boards.query.filter_by(user_id=user.id).all()
        users_boards[user.id] = len(boards_list)
    return render_template(
        "admin/index.html", page_title=title,
        users=users, users_boards=users_boards)
