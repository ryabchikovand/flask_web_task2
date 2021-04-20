"""
Базовый обработчик для простого приложения
"""
from app import app, db
from flask import render_template, request, redirect, flash, url_for
from app.forms.user import LoginForm, RegisterForm, EditForm
from app.forms.post import CreatePostForm, EditPostForm, DeletePostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models.user import User
from app.models.post import Post
from werkzeug.urls import url_parse
from datetime import datetime
import random


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    """
    Функция выводит рандомные посты с заданным количеством постов- posts_quantity = .
    :return:
    """
    posts_quantity = 3
    posts = Post.query.all()
    ids = [post.id for post in posts]
    random_ids = set()
    while len(random_ids) < posts_quantity:
        random_id = random.randint(min(ids), max(ids))
        random_ids.add(random_id)
    random_posts = [post for post in posts if post.id in random_ids]
    return render_template("home.html", title="Home", posts=random_posts)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = EditForm()
    form.set_current_user(current_user)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=current_user.username).first()
        user.set_password(form.new_password_1.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats! You account been created!")
        return redirect(url_for("edit"))
    return render_template("edit.html", title="Edit", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users'))

    form = RegisterForm()
    if request.method == "POST" and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats! You account been created!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/about", methods=["GET"])
@login_required
def about():
    return render_template("about.html", title="About")


@app.route("/logout", methods=["GET"])
def logout():
    flash("User successfully logged out")
    logout_user()
    return redirect(url_for("users"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    form = LoginForm()
    if request.method == "POST" and form.validate():
        # Пытаемся найти пользвоателя с таким username в бд
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # Добавляем пользователя в сессию
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page:
            next_page = url_for("users")

        return redirect(next_page)
    return render_template("login.html", title="Log In", form=form)


@app.route("/posts", methods=["GET"])
def posts():
    # posts = Post.query.all()
    posts = Post.query.order_by(Post.time_updated.desc()).all()
    return render_template("posts.html", title="Posts", posts=posts)


@app.route("/posts/<int:id>", methods=["GET"])
@login_required
def post_page(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post_page.html", title="Posts", post=post)


@app.route("/posts/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(id):
    """
    Функция редактирует существующий пост
    :return:
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    next_page = request.args.get("edit_post")
    if not next_page:
        next_page = url_for("posts")
    form = EditPostForm()
    if request.method == "POST":
        post = Post.query.filter_by(id=id).first()
        post.title = form.title.data
        post.body = form.body.data
        post.author = form.author.data
        post.time_updated = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        flash("Congrats! Your post has been edited!")
        return redirect(url_for("posts"))
    return render_template("edit_post.html", title="Edit post", form=form)


@app.route("/posts/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(id):
    """
    Функция удаляет пост
    :param id:
    :return:
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    next_page = request.args.get("delete_post")
    if not next_page:
        next_page = url_for("posts")
    form = DeletePostForm()
    post = Post.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted.")
        return redirect(url_for("posts"))
    return render_template("delete_post.html", title="Deleting post", form=form, post=post)



@app.route("/posts/new", methods=["GET", "POST"])
@login_required
def new_post():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    next_page = request.args.get("new_post")
    if not next_page:
        next_page = url_for("posts")
    form = CreatePostForm()
    if request.method == "POST" and form.validate():
        post = Post(title=form.title.data, body=form.body.data, author=form.author.data)
        db.session.add(post)
        db.session.commit()
        flash("Congrats! Your new post has been created!")
        return redirect(url_for("posts"))
    return render_template("new_post.html", title="New Post", form=form)



@app.route("/users", methods=["GET"])
def users():
    users = [
        {
            "username" : "Alex",
            "description" : "Alex's description",
            "posts" : {
                "first" : "First super Alex's post"
            }
        }, 
        {
            "username" : "Bob",
            "description" : "Bob's description",
            "posts" : {
                "first" : "First Bob's post"
            }
        }, 
        {
            "username" : "Alice",
            "description" : "Alice's description",
            "posts" : {
                "first" : "First Alice's post"
            }
        },
    ]

    return render_template("users.html", users=users, username="Fedya", title="User Page")