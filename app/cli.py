import click
from flask.cli import with_appcontext
from .models import db, User, Course, saved_posts


@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()
    db.session.commit()
    print("Database tables created")

@click.command(name="printdb")
@with_appcontext
def print_db():
    users = User.query.all()
    courses = Course.query.all()

    for user in users:
        print(user.email, user.saved_posts)
        for course in user.created_posts:
            print(course.name)

    for course in courses:
        print(course.name, course.created_by)