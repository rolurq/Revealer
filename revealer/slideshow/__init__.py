from flask import Blueprint

slideshow = Blueprint('slideshow', __name__)

from . import views
