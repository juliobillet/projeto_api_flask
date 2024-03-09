from ..models import professor_model
from api import db


def cadastrar_professor(professor):
    professor_bd = professor_model.ProfessorModel(
        nome=professor.nome,
        disciplina=professor.disciplina,
        admissao=professor.admissao
    )
    db.session.add(professor_bd)
    db.session.commit()
    return professor_bd


def listar_professores():
    professores = professor_model.ProfessorModel.query.all()
    return professores


def listar_professor_por_id(parm_id):
    professor = professor_model.ProfessorModel.query.filter_by(id=parm_id).first()
    return professor


def atualizar_professor(professor_bd, professor_atualizado):
    professor_bd.nome = professor_atualizado.nome
    professor_bd.disciplina = professor_atualizado.disciplina
    professor_bd.admissao = professor_atualizado.admissao
    db.session.commit()


def excluir_professor(professor_bd):
    db.session.delete(professor_bd)
    db.session.commit()
