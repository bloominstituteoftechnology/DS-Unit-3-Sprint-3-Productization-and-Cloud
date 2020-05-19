
from flask import Blueprint, jsonify, request, render_template, redirect, flash
from pdb import set_trace as st
from web_app.models import User, db

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users/new")
def new_user():
    return render_template("new_user.html")


@user_routes.route("/users/create", methods=["POST"])
def create_user():
    new_user = User(username=request.form["username"])
    print("FORM DATA:", dict(request.form))
    db.session.add(new_user)
    db.session.commit()
    # flash("asdf")
    return redirect("/users/new")