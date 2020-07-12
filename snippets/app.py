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