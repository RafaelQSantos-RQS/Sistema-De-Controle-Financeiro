from modules.ui import JanelaPrincipal
from modules.database import atualiza_rendimento, create_database,inserir_valor
'''
def main():
    main_frame = JanelaPrincipal() # Instanciando a janela principal

    main_frame.inicializar()

    main_frame.rodar()
'''
def main():
    create_database()
    inserir_valor(14,"Investimento",.15)
    atualiza_rendimento()

if __name__ == "__main__":
    main()