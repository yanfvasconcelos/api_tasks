from typing import TypedDict

from bson.objectid import ObjectId
from decouple import Config
from pymongo import MongoClient

from ..presentation.viewmodels import Tarefa

class TarefaMongo(TypedDict):
    _id: ObjectId
    descricao: str
    responsavel: str
    nivel: int
    situacao: str
    prioridade: str

class TarefaMongoDBRepository():

    def __init__(self):
        #connect to MongoDB
        uri = Config('MONGODB_URL')
        client = MongoClient(uri)
        db = client['mtasks']
        self.tasks = db['tasks']
        try:
            print('MongoDB OK!')
        except:
            print('Deu erro!')
    
    def todos(self, skip=0, take=0):
        tarefas = self.tasks.find().skip(skip).limit(take)
        return list(map(Tarefa.fromDict, tarefas))
    
    def listar_situcao(self, situacao_tarefa):
        tarefas = self.tasks.find({"situacao": situacao_tarefa})
        return tarefas
    
    def filtrar_nivel_prioridade(self, nivel_tarefa, prioridade_tarefa):
        tarefas = self.tasks.find({"$and": [{"nivel": nivel_tarefa}, {"prioridade": prioridade_tarefa}]})
        return tarefas
    
    def salvar(self, tarefa):
        _id = self.tasks.insert_one(tarefa.toDict()).inserted_id
        tarefa.id = str(_id)
        return tarefa
    
    def obter_um(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        tarefa_encontrada = self.tasks.find_one(filtro)
        return Tarefa.fromDict(tarefa_encontrada) if tarefa_encontrada else None
    
    def remover(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tasks.delete_one(filtro)

    def em_andamento(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tasks.update_one(filtro, {'$set': {"situacao": "em andamento"}})
    
    def pendente(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tasks.update_one(filtro, {'$set': {"situacao": "pendente"}})

    def cancelada(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tasks.update_one(filtro, {'$set': {"situacao": "cancelada"}})
    
    def resolvida(self, tarefa_id):
        filtro = {"_id": ObjectId(tarefa_id)}
        self.tasks.update_one(filtro, {'$set': {"situacao": "resolvida"}})
        return