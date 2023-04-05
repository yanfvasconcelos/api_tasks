class TarefaInMemoryRepository():

    def __init__(self):
        self.tasks = []
        self.proximo_id = 1

    def todos(self, skip, take):
        inicio = skip

        if skip and take:
            fim = skip + take
        else:
            fim = None

        return self.filmes[inicio:fim]
    
    def listar_situacao(self, situacao_tarefa):
        tasks_filtradas = []
        for tarefa in self.tasks:
            if tarefa.situacao == situacao_tarefa:
                tasks_filtradas.append(tarefa)
        return tasks_filtradas
    
    def filtrar_nivel_prioridade(self, nivel_tarefa, prioridade_tarefa):
        tasks_filtradas = []
        for tarefa in self.tasks:
            if tarefa.nivel == nivel_tarefa and tarefa.prioridade == prioridade_tarefa:
                tasks_filtradas.append(tarefa)
        return tasks_filtradas
    
    def obter_um(self, tarefa_id):
        for tarefa in self.tasks:
            if tarefa.id == tarefa_id:
                return tarefa
        
        return None
    
    def salvar(self, tarefa):
        if tarefa.nivel in [1, 3, 5, 8]:
            if tarefa.situacao in ["nova"]:
                if tarefa.prioridade in [1, 2, 3]:
                    tarefa.id = self.proximo_id
                    self.proximo_id += 1
                    self.tasks.append(tarefa)

                    return tarefa
    
    def remover(self, tarefa_id):
        tarefa = self.obter_um(tarefa_id)
        if tarefa:
            self.tasks.remove(tarefa)

    def atualizar_situacao(self, tarefa_id):
        for index in range(len(self.tasks)):
            tarefa_atual = self.tasks[index]
            if tarefa_atual.id == tarefa_id:
                return tarefa_atual
            
    def em_andamento(self, tarefa_id):
        tarefa_atual = self.atualizar_situacao(tarefa_id)
        if tarefa_atual.situacao in ['nova', 'pendente']:
            tarefa_atual.situacao = 'em andamento'
            return
    
    def pendente(self, tarefa_id):
        tarefa_atual = self.atualizar_situacao(tarefa_id)
        if tarefa_atual.situacao in ['nova', 'em andamento']:
            tarefa_atual.situacao = 'pendente'
            return
    
    def cancelada(self, tarefa_id):
        tarefa_atual = self.atualizar_situacao(tarefa_id)
        if tarefa_atual.situacao in ['nova', 'em andamento', 'pendente']:
            tarefa_atual.situacao = 'cancelada'
            return
        
    def resolvida(self, tarefa_id):
        tarefa_atual = self.atualizar_situacao(tarefa_id)
        if tarefa_atual.situacao in ['em andamento']:
            tarefa_atual.situacao = 'resolvida'
            return
