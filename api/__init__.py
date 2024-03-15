from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
ma = Marshmallow(app)
ma.init_app(app)

api = Api(app)

from api.controller import (
    aluno_controller,
    professor_controller,
    turma_controller,
    disciplina_controller,
    curso_controller
)
from .models import (
    aluno_model,
    professor_model,
    turma_model,
    disciplina_model,
    curso_model
)
