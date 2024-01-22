from modules.ui import JanelaPrincipal
from modules.database import atualiza_rendimento, create_database,inserir_registro,deletar_registro,alterar_registro
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
    inserir_registro(valor=18,tipo='Receita',taxa=0.014)
    alterar_registro(id=0,tipo="Investimento")

if __name__ == "__main__":
    main()