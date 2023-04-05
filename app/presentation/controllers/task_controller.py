from fastapi import APIRouter, HTTPException, status

from app.persistence.task_mongodb_repository import TarefaMongoDBRepository
from app.persistence.task_repository import TarefaInMemoryRepository

from ..viewmodels import Tarefa

print('task controller ok')
router = APIRouter()
prefix = '/tasks'

tasks_repository = TarefaMongoDBRepository()

@router.get('/')
def todas_tarefas(skip: int | None = 0, take: int | None = 0):
    return tasks_repository.todos(skip, take)

@router.get('/situacao')
def listar_por_situacao(situacao_tarefa: str):
    tasks_filtradas = [tasks_repository.listar_situcao(situacao_tarefa)]
    return tasks_filtradas

@router.get('/np')
def filtrar_nivel_prioridade(nivel_tarefa: int, prioridade_tarefa: int):
    tasks_filtradas = [tasks_repository.filtrar_nivel_prioridade(nivel_tarefa, prioridade_tarefa)]
    return tasks_filtradas

@router.get('/{tarefa_id}')
def obter_tarefa(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não há tarefa com id = {tarefa_id}')
    
    return tarefa

@router.post('/', status_code=status.HTTP_201_CREATED)
def nova_tarefa(tarefa: Tarefa):
    if tarefa.nivel in [1, 3, 5, 8]:
        if tarefa.situacao in ["nova"]:
            if tarefa.prioridade in [1, 2, 3]:
                
                return tasks_repository.salvar(tarefa)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Parâmetros inválidos!')

@router.delete('/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_tarefa(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa não encontrada')
    
    tasks_repository.remover(tarefa_id)

@router.put('/{tarefa_id}/iniciar')
def em_andamento(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa não encontrada!')
    
    tasks_repository.em_andamento(tarefa_id)

@router.put('/{tarefa_id}/pendente')
def pendente(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa não encontrada!')
    
    tasks_repository.pendente(tarefa_id)

@router.put('/{tarefa_id}/cancelar')
def cancelada(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f'Tarefa não encontrada!')
    
    tasks_repository.cancelada(tarefa_id)

@router.put('/{tarefa_id}/resolver')
def resolvida(tarefa_id: int | str):
    tarefa = tasks_repository.obter_um(tarefa_id)

    if not tarefa:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f'Tarefa não encontrada!')
    
    tasks_repository.resolvida(tarefa_id)