from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
import re
import os
from app import app, db
from app.models import Admin, Nodes
from app.forms import AdminForm, LoginForm, NodeForm
from app.handler import NodeHandler
from yaml import safe_load

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            admin = db.session.query(Admin).filter(Admin.login == form.login.data).one()
            if admin.check_password(form.password.data):
                login_user(admin, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            flash('Неверный логин или пароль')
        except:
            flash('Неверный логин или пароль')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin(login=form.login.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash(f"Добавлен администратор {admin.login}")
        return redirect(url_for("admins"))
    admins = db.session.query(Admin).all()
    return render_template("admins.html", form=form, admins=admins)

@app.route('/admins/del/<int:id>')
@login_required
def admins_del(id):
    admin = db.session.query(Admin).filter(Admin.id==id).one()
    db.session.delete(admin)
    db.session.commit()
    flash(f"Админ {admin.login} удален")
    return redirect(url_for("admins"))

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    nodes = db.session.query(Nodes.project).distinct().all()
    nodes = [ i[0] for i in nodes ]
    path = os.getcwd() + '/app/plugins/'
    plugins = [f.replace(".yml", "") for f in os.listdir(path) if re.search(r'\.yml$', f)]
    form = NodeForm()
    form.project.choices = [ (i, i) for i in plugins ]
    if form.validate_on_submit():
        node = Nodes(project=form.project.data, name=form.name.data, ip=form.ip.data, login=form.login.data, password=form.password.data)
        db.session.add(node)
        db.session.commit()
        flash(f"Нода {node.name} добавлена")
        return redirect(url_for("index"))
    form.process()
    return render_template("index.html", form=form, nodes=nodes)

@app.route("/nodes/<string:name>")
@login_required
def nodes(name):
    nodelist = db.session.query(Nodes).filter(Nodes.project==name).all()
    return render_template("nodes.html", nodelist=nodelist)

@app.route("/stat/<int:id>")
@login_required
def stat(id):
    try:
        node = db.session.query(Nodes).filter(Nodes.id==id).one()
    except:
        return {"error": f"Not found node with id {id}"}
    try:
        f = open(f"app/plugins/{node.project}.yml")
        template = safe_load(f)
        f.close()
    except:
        return {"error": f"Can not open template {node.project}.yml"}
    handler = NodeHandler(ip=node.ip, login=node.login, password=node.password, template=template)
    if handler.conect():
        r = handler.query()
        handler.disconect()
        return r
    else:
        return {"error": f"Can not connect to {handler.login}@{handler.ip}"}