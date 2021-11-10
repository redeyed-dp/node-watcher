from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import IPAddress, NumberRange

class ProxyForm(FlaskForm):
    ip = StringField("IP", validators=[IPAddress()])
    port = IntegerField("Порт", validators=[NumberRange(min=1, max=65535)])
    proto = SelectField("Протокол", choices=('socks5', 'socks4', 'http'))
    login = StringField("Логин")
    password = StringField("Пароль")
    submit = SubmitField("Сохранить")