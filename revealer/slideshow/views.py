from flask import render_template, redirect, url_for, flash, abort
from flask.ext.login import current_user, login_required
from werkzeug.security import gen_salt
from . import slideshow
from .forms import SlideshowForm
from .. import slideshows, db
from ..models import Slideshow, Presentation


@slideshow.route('/slideshows')
def index():
    return render_template('slideshow/index.html',
                           slideshows=Slideshow.query.all())


@slideshow.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = SlideshowForm()
    if form.validate_on_submit():
        record = Slideshow(title=form.title.data, user=current_user,
                           description=form.description.data)
        db.session.add(record)
        db.session.commit()

        slideshows.save(form.slides.data, name=str(record.id))

        flash("Slideshow saved.", category='success')
        return redirect(url_for('slideshow.view', id=record.id))
    return render_template('slideshow/upload.html', form=form)


@slideshow.route('/slide/<int:id>/master/')
@login_required
def present(id):
    record = Slideshow.query.filter_by(user=current_user).first()
    if record is not None:
        record.present()  # update last_presented value

        # create the presentation instance and the corresponding key
        pres = Presentation(slideshow_hash=gen_salt(12), slideshow=record)
        db.session.add(pres)
        db.session.commit()
        return render_template('slideshows/%s' % id, user_type='master',
                               mult_id=pres.slideshow_hash)
    flash("You can't control this slideshow.", category='danger')
    return abort(401)


@slideshow.route('/slide/<int:id>/client/')
def listen(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='client',
                               mult_id=id)
    flash("Invalid slideshow.", category='danger')


@slideshow.route('/slide/<int:id>/viewer/')
def view(id):
    record = Slideshow.query.get(id)
    if record is not None:
        return render_template('slideshows/%s' % id, user_type='viewer')
    flash("Invalid slideshow.", category='danger')
    return abort(404)


@slideshow.route('/slideshow/remove/<int:id>')
@login_required
def remove(id):
    record = Slideshow.query.get(id)
    if record and current_user == record.user:
        record.delete()

        flash("Removed slideshow", category="warning")
        return redirect(url_for('slideshow.index'))
    return abort(404) if not record else abort(401)
