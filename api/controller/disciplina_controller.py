from flask_restful import Resource
from api import api
from ..schemas import disciplina_schema
from flask import request, make_response, jsonify
from ..dto import disciplina_dto
from ..service import disciplina_service


class DisciplinaController(Resource):
    def get(self):
        disciplinas = disciplina_service.listar_disciplinas()
        validate = disciplina_schema.DisciplinaSchema(many=True)
        return make_response(validate.jsonify(disciplinas), 200)

    def post(self):
        schema_disciplina = disciplina_schema.DisciplinaSchema()
        validate = schema_disciplina.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]

            nova_disciplina = disciplina_dto.DisciplinaDTO(nome=nome)
            retorno = disciplina_service.cadastrar_disciplina(nova_disciplina)
            disciplina_json = schema_disciplina.jsonify(retorno)
            return make_response(disciplina_json, 201)


class DisciplinaDetailController(Resource):
    def get(self, disciplina_id):
        disciplina = disciplina_service.listar_disciplinas_por_id(disciplina_id)
        if disciplina is None:
            return make_response(jsonify("Disciplina não encontrada!"), 404)

        validate = disciplina_schema.DisciplinaSchema()
        return make_response(validate.jsonify(disciplina), 200)

    def put(self, disciplina_id):
        disciplina = disciplina_service.listar_disciplinas_por_id(disciplina_id)
        if disciplina is None:
            return make_response(jsonify("Disciplina não encontrada!"), 404)
        schema_disciplina = disciplina_schema.DisciplinaSchema()
        validate = schema_disciplina.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]

            disciplina_atualizada = disciplina_dto.DisciplinaDTO(nome=nome)
            disciplina_service.atualizar_disciplina(disciplina, disciplina_atualizada)
            retorno_disciplina_atualizada = disciplina_service.listar_disciplinas_por_id(disciplina_id)
            return make_response(schema_disciplina.jsonify(retorno_disciplina_atualizada), 200)

    def delete(self, disciplina_id):
        disciplina_bd = disciplina_service.listar_disciplinas_por_id(disciplina_id)
        if disciplina_bd is None:
            return make_response(jsonify("Disciplina não encontrada!"), 404)
        disciplina_service.excluir_disciplina(disciplina_bd)
        return make_response(jsonify("Disciplina excluída com sucesso!"), 204)


# Listar e cadastrar disciplinas
api.add_resource(DisciplinaController, "/disciplina")
# Detalhes, atualizar e excluir uma disciplina específica
api.add_resource(DisciplinaDetailController, "/disciplina/<int:disciplina_id>")
