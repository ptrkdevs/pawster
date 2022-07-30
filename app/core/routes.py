from app.core import bp
from flask import request, abort, render_template, flash, redirect, url_for
from app.models import Pet, Tricks, Images, User
from flask_login import login_required, current_user
from app.core.forms import PetForm, UpdatePetForm, UpdatePetPictures, UpdateTricksForm
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


@bp.route("/home/adoptions", methods=["GET", "POST"])
def adoptions():

    pets = Pet.query.filter(Pet.for_adoption == 0).all()

    if request.method == "POST":
        # search is not empty
        if request.form.get("breed") != "":

            pets = Pet.query.filter(
                Pet.breed == request.form.get("breed"), Pet.for_adoption == 0
            )

    return render_template("index.html", pets=pets)


@bp.route("/pet/<string:id>")
def pet_detail(id: str):

    pet = Pet.query.filter_by(id=id).first()

    if pet is None:
        abort(404)

    pet.owner = User.query.filter_by(id=pet.owner_id).first()
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
        pet.for_adoption = form.for_adoption.data

        db.session.commit()

        return redirect(url_for(".pet_detail", id=pet.id))

    else:

        form.name.data = pet.name
        form.age.data = pet.age
        form.description.data = pet.description

    return render_template("update_petform.html", form=form)


@bp.route("/pet/tricks/delete")
@login_required
def delete_trick():
    pet_id = request.args.get("pet_id")
    id = request.args.get("id")

    pet = Pet.query.filter_by(id=pet_id).first()

    if pet not in current_user.pets:
        flash("cannot perform that operation", "error")
        return redirect(url_for(".pet_detail", id=pet.id))

    trick = Tricks.query.filter_by(id=id).first()

    if pet_id != trick.pet_id or not trick:
        flash("permission denied for that action")
        return redirect(".pet_detail", id=pet_id)
    else:
        db.session.delete(trick)
        db.session.commit()

    return redirect(url_for(".pet_detail", id=pet_id))


# update pet profile picture
@bp.route("/pet/<string:pet_id>media/add", methods=["GET", "POST"])
@login_required
def add_pet_picture(pet_id):

    pet = Pet.query.filter_by(id=pet_id).first()
    form = UpdatePetPictures()

    if form.validate_on_submit():
        if form.images.data:
            for picture in form.images.data:

                pet_img = handle_upload(picture, type="pet_picture", id=pet_id)
                pet_image = Images(image=str(pet_img), pet_id=pet.id)

                db.session.add(pet_image)
                db.session.commit()

            return redirect(url_for(".pet_detail", id=pet.id))

    return render_template("pet_add_media.html", form=form)


# delete picture
@bp.route("/pet/<string:pet_id>/media/delete")
@login_required
def delete_pic_picture(pet_id):

    pet = Pet.query.filter_by(id=pet_id).first()

    if pet not in current_user.pets:
        flash("cannot perform that operation", "error")
        return redirect(url_for(".pet_detail", id=pet.id))

    image_id = request.args.get("image_id")

    pet_image = Images.query.filter_by(id=image_id).first()
    db.session.delete(pet_image)
    db.session.commit()
    flash("image deleted", "success")

    return redirect(url_for(".pet_detail", id=pet.id))


# update tricks
@bp.route("/pet/<string:pet_id>/tricks/add", methods=["GET", "POST"])
@login_required
def add_trick(pet_id):

    pet = Pet.query.filter_by(id=pet_id).first()

    if pet not in current_user.pets:
        flash("cannot perform that operation", "error")
        return redirect(url_for(".pet_detail", id=pet.id))

    form = UpdateTricksForm()

    if form.validate_on_submit():

        trick = Tricks(name=form.name.data, detail=form.detail.data, pet_id=pet.id)

        db.session.add(trick)
        db.session.commit()

        flash("New skill added successfully", "success")
        return redirect(url_for(".pet_detail", id=pet.id))

    return render_template("add_tricks.html", form=form)
