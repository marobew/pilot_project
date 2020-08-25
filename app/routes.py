from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse


@app.route("/test")
def test():
    return render_template("test_like.html")


@app.route("/")
@app.route("/index")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.posted_at.desc()).paginate(
        page, 6, error_out=False
    )
    return render_template("post/index.html", posts=posts)


""" USER """


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("이름 또는 비밀번호가 맞지 않습니다. ")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("user/login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("회원가입이 완료되었습니다!")
        return redirect(url_for("login"))
    return render_template("/user/register.html", title="Register", form=form)


@app.route("/mypage", methods=["GET", "POST"])
def mypage():
    if current_user.is_authenticated:
        return render_template("/user/mypage.html")
    return render_template("/post/index.html")


@app.route("/mypage/edit", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = session.get("id")
        password = request.form["password"]
        print(password)
        if not user.check_password(password):
            flash("비밀번호가 맞지 않습니다. ")
            return redirect(url_for("edit_profile"))
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash("수정이 완료되었습니다!")
        return redirect(url_for("mypage"))
    return render_template("/user/edit_profile.html", form=form)


""" /USER """

""" POST """

# create
@app.route("/add", methods=["POST", "GET"])
def add():
    if current_user.is_authenticated:
        form = PostForm()
        if request.method == "POST":
            user = current_user
            user.point += int(10)
            user.level = int(user.point // 100 + 1)
            # print(user.point)
            anony = form.anonymous.data
            if anony == True:
                post = Post(
                    sender=None,  # 나중에 수정해야함
                    title=form.title.data,
                    receiver=form.receiver.data,
                    content=form.content.data,
                )
            else:
                post = Post(
                    sender=current_user.id,
                    title=form.title.data,
                    receiver=form.receiver.data,
                    content=form.content.data,
                )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("post/add.html", form=form)


# delete
@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))


# update
@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    form = PostForm()
    post = Post.query.get(id)
    if request.method == "POST":
        post.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("post/edit.html", post=post, form=form)


"""  /POST """
