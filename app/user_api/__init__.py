from flask import Blueprint

bp = Blueprint('user_api', __name__)

from app.user_api import routes
