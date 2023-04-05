from bson.objectid import ObjectId
from pydantic import BaseModel

class Tarefa(BaseModel):
    id: int | None | str
    descricao: str
    responsavel: str
    nivel: int
    situacao: str
    prioridade: int

    class Config:
        orm_mode = True

    #CLS referencia a classe como um todo
    #cria uma nova instância da classe
    @classmethod
    def fromDict(cls, tarefa):
        tarefa_ = Tarefa(id=str(tarefa['_id']),
                         descricao=tarefa['descricao'],
                         responsavel=tarefa['responsavel'],
                         nivel=tarefa['nivel'],
                         situacao=tarefa['situacao'],
                         prioridade=tarefa['prioridade'])
        return tarefa_
    
    #retorna um dicionário
    def toDict(self):
        return {
            "descricao": self.descricao,
            "responsavel": self.responsavel,
            "nivel": self.nivel,
            "situacao": self.situacao,
            "prioridade": self.prioridade
        }

class User(BaseModel):
    id: int | None
    nome: str
    email: str
    senha: str