from flask import render_template, flash, redirect, url_for
import re
import os
from app import app, db
from app.models import Nodes
from app.forms import NodeForm
from app.handler import NodeHandler
from yaml import safe_load

@app.route("/", methods=['GET', 'POST'])
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
def nodes(name):
    nodelist = db.session.query(Nodes).filter(Nodes.project==name).all()
    return render_template("nodes.html", nodelist=nodelist)

@app.route("/stat/<int:id>")
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