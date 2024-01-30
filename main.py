from modules.ui_cli import menu,menu_inserir,menu_ler,menu_deletar,menu_atualizar
from logging import INFO, basicConfig
from modules.database import Localbase
basicConfig(level=INFO, format=f'[%(asctime)s]: %(message)s',datefmt='%d/%m/%Y %H:%M:%S')

def main():
    database = Localbase(database_file='database.csv')
    database.atualiza_rendimento()
    while True:
        match(menu()):
            case 1:
                entrada = menu_inserir()
                database.inserir_registro(valor=entrada.get('valor'),
                                          tipo=entrada.get('tipo'),
                                          taxa=entrada.get('taxa'))
                input("Aperte Enter para continuar...")
            case 2:
                entrada = menu_ler()
                database.ler_registros(data=entrada.get('data'),
                                       tipo=entrada.get('tipo'),
                                       valor=entrada.get('valor'),
                                       print_table=True)
                input("Aperte Enter para continuar...")
            case 3:
                database.ler_registros(print_table=True)
                entrada = menu_deletar()
                database.deletar_registro(id=entrada)
                input("Aperte Enter para continuar...")
            case 4:
                database.ler_registros(print_table=True)
                entrada = menu_atualizar()
                database.alterar_registro(id=entrada.get('id'),
                                          valor=entrada.get('entrada'),
                                          tipo=entrada.get('tipo'),
                                          taxa=entrada.get('taxa'))
                input("Aperte Enter para continuar...")

if __name__ == "__main__":
    main()