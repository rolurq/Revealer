from flask import render_template, redirect, url_for, flash, abort, request
from flask.ext.login import current_user, login_required

from . import slides
from .. import slideshows, resources, db
from ..models import Slideshow
from .forms import SlideshowForm


@slides.route('/slideshows', defaults={'expand': 0}, methods=('GET', 'POST'))
@slides.route('/slideshows/<int:expand>', methods=('GET', 'POST'))
def index(expand):
    page = request.args.get('page', 1, type=int)
    pagination = Slideshow.query.order_by(Slideshow.created.desc())\
        .paginate(page, per_page=10, error_out=False)

    return render_template('slides/index.html', expand=expand,
                           slideshows=pagination.items, pagination=pagination)


@slides.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = SlideshowForm()
    if form.validate_on_submit():
        record = Slideshow(title=form.title.data, user=current_user,
                           description=form.description.data)
        db.session.add(record)
        db.session.commit()

        slideshows.save(form.slides.data, name=str(record.id))

        resources_files = request.files.getlist("resources")
        for resource in resources_files:
            resources.save(resource, folder='%d_files' % record.id)

        flash("Slideshow saved.", category='success')
        return redirect(url_for('slides.view', id=record.id))
    return render_template('slides/upload.html', form=form)


@slides.route('/slide/<int:id>/viewer/')
def view(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='viewer')
    flash("Invalid slideshow.", category='danger')
    return abort(404)


@slides.route('/slide/remove/<int:id>')
@login_required
def remove(id):
    record = Slideshow.query.get(id)
    if record and current_user == record.user:
        record.delete()

        flash("Removed slideshow", category="warning")
        return redirect(url_for('slides.index'))
    return abort(404 if not record else 401)
