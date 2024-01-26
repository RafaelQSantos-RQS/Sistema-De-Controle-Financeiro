from modules.ui import JanelaPrincipal
from modules.database import Localbase
from logging import INFO, basicConfig

basicConfig(level=INFO, format=f'[%(asctime)s]: %(message)s',datefmt='%d/%m/%Y %H:%M:%S')
'''
def main():
    main_frame = JanelaPrincipal() # Instanciando a janela principal

    main_frame.inicializar()

    main_frame.rodar()
'''
def main():
    database = Localbase(database_file='database.csv')
    database.atualiza_rendimento()
    #database.inserir_registro(14,'Despesas',taxa=0.14)
    #database.inserir_registro(150,'Despesas')
    #database.deletar_registro(14)
    #database.ler_registros(data=("25/01/2024","26/01/2024"),tipo='Despesas',print_table=True)
    database.exportar_relatorio(formato='json',data=("25/01/2024","25/01/2024"))

if __name__ == "__main__":
    print(type(True))
    main()