from flask import request, make_response, render_template, abort,\
    send_from_directory, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from flask.ext.socketio import emit
from werkzeug.security import gen_salt

from . import presentation
from .. import slideshows, db, socketio
from ..models import Slideshow, Presentation


@presentation.route('/present/<int:id>')
@login_required
def present(id):
    record = Slideshow.query.get(id)
    if record is not None and record.user == current_user:
        record.present()  # update last_presented value

        # create the presentation instance and the corresponding key
        pres = Presentation(slideshow_hash=gen_salt(12), slideshow=record)
        db.session.add(pres)
        db.session.commit()

        pres_id = pres.id  # clousure presentation id

        @socketio.on('connect', namespace='/%s' % pres.slideshow_hash)
        def connect():
            pres = Presentation.query.get(pres_id)
            pres.connected()

            # return pres.state  # newly connected client gets the current state

        @socketio.on('disconnect', namespace='/%s' % pres.slideshow_hash)
        def disconnect():
            pres = Presentation.query.get(pres_id)
            pres.disconnected()

        @socketio.on('state', namespace='/%s' % pres.slideshow_hash)
        def state(data):
            # pres = Presentation.query.get(pres_id)
            # pres.statechanged(data)  # update state for incoming clients

            emit('statechanged', data, broadcast=True)

        return redirect(url_for('presentation.control',
                                hash=pres.slideshow_hash))
    flash("You can't present this slideshow.", category='danger')
    return abort(401)


@presentation.route('/presentation/stop', methods=('POST',))
@login_required
def stop():
    id = request.form.get('id', 0, type=int)
    record = Presentation.query.get(id)
    if record is not None and record.slideshow.user == current_user:
        record.delete()
        return make_response('OK', 200)
    return make_response('Unauthorized', 401) if record else\
        make_response('Not Found', 404)


@presentation.route('/presentation/<string:hash>/master/')
@login_required
def control(hash):
    record = Presentation.query.filter_by(slideshow_hash=hash).first()
    if record and record.slideshow.user == current_user:
        return render_template('slideshows/%s' % record.slideshow.id,
                               user_type='master',
                               mult_id=record.slideshow_hash)
    return abort(404 if not record else 401)


@presentation.route('/presentation/<string:hash>/client/')
def listen(hash):
    record = Presentation.query.filter_by(slideshow_hash=hash).first_or_404()
    return render_template('slideshows/%s' % record.slideshow.id,
                           user_type='client',
                           mult_id=record.slideshow_hash)


# serve resource files
@presentation.route('/presentation/<string:hash>/master/files/'
                    '<string:archive>', defaults={'id': 0})
@presentation.route('/presentation/<string:hash>/client/files/'
                    '<string:archive>', defaults={'id': 0})
@presentation.route('/presentation/<int:id>/viewer/files/<string:archive>',
                    defaults={'hash': None})
def files(archive, hash, id):
    if not id:
        record = Presentation.query.filter_by(slideshow_hash=hash)\
            .first_or_404()
        id = record.slideshow.id

    return send_from_directory(slideshows.path('%d_files' % id), archive)
