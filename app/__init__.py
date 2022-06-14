from flask import Flask, redirect, url_for, flash, render_template, request
from flask_login import login_required, logout_user, current_user
from .config import Config
from .models import db, login_manager, User, Course
from .oauth import blueprint
from .cli import create_db, print_db


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(print_db)
app.cli.add_command(create_db)
db.init_app(app)
login_manager.init_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/createcourse", methods=["POST"])
def create_course():
    content = request.form['content']
    name = request.form['name']
    user_id = current_user.id
    course = Course(name=name, content=content, created_by=user_id)
    db.session.add(course)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/courses")
def courses():
    courses = Course.query.all()
    return render_template("courses.html", courses=courses)
 #course_id=course.id, user_id=current_user.id
 #/<int:course_id>/<int:user_id>
@app.route("/course/save", methods=["POST"])
def save_course():
    course = Course.query.get(request.form['course_id'])
    user = User.query.get(request.form['user_id'])
    user.saved_posts.append(course)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("courses"))