from modules.ui import JanelaPrincipal
from modules.database import atualiza_rendimento, create_database,insert_values
'''
def main():
    main_frame = JanelaPrincipal() # Instanciando a janela principal

    main_frame.inicializar()

    main_frame.rodar()
'''
def main():
    create_database()
    insert_values(14,"Investimento",taxa=1.0)
    #atualiza_rendimento()

if __name__ == "__main__":
    main()