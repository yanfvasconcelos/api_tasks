const baseURL = 'https://api-tasks-pwdf.onrender.com/tasks/'

let tasks = []

function atualizar_tela() {
    const ul_tasks = document.getElementById('list-task')
    ul_tasks.innerHTML = []

    for (let tarefa of tasks) {
        const item = document.createElement('li')
        item.setAttribute('id', `${tarefa.id}`)
        const label = `${tarefa.id} - ${tarefa.descricao} - ${tarefa.responsavel} - ${tarefa.nivel} - ${tarefa.situacao} - ${tarefa.prioridade} `


        //BOTÃO INICIAR TAREFA
        const btn_iniciar = document.createElement('a')
        btn_iniciar.innerText = 'Iniciar'
        btn_iniciar.href = '#'
        btn_iniciar.onclick = async (event) => {

            event.preventDefault()
            const confirmou = confirm(`Deseja mesmo iniciar a tarefa: ${tarefa.id}`)

            if (!confirmou) {
                return
            }

            const response = await fetch(baseURL + tarefa.id + '/iniciar', { method: 'PUT' })

            if (response.ok) {
                alert('Tarefa iniciada com sucesso!')
                carregar_tarefas()
            }
        }

        //BOTÃO PARAR TAREFA(PENDENTE)
        const btn_parar = document.createElement('a')
        btn_parar.innerText = 'Parar'
        btn_parar.href = '#'
        btn_parar.onclick = async (event) => {

            event.preventDefault()
            const confirmou = confirm(`Deseja mesmo parar a tarefa: ${tarefa.id}`)

            if (!confirmou) {
                return
            }

            const response = await fetch(baseURL + tarefa.id + '/pendente', { method: 'PUT' })

            if (response.ok) {
                alert('Tarefa parada com sucesso!')
                carregar_tarefas()
            }
        }

        //BOTÃO CANCELAR TAREFA
        const btn_cancelar = document.createElement('a')
        btn_cancelar.innerText = 'Cancelar'
        btn_cancelar.href = '#'
        btn_cancelar.onclick = async (event) => {

            event.preventDefault()
            const confirmou = confirm(`Deseja mesmo cancelar a tarefa: ${tarefa.id}`)

            if (!confirmou) {
                return
            }

            const response = await fetch(baseURL + tarefa.id + '/cancelar', { method: 'PUT' })

            if (response.ok) {
                alert('Tarefa cancelada com sucesso!')
                carregar_tarefas()
            }
        }

        //BOTÃO FINALIZAR TAREFA
        const btn_finalizar = document.createElement('a')
        btn_finalizar.innerText = 'Finalizar'
        btn_finalizar.href = '#'
        btn_finalizar.onclick = async (event) => {

            event.preventDefault()
            const confirmou = confirm(`Deseja mesmo finalizar a tarefa: ${tarefa.id}`)

            if (!confirmou) {
                return
            }

            const response = await fetch(baseURL + tarefa.id + '/resolver', { method: 'PUT' })

            if (response.ok) {
                alert('Tarefa finalizada com sucesso!')
                carregar_tarefas()
            }
        }

        //BOTÃO REMOVER
        const btn_remover = document.createElement('a')
        btn_remover.innerText = 'Remover'
        btn_remover.href = '#'
        btn_remover.onclick = async (event) => {

            event.preventDefault()
            const confirmou = confirm(`Deseja mesmo remover a tarefa: ${tarefa.id}`)

            if (!confirmou) {
                return
            }

            const response = await fetch(baseURL + tarefa.id, { method: 'DELETE' })

            if (response.ok) {
                alert('Tarefa removida com sucesso!')
                carregar_tarefas()
            }
        }

        item.innerText = label
        if (tarefa.situacao == 'nova'){
            item.appendChild(btn_iniciar)
            item.append(' ')
            item.appendChild(btn_cancelar)
            item.append(' ')
            item.appendChild(btn_parar)
            item.append(' ')
            item.appendChild(btn_remover)
        }
        if (tarefa.situacao == 'em andamento'){
            item.appendChild(btn_parar)
            item.append(' ')
            item.appendChild(btn_cancelar)
            item.append(' ')
            item.appendChild(btn_finalizar)
            item.append(' ')
            item.appendChild(btn_remover)
        }
        if (tarefa.situacao == 'pendente'){
            item.appendChild(btn_iniciar)
            item.append(' ')
            item.appendChild(btn_cancelar)
            item.append(' ')
            item.appendChild(btn_remover)
        }
        if (tarefa.situacao == 'cancelada'){
            item.appendChild(btn_iniciar)
            item.append(' ')
            item.appendChild(btn_remover)
        }
        if (tarefa.situacao == 'resolvida'){
            item.appendChild(btn_remover)
        }

        ul_tasks.appendChild(item)

    }
}

async function carregar_tarefas() {
    console.log('API - Todas as Tarefas')
    const response = await fetch(baseURL)

    const status = response.status
    tasks = await response.json()

    atualizar_tela()
}

function configurar_formulario() {
    const form_task = document.getElementById('form-task')

    form_task.onsubmit = async function (event) {

        event.preventDefault()

        const descricao = document.getElementById('descricao').value
        const responsavel = document.getElementById('responsavel').value
        const nivel = Number(document.getElementById('nivel').value)
        const situacao = document.getElementById('situacao').value
        const prioridade = Number(document.getElementById('prioridade').value)

        const tarefa = { descricao, responsavel, nivel, situacao, prioridade }

        console.log('Submeteu!')

        const response = await fetch(baseURL, { method: 'POST', body: JSON.stringify(tarefa), headers: { 'Content-Type': 'application/json' } })

        if (response.status === 201) {
            alert('Tarefa Adicionado com sucesso!')
            carregar_tarefas()
            form_task.reset()
        } else {
            alert('Não foi possível adicionar')
        }
    }
}

function app() {
    console.log('Hello Tasks')
    configurar_formulario()
    carregar_tarefas()
}
var elementos = document.getElementsByTagName('div')
console.log(elementos)
app()