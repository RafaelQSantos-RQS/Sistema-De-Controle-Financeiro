from modules.ui import JanelaPrincipal
from modules.utilities import create_database,insert_values
'''
def main():
    main_frame = JanelaPrincipal() # Instanciando a janela principal

    main_frame.inicializar()

    main_frame.rodar()
'''
def main():
    create_database()
    insert_values(14,"Receita")

if __name__ == "__main__":
    main()