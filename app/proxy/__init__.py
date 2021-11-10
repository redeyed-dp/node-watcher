from flask import Blueprint

bp = Blueprint('proxy', __name__, template_folder='templates')

from app.proxy import views