from flask import render_template, request
from . import app
from .models import Presentation


@app.route('/', methods=('GET', 'POST'))
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Presentation.query.order_by(Presentation.created.desc())\
        .paginate(page, per_page=5, error_out=False)

    return render_template('index.html', pagination=pagination,
                           presentations=pagination.items)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html"), 401
