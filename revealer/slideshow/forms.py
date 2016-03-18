from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileAllowed, FileField
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from .. import slideshows


class SlideshowForm(Form):
    title = StringField('Title', validators=[Required()])
    slides = FileField('Slides', validators=[FileRequired(),
                                             FileAllowed(slideshows,
                                                         'HTML files only!')])
    submit = SubmitField('Upload')
