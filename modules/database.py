import os
import json
from datetime import datetime
from modules.utilities import hoje,calc_montante

def create_database() -> None:
    """
    Creates a basic JSON database file named "database.json" if it doesn't already exist.

    Parameters:
        None

    Returns:
        None

    Usage:
        The function creates a simple JSON file that can be used as a database to store data. If the "database.json" file
        already exists, the function takes no action.

    Example:
        ```python
        # Create the "database.json" file if it doesn't exist
        create_database()
        ```

    Note:
        The created JSON file has default keys such as "data," "type," "value," and "amount" with initial values set to None.
        You can customize or add more keys as needed for your application.
    """
    # Checks if the "database.json" file already exists
    database_path = "database.json"
    if os.path.exists(database_path):
        return None

    # Creates a JSON dictionary with keys "data", "type", "value", and "amount", all with initial values of None
    json_base = {
        "data_de_criacao": [],
        "ultima_atualizacao": [],
        "tipo": [],
        "valor": [],
        "taxa":[],
        "montante": []
    }

    # Opens the "database.json" file in write mode
    with open(database_path, "w") as file:
        # Writes the JSON dictionary to the JSON file with an indentation of 4 spaces for better readability
        json.dump(json_base, file, indent=4)

    return None

def atualiza_rendimento() -> None:
    '''
    '''
    # Verificando se a base de dados existe
    if not os.path.exists('database.json'):
        raise Exception("Database not exist")
    
    # Lendo a base de dados
    database_path = 'database.json'
    with open(database_path,'r') as file:
        database = json.load(file)
    
    for i in range(0,len(database['data_de_criacao'])):
        if database['tipo'][i].lower() == "investimento":
            dia_da_transacao,dia_atual = datetime.strptime(database['data_de_criacao'][i],"%d/%m/%Y %H:%M:%S"),datetime.today()
            dias_passados = abs((dia_atual - dia_da_transacao).days)
            print(f"Passaram-se {dias_passados} dias")
            database['ultima_atualizacao'][i] = hoje()
            database['montante'][i] = round(calc_montante(capital=database['valor'][i],taxa=database['taxa'][i],tempo=dias_passados),2)

    with open(database_path,'w') as file:
            json.dump(database,file,indent=4)

def inserir_valor(valor:float,tipo:str,taxa:float=None) -> None:
    '''
    '''

    # Verificando se é investimento e se a taxa está preenchida
    if tipo.casefold() == "investimento".casefold() and taxa is None:
        raise ValueError("Taxa can't be None")
    
    # Verificando se a taxa passanda para o investimento é float
    if tipo.casefold() == "investimento".casefold() and not isinstance(taxa,float):
        raise ValueError("Taxa precisa ser float")
    
    database_path = 'database.json'
    with open(database_path,'r') as file:
        database = json.load(file)
    
    try:
        database['data_de_criacao'].append(hoje())
        database['ultima_atualizacao'].append(hoje())
        database['tipo'].append(tipo)
        database['valor'].append(valor)
        database['taxa'].append(taxa if tipo.casefold() == "investimento".casefold() else None)
        database['montante'].append(None)

        with open(database_path,'w') as file:
            json.dump(database,file,indent=4)
        
        print("Valor inserido com sucesso")
    except Exception as err:
        print(f"Erro ao inserir no banco de dados -> {err}")
