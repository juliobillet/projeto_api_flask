from flask_restful import Resource
from api import api
from ..schemas import curso_schema
from flask import request, make_response, jsonify
from ..dto import curso_dto
from ..service import curso_service


class CursoController(Resource):
    def get(self):
        cursos = curso_service.listar_cursos()
        validate = curso_schema.CursoSchema(many=True)
        return make_response(validate.jsonify(cursos), 200)

    def post(self):
        schema_curso = curso_schema.CursoSchema()
        validate = schema_curso.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            disciplinas = request.json["disciplinas"]

            novo_curso = curso_dto.CursoDTO(
                nome=nome,
                descricao=descricao,
                disciplinas=disciplinas
            )
            retorno = curso_service.cadastrar_curso(novo_curso)
            curso_json = schema_curso.jsonify(retorno)
            return make_response(curso_json, 201)


class CursoDetailController(Resource):
    def get(self, curso_id):
        curso = curso_service.listar_curso_por_id(curso_id)
        if curso is None:
            return make_response(jsonify("Curso não encontrado!"), 404)

        validate = curso_schema.CursoSchema()
        return make_response(validate.jsonify(curso), 200)

    def put(self, curso_id):
        curso = curso_service.listar_curso_por_id(curso_id)
        if curso is None:
            return make_response(jsonify("Curso não encontrado!"), 404)
        schema_curso = curso_schema.CursoSchema()
        validate = schema_curso.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            disciplinas = request.json["disciplinas"]

            curso_atualizado = curso_dto.CursoDTO(
                nome=nome,
                descricao=descricao,
                disciplinas=disciplinas
            )
            curso_service.atualizar_curso(curso, curso_atualizado)
            retorno_curso_atualizado = curso_service.listar_curso_por_id(curso_id)
            return make_response(schema_curso.jsonify(retorno_curso_atualizado), 200)

    def delete(self, curso_id):
        curso_bd = curso_service.listar_curso_por_id(curso_id)
        if curso_bd is None:
            return make_response(jsonify("Curso não encontrado!"), 404)
        curso_service.excluir_curso(curso_bd)
        return make_response(jsonify("Curso excluído com sucesso!"), 204)


# Listar e cadastrar cursos
api.add_resource(CursoController, "/curso")
# Detalhes, atualizar e excluir um curso específico
api.add_resource(CursoDetailController, "/curso/<int:curso_id>")
