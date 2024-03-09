from api import ma
from ..models import professor_model
from marshmallow import fields


class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = professor_model.ProfessorModel
        load_instance = True
        fields = ("id", "nome", "disciplina", "admissao")

    nome = fields.String(required=True)
    disciplina = fields.String(required=True)
    admissao = fields.Date(required=True)
