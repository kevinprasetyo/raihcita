from flask import Blueprint

blueprint = Blueprint(
    'learningielts_blueprint',
    __name__,
    url_prefix='/learning/ielts'
)