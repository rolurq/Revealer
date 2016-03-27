from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileAllowed, FileField
from flask.ext.login import current_user
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from wtforms import ValidationError
from .. import slideshows
from ..models import Slideshow


class SlideshowForm(Form):
    title = StringField('Title', validators=[Required()])
    description = TextAreaField('Description')
    slides = FileField('Slides', validators=[FileRequired(),
                                             FileAllowed(slideshows,
                                                         'HTML files only!')],
                       description="You should upload a HTML file")
    submit = SubmitField('Upload')

    def validate_title(self, field):
        if Slideshow.query.filter_by(title=field.data,
                                     user=current_user).first():
            raise ValidationError('Slideshow title already exists')
