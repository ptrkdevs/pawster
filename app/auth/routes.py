from app.auth import bp
from flask import render_template, redirect, url_for, flash, request, abort
from app.auth.forms import LoginForm, RegisterForm, UpdateForm
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.file_upload import handle_upload


@bp.route("/login", methods=["GET", "POST"])
def login():

    print(request.path)

    if current_user.is_authenticated:
        return redirect(url_for("core.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(password=form.password.data):

            login_user(user)

            flash(f"Welcome back {current_user.name}", "success")

            return redirect(url_for("core.dashboard"))

        flash(" email or password incorrect.", "error")

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data, email=form.email.data, password=form.password.data
        )

        db.session.add(user)

        db.session.commit()

        return redirect(url_for("core.dashboard"))

    return render_template("auth/register.html", form=form)


@bp.route("/profile/<string:id>")
def profile(id: str):

    user = User.query.filter_by(id=id).first()

    if user is None:
        abort(404)

    return render_template("auth/profile.html", profile=user)


@bp.route("/profile/update", methods=["GET", "POST"])
@login_required
def update_profile():

    form = UpdateForm()

    if form.validate_on_submit():

        if form.profile_image.data:
            # means user has upload a profile image
            pic_file = handle_upload(
                file_upload=form.profile_image.data,
                type="profile_picture",
                name=current_user.name,
            )
            current_user.profile_image = pic_file

        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.contact_number = form.contact_number.data

        db.session.commit()
        return redirect(url_for(".profile", id=current_user.id))

    if request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.contact_number.data = current_user.contact_number

    return render_template("auth/updateform.html", form=form)


@bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for(".login"))
