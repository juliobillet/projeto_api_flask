from flask_restful import Resource
from api import api
from ..schemas import professor_schema
from flask import request, make_response, jsonify
from ..dto import professor_dto
from ..service import professor_service


class ProfessorController(Resource):
    def get(self):
        professores = professor_service.listar_professores()
        validate = professor_schema.ProfessorSchema(many=True)
        return make_response(validate.jsonify(professores), 200)

    def post(self):
        schema_professor = professor_schema.ProfessorSchema()
        validate = schema_professor.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            disciplina = request.json["disciplina"]
            admissao = request.json["admissao"]

            novo_professor = professor_dto.ProfessorDTO(
                nome=nome,
                disciplina=disciplina,
                admissao=admissao
            )

            retorno = professor_service.cadastrar_professor(novo_professor)
            retorno_json = schema_professor.jsonify(retorno)
            return make_response(retorno_json, 201)


class ProfessorDetailController(Resource):
    def get(self, professor_id):
        professor = professor_service.listar_professor_por_id(professor_id)
        if professor is None:
            return make_response(jsonify("Professor não encontrado!"), 404)

        validate = professor_schema.ProfessorSchema()
        return make_response(validate.jsonify(professor), 200)

    def put(self, professor_id):
        professor = professor_service.listar_professor_por_id(professor_id)
        if professor is None:
            return make_response(jsonify("Professor não encontrado!"), 404)

        schema_professor = professor_schema.ProfessorSchema()
        validate = schema_professor.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            disciplina = request.json["disciplina"]
            admissao = request.json["admissao"]

            novos_dados_professor = professor_dto.ProfessorDTO(
                nome=nome,
                disciplina=disciplina,
                admissao=admissao
            )
            professor_service.atualizar_professor(professor, novos_dados_professor)
            professor_atualizado = professor_service.listar_professor_por_id(professor_id)
            return make_response(schema_professor.jsonify(professor_atualizado), 200)

    def delete(self, professor_id):
        professor_bd = professor_service.listar_professor_por_id(professor_id)
        if professor_bd is None:
            return make_response(jsonify("Professor não encontrado!"), 404)

        professor_service.excluir_professor(professor_bd)
        return make_response(jsonify("Professor excluído com sucesso!"), 204)


# Listar e cadastrar professores
api.add_resource(ProfessorController, "/professor")
# Detalhes, atualizar e excluir um professor específico
api.add_resource(ProfessorDetailController, "/professor/<int:professor_id>")

