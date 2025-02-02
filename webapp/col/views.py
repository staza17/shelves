from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user

from webapp.db import db

from webapp.col.forms import EditColName
from webapp.cards.models import Cards
from webapp.col.models import Col
from webapp.cards.views import number_minus

blueprint = Blueprint("col", __name__, url_prefix="/col")

@blueprint.route("/edit-col-name/<int:board_id>/<int:col_id>", methods=["GET"])
def edit_col_name(board_id, col_id):
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = EditColName()
    title = "Изменить название колонки"
    col = Col.query.get(col_id)
    return render_template(
        "col/edit_col_name.html", page_title=title, form=form,
        col=col, board_id=board_id)

@blueprint.route("/process-edit-col-name", methods=["Post"])
def process_edit_col_name():
    form = EditColName()
    if form.validate_on_submit():
        col_id = request.form['col']
        col = db.session.query(Col).get(col_id)
        col.col_name = form.name.data
        db.session.commit()
        board_id = request.form['board']
        return redirect(url_for("boards.get_board", id=board_id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}".format(error))
    return redirect(url_for("cards.edit_card"))

@blueprint.route("/move-to-col/<int:board_id>/<int:col_id>/<int:card_id>/", methods=["GET"])
def move_to_col(board_id, col_id, card_id):
    card = db.session.query(Cards).get(card_id)
    prev_col_id = card.col_id
    prev_card_num = card.number
    card.col_id = col_id
    new_cards_list = Cards.query.filter_by(col_id=col_id).all()
    card.number = len(new_cards_list)
    prev_cards_list = Cards.query.filter_by(col_id=prev_col_id).all()
    number_minus(prev_cards_list, prev_card_num)
    db.session.commit()
    return redirect(url_for("boards.get_board", id=board_id))