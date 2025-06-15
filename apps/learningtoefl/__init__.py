from flask import Blueprint

blueprint = Blueprint(
    'learningtoefl_blueprint',
    __name__,
    url_prefix='/learning/toefl'
)
