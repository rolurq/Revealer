from flask import render_template, abort, request, flash, redirect, url_for
from flask.ext.login import current_user
from jinja2 import TemplateNotFound

from . import app, slideshows, db
from .models import Slideshow

multiplexer = {}
multiplex_count = 0


@app.route('/<presentation_name>/<user_type>', methods=['GET'])
@app.route('/<presentation_name>/', defaults={'user_type': 'client'},
           methods=['GET'])
def slide(presentation_name, user_type):
    global multiplex_count, multiplexer
    try:
        if presentation_name in multiplexer:
            multiplex_id = multiplexer[presentation_name]
        else:
            multiplex_id = multiplex_count
            multiplexer[presentation_name] = multiplex_id
            multiplex_count += 1
        return render_template(presentation_name,
                               user_type=user_type,
                               mult_id=multiplex_id)
    except TemplateNotFound:
        abort(404)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'slideshow' in request.files:
        filename = slideshows.save(request.files['slideshow'])

        record = Slideshow(title=filename, user=current_user)
        db.session.add(record)
        db.session.commit()

        flash("Slideshow saved.")
        return redirect(url_for('slide', presentation_name=filename,
                                user_type='viewer'))
    return render_template('upload.html')


@app.route('/')
def index():
    return render_template('index.html')
