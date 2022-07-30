from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    MultipleFileField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from app.models import Pet


class PetForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired("Name is required.")])
    breed = StringField("Breed", validators=[DataRequired("Breed cannot be empty.")])
    age = StringField("Age", validators=[DataRequired("Age cannot be empty.")])

    submit = SubmitField(
        "Add post",
    )


class UpdatePetForm(FlaskForm):

    profile_image = FileField("Profile image", validators=[FileAllowed(["jpg", "png"])])
    name = StringField("Name", validators=[DataRequired("Name is required.")])
    description = TextAreaField("Description")
    for_adoption = SelectField("For adoption", choices=[(0, "yes"), (1, "no")])
    age = StringField("Age", validators=[DataRequired("Age cannot be empty.")])

    submit = SubmitField(
        "Update",
    )


class UpdatePetPictures(FlaskForm):

    images = MultipleFileField("Pet pictures", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Add")


class UpdateTricksForm(FlaskForm):

    name = StringField("Trick", validators=[DataRequired("Name is required.")])
    detail = StringField("Detail", validators=[DataRequired("Name is required.")])

    submit = SubmitField(
        "Add trick",
    )
