from api import db


class ProfessorModel(db.Model):
    __tablename__ = "professor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    admissao = db.Column(db.Date, nullable=False)
