import sqlite3

# conecta ao banco de dados 'todo-app'
# caso o banco não exista ele será criado
conn = sqlite3.connect("todo-app.db")

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
    cursor = conn.cursor()
    conn.execute("insert into tarefa (tarefa, concluido) values (?, 0)", (tarefa, ))
    conn.commit()

def remover_tarefa(cd_tarefa):
    """ remove a tarefa da tabela """
    cursor = conn.cursor()
    conn.execute("delete from tarefa where cd_tarefa = ?", (cd_tarefa, ))
    conn.commit()

def concluir_tarefa(cd_tarefa):
    """ marca a tarefa como concluida """
    cursor = conn.cursor()
    conn.execute("update tarefa set concluido = 1 where cd_tarefa = ?", (cd_tarefa, ))
    conn.commit()

def get_tarefas():
    """ retorna a lista de tarefas cadastras """
    cursor = conn.cursor()
    return conn.execute("select cd_tarefa, tarefa, concluido from tarefa")

def exibir_tarefas():
    print ("--- Tarefas")
    for tarefa in get_tarefas():
        t = f"- [{tarefa[0]}] {tarefa[1]}"
        if (tarefa[2] == 1):
            print (colorir(t))
        else:
            print (t)

def colorir(texto):
    """ 
    Muda cor do terminal para verde
    esses códigos de cores são para terminais linux
    provavelmente não funcionará em Windows
    """
    return f"\033[92m{texto}\033[0m"

def menu_inicial():
    menu = """
--- O que você deseja fazer? digite a opção
1 -> Nova tarefa
2 -> Concluir tarefa
    """
    print (menu)

def menu_nova_tarefa():
    menu = """
--- Informe a descrição da tarefa ou 99 para voltar
    """
    print (menu)

def menu_concluir_tarefa():
    menu = """
--- Informe o código da tarefa que deseja CONCLUIR ou 99 para voltar
    """
    print (menu)    

if __name__ == "__main__":
    criar_tabela_todo(conn)    
    while True:
        exibir_tarefas()
        escolha = input("O que deseja fazer? 1 = Nova tarefa, 2 = Concluir tarefa => ")
        try:
            escolha_int = int(escolha)
           
            if escolha_int == 1:
                texto_nova_tarefa = input("Descreva a Tarefa => ")
                print ("adicionando tarefa -> " + str(texto_nova_tarefa))
                if texto_nova_tarefa != "99":
                    add_tarefa(texto_nova_tarefa)
            elif escolha_int == 2:
                cd_tarefa = int(input("Qual tarefa quer concluir? digite o código => "))
                print ("Concluindo tarefa tarefa -> " + str(cd_tarefa))
                if cd_tarefa != 99:
                    concluir_tarefa(cd_tarefa)
        except ValueError as e :
            print ("Opção não reconhecida, por favor informa um número")
        except Exception:
            exit(0)