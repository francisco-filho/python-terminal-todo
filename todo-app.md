# CRUD na prática com Python + Sqlite

Neste tutorial mostraremos como criar uma aplicação CRUD (create, read, update and delete) com python e sqlite. Criaremos um TODO APP (app de tarefas) em que poderemos adicionar, remover e alterar as tarefas, e para manter o desenvolvimento simples a interface para a aplicação será o próprio terminal de linha de comando.

Nós abordaremos os seguintes tópicos:

- conexão  ao banco de dados sqlite
- inserir, alterar e remover registros no banco de dados
- solicitanção de input do usuário no terminal

> Para seguir este tutorial você deve conhecer o básico de python como funções, estruturas de controle e repetição 

## Sqlite

Escolhemos o sqlite por que o python já tem suporte nativo ao mesmo e não é necessário instalar uma biblioteca sequer para começar a utiliza-lo, e de bônus todo o conhecimento que você obter vai poder ser utilizado com qualquer outro banco que tenha drivers para python desde que eles implementem a api ????????? de banco de dados para python. O sqlite tambem possui as principais funcionalidades que os **grandes** bancos de dados tem só não é o mais indicado para aplicações que recebam diversas conexões simultaneas como aplicações web, mas para nosso pequeno app ele é mais que perfeito.

> o sqlite é o banco utilizado nos celulares android e iPhone

## Implementação

Os principais métodos do sqlite utilizados são `connect()`, `execute()` e `commit()`

 `connect(path_arquivo)` retorna uma conexão com o banco de dados sqlite, que no nosso caso é o arquivo "todo-app.db" que está no diretório da aplicação.

 `conn.execute(sql, tupla)` executa comandos sql utilizando a conexão ao banco. O primeiro argumento é o código sql e o segundo parametro (opcional) é uma tupla com as variáveis que serão usadas na consulta. Esse comando retornar um objeto `cursor` o qual podemos interar e ler os resultados da consulta.

 `conn.commit()` comita as alterações realizadas no banco de dados

 Nossa classe `db` ainda tem o método `criar_tabela_todo()` que cria a tabela no nosso banco de dados caso ela ainda não exista.

Vamos criar um módulo python que conterá a funcionalidade de acesso ao banco de dados, nomei o arquivo `db.py` e digite o seguinte conteudo:

```python
# a biblioteca sqlite3 já está disponível no python3, não é necessário instalar nada mais
import sqlite3

# conecta ao banco de dados 'todo-app'
# caso o banco não exista ele será criado
conn = sqlite3.connect("todo-app.db")

def criar_tabela_todo(conn):
    """ cria a tabela 'tarefa' caso ela não exista """
    conn.execute("""
    create table if not exists tarefa (
        cd_tarefa integer primary key autoincrement,
        tarefa text,
        concluido integer
    )
    """)

def add_tarefa(tarefa):
    """ adiciona uma nova tarefa """
    conn.execute("insert into tarefa (tarefa, concluido) values (?, 0)", (tarefa, ))
    conn.commit()

def remover_tarefa(cd_tarefa):
    """ remove a tarefa da tabela """
    conn.execute("delete from tarefa where cd_tarefa = ?", (cd_tarefa, ))
    conn.commit()

def concluir_tarefa(cd_tarefa):
    """ marca a tarefa como concluida """
    conn.execute("update tarefa set concluido = 1 where cd_tarefa = ?", (cd_tarefa, ))
    conn.commit()

def get_tarefas(): # retorna um cursor
    """ retorna a lista de tarefas cadastras """
    return conn.execute("select cd_tarefa, tarefa, concluido from tarefa")

```

Agora é hora de criarmos a aplicação de tarefas. A primeira vista esta este código parece complexo, mas o que ela mais faz é imprimir as informações na tela. Utilizamos dois me´todos para isso:

 `exibir_cabecalho()` exibe o nome do app com informações básicas
 `exibir_tarefas()` exibe a lista de tarefas cadastradas no sistema

 Logo depois temos os métodos utilizados para interação com o usuário:

 `mostrar_opcao_nova_tarefa()` O sistema mostra a opção perguntndo ao usuário o que ele deseja fazer, as duas opções disponíveis são **incluir uma nova tarefa** ou **concluir uma tarefa**. Caso o usuário selecione **incluir** a perguntará a descrição da tarefa que ele quer cadastrar. Mas se ele selecionar a opção de conclusão, o método explicado abaixo será chamado.
 `mostrar_opcao_concluir_tarefa()` Nessa opção o sistema pergunta ao usuário o código da tarefa que ele deseja concluir, quando o usuário informa, o sistema marca a atividade como concluida e o ciclo começa novamente.

Segue abaixo o arquivo `mensagens.py`

 ```python
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

## continua        
```

E finalmente chegamos ao método `main()` que controla o fluxo do programa. Nele criamos um loop infinito onde:

- exibimos o cabeçalho e tarefas
- solicitamos a interação do usuário
- e depois repetimos tudo de novo

```python
import db
import mensagens as msg

def main():
    NOVA_TAREFA     = 1
    CONCLUIR_TAREFA = 2
    
    while True:
        msg.exibir_cabecalho()
        msg.exibir_tarefas()
        try:
            # exibe as opções disponíveis
            opcao = int(input("O que deseja fazer? 1 = Nova tarefa, 2 = Concluir tarefa => "))

            # verifica qual opção o usuário escolheu
            if opcao == NOVA_TAREFA:
                msg.mostrar_opcao_nova_tarefa()
            elif opcao == CONCLUIR_TAREFA:
                msg.mostrar_opcao_concluir_tarefa()
            else:
                print ("Opção não reconhecida, por favor informar um número")    
        except ValueError as e :
            print ("Opção não reconhecida, por favor informar um número")
        except Exception:
            exit(0)

if __name__ == "__main__":
    db.criar_tabela_todo()

    main()
 ```

## Referências

[Documentação sqlite](https://www.sqlite.org/docs.html)