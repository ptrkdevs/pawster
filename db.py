from app import db, create_app
from app.models import User, Pet


def build():
    app = create_app()
    db.create_all(app=app)


def create_sample():
    pet1 = Pet("gregory", "german shephard", 2)
    pet2 = Pet("andrew eatpoops", "chuhuahua", 3)
    pet3 = Pet("anthony", "golden retriever", 3)

    app = create_app()
    with app.app_context():
        db.session.add(pet1)
        db.session.add(pet2)
        db.session.add(pet3)
        db.session.commit()


if __name__ == "__main__":
    build()
    create_sample()
