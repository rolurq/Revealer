from flask import Blueprint

presentation = Blueprint('presentation', __name__)

from . import views

