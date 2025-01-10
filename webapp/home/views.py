from flask import Blueprint, render_template

blueprint = Blueprint("home", __name__)

@blueprint.route("/")
def home():
    title = "Онлайн-доска"
    return render_template("home/home.html", page_title=title)
