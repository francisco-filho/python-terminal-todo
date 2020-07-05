import sqlite3

# conecta ao banco de dados 'todo-app'
# caso o banco não exista ele será criado
conn = sqlite3.connect("todo-app.db")

def criar_tabela_todo(conn):
    """  """
    cursor = conn.cursor()
    conn.execute("""
    create table if not exists tarefa (
        cd_tarefa integer primary key autoincrement,
        tarefa text,
        concluido integer
    )
    """)

def add_tarefa(tarefa):
    cursor = conn.cursor()
    conn.execute("insert into tarefa (tarefa, concluido) values (?, 0)", (tarefa, ))
    conn.commit()

def remover_tarefa(cd_tarefa):
    cursor = conn.cursor()
    conn.execute("delete from tarefa where cd_tarefa = ?", (cd_tarefa, ))

def concluir_tarefa(cd_tarefa):
    cursor = conn.cursor()
    conn.execute("update tarefa set concluido = 1 where cd_tarefa = ?", (cd_tarefa, ))
    conn.commit()

def get_tarefas():
    cursor = conn.cursor()
    return conn.execute("select cd_tarefa, tarefa, concluido from tarefa")

def listar_tarefas():
    print ("--- Tarefas")
    for tarefa in get_tarefas():
        t = f"- [{tarefa[0]}] {tarefa[1]}"
        if (tarefa[2] == 1):
            print (color_red(t))
        else:
            print (t)

def color_red(texto):
    return f"\033[92m{texto}\033[0m"

def menu_inicial():
    menu = """
--- O que você deseja fazer? digite a opção
1 -> Nova tarefa
2 -> Concluir tarefa
    """
    return menu

def menu_nova_tarefa():
    menu = """
--- Informe a descrição da tarefa ou 99 para voltar
    """
    return menu    

def menu_concluir_tarefa():
    menu = """
--- Informe o código da tarefa que deseja CONCLUIR ou 99 para voltar
    """
    return menu        

if __name__ == "__main__":
    criar_tabela_todo(conn)    
    while True:
        listar_tarefas()
        print (menu_inicial())
        escolha = input()
        try:
            escolha_int = int(escolha)
            print ("Você selecionou ", escolha)
            
            if escolha_int == 1:
                texto_nova_tarefa = ""
                while True:
                    print(menu_nova_tarefa())
                    texto_nova_tarefa = input()
                    print ("adicionando tarefa -> " + str(texto_nova_tarefa))
                    if texto_nova_tarefa == "99":
                        break
                    add_tarefa(texto_nova_tarefa)
            elif escolha_int == 2:
                cd_tarefa = ""
                while True:
                    print(menu_concluir_tarefa())
                    cd_tarefa = int(input())
                    print ("Concluindo tarefa tarefa -> " + str(cd_tarefa))
                    if cd_tarefa == 99:
                        break
                    concluir_tarefa(cd_tarefa)                    
        except Exception as e :
            print(e)
            exit(0)