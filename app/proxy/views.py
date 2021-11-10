from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
import requests
from app import db
from app.proxy import bp
from app.proxy.models import Proxy
from app.proxy.forms import ProxyForm

@bp.route("/", methods=['GET', 'POST'])
def index():
    form = ProxyForm()
    if form.validate_on_submit():
        proxy = Proxy(ip=form.ip.data, port=form.port.data, proto=form.proto.data, login=form.login.data, password=form.password.data)
        db.session.add(proxy)
        db.session.commit()
        flash(f"Прокси {proxy.ip}:{proxy.port} добавлен в мониторинг")
        return redirect(url_for("proxy.index"))
    proxies = db.session.query(Proxy).all()
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    try:
        r = requests.get('https://ifconfig.me')
        if r.status_code == 200:
            self_ip = r.text
        else:
            self_ip = r.status_code
    except Exception as e:
        self_ip = e
    return render_template("proxy.html", form=form, proxies=proxies, client_ip=client_ip, self_ip=self_ip)

@bp.route("/del/<int:id>")
def delete(id):
    proxy = db.session.query(Proxy).filter(Proxy.id==id).one()
    db.session.delete(proxy)
    db.session.commit()
    flash(f"Прокси {proxy.ip}:{proxy.port} удален из мониторинга")
    return redirect(url_for("proxy.index"))