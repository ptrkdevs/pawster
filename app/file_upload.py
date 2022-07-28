from PIL import Image
from flask import current_app
import os


def handle_upload(file_upload, type, *args, **kwargs):

    filename = file_upload.filename

    ext_type = filename.split(".")[-1]

    types = {
        "profile_picture": "static/images/profile_pictures",
        "pet_picture": "static/images/pet_pictures",
    }

    if type == "profile_picture":

        name = str(kwargs["name"].replace(" ", "_"))
        storage_name = f"{name}.{ext_type}"

        filepath = os.path.join(current_app.root_path, types[type], storage_name)
        # filepath = os.path.join(os.path.dirname(__file__), types[type], storage_name) testing

    if type == "pet_picture":
        storage_name = f"{str(kwargs['id'])}_{filename}"

        filepath = os.path.join(current_app.root_path, types[type], storage_name)

    output_size = (400, 400)

    pic = Image.open(file_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_name
