from dataclasses import dataclass
from datetime import date


@dataclass
class ProfessorDTO:
    nome: str
    disciplina: str
    admissao: date
