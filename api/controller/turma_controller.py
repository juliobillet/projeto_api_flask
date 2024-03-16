from flask_restful import Resource
from api import api
from ..schemas import turma_schema
from flask import request, make_response, jsonify
from ..dto import turma_dto
from ..service import turma_service


class TurmaController(Resource):
    def get(self):
        turmas = turma_service.listar_turmas()
        validate = turma_schema.TurmaSchema(many=True)
        return make_response(validate.jsonify(turmas), 200)

    def post(self):
        schema_turma = turma_schema.TurmaSchema()
        validate = schema_turma.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_inicio = request.json["data_inicio"]
            data_fim = request.json["data_fim"]
            curso_id = request.json["curso_id"]

            nova_turma = turma_dto.TurmaDTO(
                nome=nome,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                curso_id=curso_id
            )
            retorno = turma_service.cadastrar_turma(nova_turma)
            turma_json = schema_turma.jsonify(retorno)
            return make_response(turma_json, 201)


class TurmaDetailController(Resource):
    def get(self, turma_id):
        turma = turma_service.listar_turma_por_id(turma_id)
        if turma is None:
            return make_response(jsonify("Turma não encontrada!"), 404)

        validate = turma_schema.TurmaSchema()
        return make_response(validate.jsonify(turma), 200)

    def put(self, turma_id):
        turma = turma_service.listar_turma_por_id(turma_id)
        if turma is None:
            return make_response(jsonify("Turma não encontrada!"), 404)
        schema_turma = turma_schema.TurmaSchema()
        validate = schema_turma.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            data_inicio = request.json["data_inicio"]
            data_fim = request.json["data_fim"]
            curso_id = request.json["curso_id"]

            turma_atualizada = turma_dto.TurmaDTO(
                nome=nome,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                curso_id=curso_id
            )
            turma_service.atualizar_turma(turma, turma_atualizada)
            retorno_turma_atualizada = turma_service.listar_turma_por_id(turma_id)
            return make_response(schema_turma.jsonify(retorno_turma_atualizada), 200)

    def delete(self, turma_id):
        turma_bd = turma_service.listar_turma_por_id(turma_id)
        if turma_bd is None:
            return make_response(jsonify("Turma não encontrada!"), 404)
        turma_service.excluir_turma(turma_bd)
        return make_response(jsonify("Turma excluída com sucesso!"), 204)


# Listar e cadastrar turmas
api.add_resource(TurmaController, "/turma")
# Detalhes, atualizar e excluir uma turma específica
api.add_resource(TurmaDetailController, "/turma/<int:turma_id>")
