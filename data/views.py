from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("/home.html", user=current_user)


@views.route("/T2S_converter")
@login_required
def T2Sapp():
    return render_template("/Text2Speech-converter.html", user=current_user)
