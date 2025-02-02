from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user

from webapp.db import db

from webapp.cards.forms import CreateCard, EditCard
from webapp.cards.models import Cards
from webapp.col.models import Col

blueprint = Blueprint("cards", __name__, url_prefix="/cards")

@blueprint.route("/create-card/<int:board_id>//<int:col_id>", methods=["GET"])
def create_card(board_id, col_id):
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = CreateCard()
    title = "Создание карточки"
    return render_template(
        "cards/create_card.html", page_title=title,
        form=form, col_id=col_id, board_id=board_id)

@blueprint.route("/process-create-card", methods=["Post"])
def process_create_card():
    form = CreateCard()
    if form.validate_on_submit():
        col_id = request.form['col']
        board_id = request.form['board']
        all_cards = Cards.query.filter_by(col_id=col_id).all()
        number = len(all_cards) + 1
        card = Cards(text=form.text.data, number=number, col_id=col_id)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for("boards.get_board", id=board_id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}".format(error))
    return redirect(url_for("cards.create_card"))

@blueprint.route("/edit-card/<int:board_id>/<int:card_id>", methods=["GET"])
def edit_card(board_id, card_id):
    if not current_user.is_authenticated:
        return redirect(url_for("user.login"))
    form = EditCard()
    title = "Редактирование карточки"
    card = Cards.query.get(card_id)
    return render_template(
        "cards/edit_card.html", page_title=title,
        form=form, card=card, board_id=board_id)

@blueprint.route("/process-edit-card", methods=["Post"])
def process_edit_card():
    form = EditCard()
    if form.validate_on_submit():
        card_id = request.form['card']
        card = db.session.query(Cards).get(card_id)
        card.text = form.text.data
        db.session.commit()
        board_id = request.form['board']
        return redirect(url_for("boards.get_board", id=board_id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("{}".format(error))
    return redirect(url_for("cards.edit_card"))

def get_prev_id(cards_list, searched_number):
    for card in cards_list:
        if card.number == searched_number:
            prev_id = card.id
            return prev_id

def change_number(prev_id, card_number, card, new_card_number):
    prev_card = db.session.query(Cards).get(prev_id)
    if prev_card:
        prev_card.number = card_number
        card.number = new_card_number
        db.session.commit()

def number_plus(cards_list, card_number):
    for c in cards_list:
        if c.number < card_number:
            prev_card = db.session.query(Cards).get(c.id)
            if prev_card:
                prev_card.number += 1

def number_minus(cards_list, card_number):
    for c in cards_list:
        if c.number > card_number:
            prev_card = db.session.query(Cards).get(c.id)
            if prev_card:
                prev_card.number -= 1

@blueprint.route("/move-card/<int:board_id>/<int:card_id>/<int:act>", methods=["GET"])
def move_card(board_id, card_id, act):
    card = db.session.query(Cards).get(card_id)
    card_number = card.number
    col_id = card.col_id
    cards_list = Cards.query.filter_by(col_id=col_id).all()
    if act == 1:
        number_plus(cards_list, card_number)
        card.number = 1
        db.session.commit()
    elif act == 2:
        new_card_number = card_number - 1
        prev_id = get_prev_id(cards_list, new_card_number)
        change_number(prev_id, card_number, card, new_card_number)
    elif act == 3:
        new_card_number = card_number + 1
        prev_id = get_prev_id(cards_list, new_card_number)
        change_number(prev_id, card_number, card, new_card_number)
    else:
        number_minus(cards_list, card_number)
        card.number = len(cards_list)
        db.session.commit()
    return redirect(url_for("boards.get_board", id=board_id))

@blueprint.route("/del-card/<int:board_id>/<int:card_id>", methods=["GET"])
def del_card(board_id, card_id):
    card = db.session.query(Cards).get(card_id)
    cards_list = Cards.query.filter_by(col_id=card.col_id).all()
    card_number = card.number
    db.session.delete(card)
    number_minus(cards_list, card_number)
    db.session.commit()
    return redirect(url_for("boards.get_board", id=board_id))
