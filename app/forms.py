from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress

class NodeForm(FlaskForm):
    project = SelectField("Проект", choices=[])
    name = StringField("Имя", validators=[DataRequired()])
    ip = StringField("IP", validators=[IPAddress()])
    login = StringField("Логин", validators=[DataRequired()], default="root")
    password = StringField("Пароль")
    submit = SubmitField("Сохранить")