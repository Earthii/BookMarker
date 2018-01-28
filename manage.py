"""
python3 manage.py to see the available actions
python3 manage.py initdb creates the db
python3 manage.py dropdb deletes the db
python3 manage.py runserver starts the app
"""
from app import app, db
from flask.ext.script import Manager, prompt_bool  # flask script to create admin interface
from app.models import User
from werkzeug.security import generate_password_hash

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="earthii", email="xiao_eric@hotmail.com", password_hash=generate_password_hash("admin")))
    db.session.add(User(username="lei", email="lei@hotmail.com", password_hash=generate_password_hash("123")))
    db.session.commit()
    print("Initialized the database!")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")


if __name__ == "__main__":
    manager.run()