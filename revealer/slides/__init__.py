from flask import Blueprint

slides = Blueprint('slides', __name__)

from . import views
