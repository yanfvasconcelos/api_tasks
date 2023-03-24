from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


class Tarefa(BaseModel):
    id: int | None
    descricao: str
    responsavel: str
    nivel: int
    situacao: str
    prioridade: int


tasks: list[Tarefa] = []

# List Tasks
@app.get('/tasks')
def listar_tarefas(skip: int | None = None, take: int | None = None):
    inicio = skip
    if skip and take:
        fim = skip + take
    else:
        fim = None
    return tasks[inicio:fim]

# List a task by status
@app.get('/tasks/situacao')
def listar_por_situacao(situacao_tarefa: str):
    if situacao_tarefa not in ["nova", "em andamento", "pendente", "resolvida", "cancelada"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Impossível concluir ação!')

    tasks_filtradas = []

    for tarefa in tasks:
        if tarefa.situacao == situacao_tarefa:
            tasks_filtradas.append(tarefa)
    return tasks_filtradas


@app.get('/tasks/np')
def filtrar_nivel_prioridade(nivel_tarefa: int, prioridade_tarefa: int):
    if nivel_tarefa not in [1, 3, 5, 8] or prioridade_tarefa not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Impossível concluir ação!')

    tasks_np = []

    for tarefa in tasks:
        if tarefa.nivel == nivel_tarefa and tarefa.prioridade == prioridade_tarefa:
            tasks_np.append(tarefa)
    return tasks_np

# get a task by id
@app.get('/tasks/{tarefa_id}')
def obter_tarefa(tarefa_id: int):
    for tarefa in tasks:
        if tarefa.id == tarefa_id:
            return tarefa

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa não encontrada: {tarefa_id}')

# Add Task
@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def nova_tarefa(tarefa: Tarefa):
    if tarefa.nivel in [1, 3, 5, 8]:
        if tarefa.situacao in ["nova"]:
            if tarefa.prioridade in [1, 2, 3]:
                tarefa.id = len(tasks) + 18
                tasks.append(tarefa)
                return tarefa

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Parâmetros inválidos.')

# Remove Task
@app.delete('/tasks/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(tarefa_id: int):
    for tarefa_atual in tasks:
        if tarefa_atual.id == tarefa_id:
            tasks.remove(tarefa_atual)
            return
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail="Tarefa não encontrada.")

# update status to "in progress"
@app.put('/tasks/{tarefa_id}/iniciar')
def em_andamento(tarefa_id: int):
    for index in range(len(tasks)):
        tarefa_atual = tasks[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "nova" or tarefa_atual.situacao == "pendente":
                tarefa_atual.situacao = "em andamento"
                return

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Impossível concluir ação!')

# update status to "outstanding"
@app.put('/tasks/{tarefa_id}/pender')
def pendente(tarefa_id: int):
    for index in range(len(tasks)):
        tarefa_atual = tasks[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "nova" or tarefa_atual.situacao == "em andamento":
                tarefa_atual.situacao = "pendente"
                return

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Impossível concluir ação!')

# update status to "canceled"
@app.put('/tasks/{tarefa_id}/cancelar')
def cancelada(tarefa_id: int):
    for index in range(len(tasks)):
        tarefa_atual = tasks[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao in ["nova", "em andamento", "pendente"]:
                tarefa_atual.situacao = "cancelada"
                return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Tarefa não encontrada!')

# update status to "resolved"
@app.put('/tasks/{tarefa_id}/resolver')
def resolvida(tarefa_id: int):
    for index in range(len(tasks)):
        tarefa_atual = tasks[index]
        if tarefa_atual.id == tarefa_id:
            if tarefa_atual.situacao == "em andamento":
                tarefa_atual.situacao = "resolvida"
                return

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Impossível concluir ação!')
