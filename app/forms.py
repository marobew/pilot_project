from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Required
from app.models import User, Post


class PostForm(FlaskForm):
    receiver = StringField("받는분", validators=[DataRequired()])
    title = StringField("제목", validators=[DataRequired()])
    content = StringField("내용", validators=[DataRequired()])
    anonymous = BooleanField("익명으로 작성하기")
    submit = SubmitField("작성하기")


class LoginForm(FlaskForm):
    username = StringField("이름", validators=[DataRequired()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    remember_me = BooleanField("로그인 상태 유지")
    submit = SubmitField("로그인")


class RegistrationForm(FlaskForm):
    username = StringField("이름", validators=[DataRequired()])
    email = StringField("이메일", validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    password2 = PasswordField(
        "비밀번호 확인하기", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("회원가입")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("이미 존재하는 이름입니다. ")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("이미 존재하는 계정입니다. ")


class EditProfileForm(FlaskForm):
    password = PasswordField("현재 비밀번호", validators=[DataRequired()])
    new_password = PasswordField("새로운 비밀번호", validators=[DataRequired()])
    new_password2 = PasswordField(
        "비밀번호 확인하기", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("수정하기")
