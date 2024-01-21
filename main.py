from modules.ui import JanelaPrincipal
from modules.database import atualiza_rendimento, create_database,inserir_valor,deletar_registro
from logging import INFO, basicConfig

basicConfig(level=INFO, format=f'[%(asctime)s]: %(message)s',datefmt='%d/%m/%Y %H:%M:%S')
'''
def main():
    main_frame = JanelaPrincipal() # Instanciando a janela principal

    main_frame.inicializar()

    main_frame.rodar()
'''
def main():
    create_database()
    atualiza_rendimento()
    inserir_valor(valor=13,tipo='Investimento',taxa=0.014)
    #deletar_registro(id=3)

if __name__ == "__main__":
    main()