from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user


from webapp.db import db
from webapp.boards.forms import CreateBoard
from webapp.boards.models import Boards
from webapp.cards.models import Cards
from webapp.col.models import Col

blueprint = Blueprint("boards", __name__, url_prefix="/boards")

@blueprint.route("/<int:id>", methods=["GET"])
def get_board(id):
    board = Boards.query.filter_by(id=id).first()
    title = board.board_name
    cols = Col.query.filter_by(board_id=id).order_by(Col.number).all()
    cards_list = []
    col_len = {}
    col_short_name = {}
    for col in cols:
        cards = Cards.query.filter_by(col_id=col.id).order_by(Cards.number).all()
        col_len[col.id] = len(cards)
        name = col.col_name
        if len(name) <= 21:
            col_short_name[col.id] = name
        else:
            col_short_name[col.id] = name[:18] + "..."
        for card in cards:
            cards_list.append(card)
    return render_template(
        "boards/board.html", page_title=title,
        board_id=id, cards_list=cards_list, col_list=cols, col_len=col_len, col_short_name=col_short_name
    )

@blueprint.route("/create-board")
def create_board():
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = CreateBoard()
    title = "Создание новой доски"
    return render_template("boards/create_board.html", page_title=title, form=form)

@blueprint.route("/process-create-board", methods=["Post"])
def process_create_board():
    form = CreateBoard()
    if form.validate_on_submit():
        board = Boards(board_name=form.board_name.data, user_id=current_user.id)
        db.session.add(board)
        db.session.commit()
        col1 = Col(col_name="1", number=1, board_id=board.id)
        col2 = Col(col_name="2", number=2, board_id=board.id)
        col3 = Col(col_name="3", number=3, board_id=board.id)
        db.session.add(col1)
        db.session.add(col2)
        db.session.add(col3)
        db.session.commit()
        flash("Доска успешно создана")
        return redirect(url_for("home.index"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}".format(error))
    return redirect(url_for("boards.create_board"))

@blueprint.route("/del-board/<int:board_id>", methods=["GET"])
def del_board(board_id):
    board = Boards.query.filter_by(id=board_id).first()
    return render_template("boards/delete_board.html", page_title="Удаление доски", board=board)

@blueprint.route("/process-del-board/<int:board_id>", methods=["POST"])
def process_del_board(board_id):
    board = db.session.query(Boards).get(board_id)
    col_list = Col.query.filter_by(board_id=board_id)
    for col in col_list:
        cards_list = Cards.query.filter_by(col_id=col.id).all()
        for card in cards_list:
            db.session.delete(card)
        db.session.delete(col)
    db.session.delete(board)
    db.session.commit()
    flash("Доска удалена")
    return redirect(url_for("home.index"))