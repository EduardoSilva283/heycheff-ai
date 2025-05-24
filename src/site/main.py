from flask import Blueprint,render_template, request

bp_site = Blueprint('site', __name__)

@bp_site.route('/')
def index():
    return render_template('index.html')