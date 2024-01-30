from logging import error,info
from typing import Literal
from datetime import datetime

def menu() -> Literal[1,2,3,4]:
    '''
    '''
    while True:

        print("\t#### MENU ####")
        print("\tSelecione uma opção:")
        print("\t1. Inserir registro")
        print("\t2. Ler registro")
        print("\t3. Deletar registro")
        print("\t4. Atualizar")
        print("\t5. Exportar relatório")
        print("\t6. Sair")
        escolha = input("Digite o número da opção desejada: ")

        match(escolha):
            case "1":
                return 1
            case "2":
                return 2
            case "3":
                return 3
            case "4":
                return 4
            case "5":
                return 5
            case "6":
                info("Fim de execução")
                exit(0)
            case _:
                error("O valor inserido não é uma opção válida")

def menu_inserir() -> dict:
    '''
    Exibe um menu para inserção de dados e retorna um dicionário com as informações inseridas.
    '''
    dicionario = {}
    print("\t#### INSERIR ####")

    while True:
        try:
            dicionario['valor'] = float(input("Insira o valor da transação: "))
            break
        except ValueError:
            print("Por favor, insira um valor válido.")

    tipos_permitidos = ['Receita', 'Despesas', 'Investimento']
    while True:
        tipo = input(f"Insira o tipo da transação ({tipos_permitidos}): ")
        if tipo in tipos_permitidos:
            dicionario['tipo'] = tipo
            break
        else:
            print("Tipo de transação inválido. Tente novamente.")

    if dicionario['tipo'] == "Investimento":
        while True:
            try:
                dicionario['taxa'] = float(input("Insira o valor da taxa em %: "))/100
                break
            except ValueError:
                print("Por favor, insira um valor válido para a taxa.")

    return dicionario

def menu_ler() -> dict:
    '''
    Exibe um menu para leitura de dados e retorna um dicionário com as informações inseridas.
    '''
    dicionario = {}
    print("\t#### LER ####")

    # Leitura de data
    data_inicial_str = input("Insira a data inicial (formato: dd/mm/yyyy, pressione Enter para vazio): ")
    data_final_str = input("Insira a data final (formato: dd/mm/yyyy, pressione Enter para vazio): ")
    # Ajusta as datas para valores extremos se estiverem vazias
    data_inicial = data_inicial_str if data_inicial_str else "01/01/1000"
    data_final = data_final_str if data_final_str else "31/12/9999"

    dicionario['data'] = (data_inicial, data_final)

    # Leitura de tipo
    tipos_permitidos = ['Receita', 'Despesas', 'Investimento']
    tipo = input(f"Insira o tipo da transação ({tipos_permitidos}, pressione Enter para vazio): ")
    dicionario['tipo'] = tipo if tipo in tipos_permitidos else None

    # Leitura de valor
    valor_inicial_str = input("Insira o valor inicial da transação (pressione Enter para vazio): ")
    valor_final_str = input("Insira o valor final da transação (pressione Enter para vazio): ")

    valor_inicial = float(valor_inicial_str) if valor_inicial_str else float('-inf')
    valor_final = float(valor_final_str) if valor_final_str else float('inf')

    dicionario['valor'] = (valor_inicial, valor_final)

    return dicionario

def menu_deletar() -> None:
    '''
    '''
    print("\t#### DELETAR ####")
    return int(input("Insira o id que deseja deletar: "))

from typing import Optional, Literal

def menu_atualizar() -> dict:
    '''
    Exibe um menu para atualização de dados e retorna um dicionário com as informações inseridas.
    '''
    dicionario = {}
    print("\t#### ATUALIZAR ####")

    # Leitura do ID
    id_transacao_str = input("Insira o ID da transação que deseja atualizar: ")
    dicionario['id'] = int(id_transacao_str) if id_transacao_str.isdigit() else None

    # Se não for fornecido um ID válido, retorna o dicionário com o ID sendo None
    if dicionario['id'] is None:
        return dicionario

    # Leitura de valor
    valor_str = input("Insira o novo valor da transação (pressione Enter para manter o valor atual): ")
    dicionario['valor'] = float(valor_str) if valor_str else None

    # Leitura de tipo
    tipos_permitidos = ['Receita', 'Despesas', 'Investimento']
    tipo = input(f"Insira o novo tipo da transação ({tipos_permitidos}, pressione Enter para manter o tipo atual): ")
    dicionario['tipo'] = tipo if tipo in tipos_permitidos else None
    # Leitura de taxa
    taxa_str = input("Insira a nova taxa (pressione Enter para manter a taxa atual): ")
    dicionario['taxa'] = float(taxa_str) if taxa_str else None

    return dicionario