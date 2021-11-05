from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired, IPAddress

class AdminForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired(message='Введите логин')])
    password = StringField('Пароль', validators=[InputRequired(message='Введите пароль')])
    submit = SubmitField('Сохранить')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[InputRequired(message='Введите логин')])
    password = PasswordField('Пароль', validators=[InputRequired(message='Введите пароль')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class NodeForm(FlaskForm):
    project = SelectField("Проект", choices=[])
    name = StringField("Имя", validators=[DataRequired()])
    ip = StringField("IP", validators=[IPAddress()])
    login = StringField("Логин", validators=[DataRequired()], default="root")
    password = StringField("Пароль")
    submit = SubmitField("Сохранить")