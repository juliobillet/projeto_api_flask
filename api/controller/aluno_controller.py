from flask_restful import Resource
from api import api
from ..schemas import aluno_schema
from flask import request, make_response, jsonify
from ..dto import aluno_dto
from ..service import aluno_service


class AlunoController(Resource):
    def get(self):
        alunos = aluno_service.listar_alunos()
        validate = aluno_schema.AlunoSchema(many=True)
        return make_response(validate.jsonify(alunos), 200)

    def post(self):
        schema_aluno = aluno_schema.AlunoSchema()
        validate = schema_aluno.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            data_nascimento = request.json["data_nascimento"]

            novo_aluno = aluno_dto.AlunoDTO(nome=nome, data_nascimento=data_nascimento)

            retorno = aluno_service.cadastrar_aluno(novo_aluno)
            retorno_json = schema_aluno.jsonify(retorno)
            return make_response(retorno_json, 201)


class AlunoDetailController(Resource):
    def get(self, aluno_id):
        aluno = aluno_service.listar_aluno_por_id(aluno_id)
        if aluno is None:
            return make_response(jsonify("Aluno não encontrado!"), 404)

        validate = aluno_schema.AlunoSchema()
        return make_response(validate.jsonify(aluno), 200)

    def put(self, aluno_id):
        aluno = aluno_service.listar_aluno_por_id(aluno_id)
        if aluno is None:
            return make_response(jsonify("Aluno não encontrado!"), 404)

        schema_aluno = aluno_schema.AlunoSchema()
        validate = schema_aluno.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            data_nascimento = request.json["data_nascimento"]

            novos_dados_aluno = aluno_dto.AlunoDTO(nome=nome, data_nascimento=data_nascimento)
            aluno_service.atualizar_aluno(aluno, novos_dados_aluno)
            aluno_atualizado = aluno_service.listar_aluno_por_id(aluno_id)
            return make_response(schema_aluno.jsonify(aluno_atualizado), 200)

    def delete(self, aluno_id):
        aluno_bd = aluno_service.listar_aluno_por_id(aluno_id)
        if aluno_bd is None:
            return make_response(jsonify("Aluno não encontrado!"), 404)

        aluno_service.excluir_aluno(aluno_bd)
        return make_response(jsonify("Aluno excluído com sucesso!"), 204)


# Listar e cadastrar alunos
api.add_resource(AlunoController, "/aluno")
# Detalhes, atualizar e excluir um aluno específico
api.add_resource(AlunoDetailController, "/aluno/<int:aluno_id>")
