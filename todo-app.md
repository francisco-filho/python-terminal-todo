# CRUD na prática com Python + Sqlite

Neste tutorial mostraremos como criar uma aplicação CRUD (create, read, update and delete) com python e sqlite. Criaremos um TODO APP (app de tarefas) em que poderemos adicionar, remover e alterar as tarefas, e para manter o desenvolvimento simples a interface para a aplicação será o próprio terminal de linha de comando.

Você aprenderá a:

- conectar ao banco de dados sqlite
- inserir, alterar e remover registros no banco de dados
- utilizar o método `input`para que o usuário possa interagir com o app no terminal

## Sqlite

Escolhemos o sqlite por que o python já tem suporte nativo ao mesmo e não é necessário instalar uma biblioteca sequer para começar a utiliza-lo, e de bônus todo o conhecimento que você obter vai poder ser utilizado com qualquer outro banco que tenha drivers para python desde que eles implementem a api ????????? de banco de dados para python. O sqlite tambem possui as principais funcionalidades que os **grandes** bancos de dados tem só não é o mais indicado para aplicações que recebam diversas conexões simultaneas como aplicações web, mas para nosso pequeno app ele é mais que perfeito.

> o sqlite é o banco utilizado nos celulares android e iPhone

Vamos criar um módulo python que conterá a funcionalidade de acesso ao banco de dados, nomei o arquivo `db.py` e digite o seguinte conteudo:

```python
import sqlite3

# conecta ao banco de dados 'todo-app'
# caso o banco não exista ele será criado
conn = sqlite3.connect("todo-app.db")

"""
    sqlite3
        - connect(arquivo)
        - execute()
        - cursor()
        - commit()
        - sql básico (select, insert, delete)
"""

def criar_tabela_todo(conn):
    """ cria a tabela 'tarefa' caso ela não exista """
    cursor = conn.cursor()
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