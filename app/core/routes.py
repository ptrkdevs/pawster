from app.core import bp
from flask import request, abort
from flask import render_template
from app.models import Pet


@bp.route("/")
def welcome():

    return render_template("welcome.html")


@bp.route("/home", methods=["GET", "POST"])
def dashboard():

    pets = Pet.query.all()

    if request.method == "POST":
        # search is not empty
        if request.form.get("breed") != "":

            pets = Pet.query.filter(Pet.breed == request.form.get("breed"))

    return render_template("index.html", pets=pets)


@bp.route("/pet/<string:id>")
def pet_detail(id: str):

    pet = Pet.query.filter_by(id=id).first()

    if pet is None:
        abort(404)

    return render_template("pet_details.html", pet=pet)
