from app.core import bp
from flask import request, abort, render_template, flash, redirect, url_for
from app.models import Pet, Tricks, Images
from flask_login import login_required, current_user
from app.core.forms import PetForm, UpdatePetForm
from app import db
from app.file_upload import handle_upload


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


@bp.route("/pet/post", methods=["GET", "POST"])
@login_required
def pet_post():

    form = PetForm()

    if form.validate_on_submit():

        pet = Pet(name=form.name.data, breed=form.breed.data, age=form.age.data)

        pet.owner_id = current_user.id

        db.session.add(pet)
        db.session.commit()

        flash("Post created", "success")
        return redirect(url_for(".dashboard"))

    return render_template("post_pet.html", form=form)


@bp.route("/pet/details/<string:id>", methods=["GET", "POST"])
@login_required
def update_pet_details(id):

    pet = Pet.query.filter_by(id=id).first()

    form = UpdatePetForm()

    if pet is None or pet.owner_id != current_user.id:
        flash("You dont have rights to update this profile", "error")
        return redirect(url_for(".pet_detail", id=pet.id))

    if form.validate_on_submit():

        if form.profile_image.data:
            profile_img = handle_upload(
                form.profile_image.data, type="pet_picture", id=pet.id
            )

            pet.profile_image = profile_img

        pet.name = form.name.data
        pet.description = form.description.data
        pet.age = form.age.data

        db.session.commit()

        return redirect(url_for(".pet_detail", id=pet.id))

    else:

        form.name.data = pet.name
        form.age.data = pet.age
        form.description.data = pet.description

    return render_template("update_petform.html", form=form)


@bp.route("/trick/delete")
def delete_trick():
    id = request.args.get("id")

    trick = Tricks.query.filter_by(id=id).first()
    pet_id = trick.pet_id

    db.session.delete(trick)
    db.session.commit()

    return redirect(url_for(".pet_detail", id=pet_id))
