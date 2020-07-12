import db

MENU_INICIAL = 99

def exibir_cabecalho():
    """ imprimi o cabeçalho no terminal utilizando o tamanho maximo de 60 caracteres """
    QTD_COLUNAS = 60
    print ("-" * QTD_COLUNAS)
    print ("{:^60}".format("TAREFAS"))
    print ("-" * QTD_COLUNAS)
    print ("{:^60}".format("tecle 99 volta para o menu inicial, [CTRL+C] sai"))
    print ("-" * QTD_COLUNAS)

def exibir_tarefas():    
    """ exibe a lista de tarefas cadastradas, com algumas formatações básicas """
    for tarefa in db.get_tarefas():
        # check = \u2713 é o caracter unicode que representa o concluido
        check = u'\u2713' if tarefa[2] == 1 else ""
        """
            os parametros passados para esse format() são o seguinte
            {:>4}  = 4 posições, alinhado a direita
            {:<47} = 47 posições, alinhado a esquerda
            {:^3}  = 3 posições, centralizado
        """
        t = "- [{:>4}] {:<47} {:^3}".format(tarefa[0], tarefa[1], check)
        print (t)
    print ("-" * 60)

def mostrar_opcao_nova_tarefa():
    texto_nova_tarefa = input("Descreva a Tarefa => ")
    print ("adicionando tarefa -> " + str(texto_nova_tarefa))
    if texto_nova_tarefa != str(MENU_INICIAL):
        db.add_tarefa(texto_nova_tarefa)    

def mostrar_opcao_concluir_tarefa():
    cd_tarefa = int(input("Qual tarefa quer concluir? digite o código => "))
    print ("Concluindo tarefa tarefa -> " + str(cd_tarefa))
    if cd_tarefa != MENU_INICIAL:
        db.concluir_tarefa(cd_tarefa)