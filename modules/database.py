import os
import json
from datetime import datetime
from typing import NoReturn,Literal,Optional,Tuple
from modules.utilities import hoje,calc_montante
from logging import info,error

def create_database() -> NoReturn:
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
    info("Criando base de dados.")
    database_path = "database.json"
    if os.path.exists(database_path):
        info("Base de dados já existente! Não será criada uma nova.")
    else:
        # Creates a JSON dictionary with keys "data", "type", "value", and "amount", all with initial values of None
        json_base = {
            "id":[],
            "data_de_criacao": [],
            "ultima_atualizacao": [],
            "tipo": [],
            "valor": [],
            "taxa":[],
            "montante": []
        }

        # Cria a base de dados chamada "database.json"
        try:
            info("Criando a base de dados em json")
            with open(database_path, "w") as file:
                json.dump(json_base, file, indent=4)
            info("Base de dados criada com sucesso!!")
        except Exception as err:
            error("Erro ao criar a base de dados")

def atualiza_rendimento() -> None:
    '''
    '''
    info("Atualizando os investimentos.")
    # Verificando se o arquivo de banco de dados existe
    database_path = 'database.json'
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo 'database.json' não encontrado!")
    
    try:
        # Lendo a base de dados
        database_path = 'database.json'
        with open(database_path,'r') as file:
            database = json.load(file)
        
        for i in database['id']:
            if database['tipo'][i].lower() == "investimento":
                dia_da_transacao,dia_atual = datetime.strptime(database['data_de_criacao'][i],"%d/%m/%Y %H:%M:%S"),datetime.today()
                dias_passados = abs((dia_atual - dia_da_transacao).days)
                database['ultima_atualizacao'][i] = hoje()
                database['montante'][i] = round(calc_montante(capital=database['valor'][i],taxa=database['taxa'][i],tempo=dias_passados),2)

        with open(database_path,'w') as file:
                json.dump(database,file,indent=4)
        info("Investimentos atualizados com sucesso!")
    except Exception as err:
        error("Erro ao atualizar os investimentos")
        raise err

def inserir_registro(valor:float,tipo:Literal['Receita','Despesas','Investimento'],taxa:float=None) -> None:
    '''
    '''
    info("Inserindo valor no banco de dados.")
    if tipo not in ['Receita','Despesas','Investimento']:
        raise ValueError("Este tipo transação não permitido!")

    # Verificando se é investimento e se a taxa está preenchida
    if tipo.casefold() == "Investimento".casefold() and taxa is None:
        raise ValueError("Taxa não pode ser None.")
    elif tipo.casefold() == "Investimento".casefold() and not isinstance(taxa,float):
        raise ValueError("Taxa precisa ser float.")
    
    # Verificando se o arquivo de banco de dados existe
    database_path = 'database.json'
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo 'database.json' não encontrado!")
    
    try:
        database['id'].append(0 if not database['id'] else database['id'][-1] + 1)
        database['data_de_criacao'].append(hoje())
        database['ultima_atualizacao'].append(hoje())
        database['tipo'].append(tipo)
        database['valor'].append(valor if tipo != "Despesas" else -valor)
        database['taxa'].append(taxa if tipo == "Investimento" else None)
        database['montante'].append(None)

        with open(database_path,'w') as file:
            json.dump(database,file,indent=4)
        
        info("Valor inserido com sucesso!")
    except Exception as err:
        error(f"Erro ao inserir no banco de dados.")
        raise err
    
def ler_registros(data_de_registro:Tuple[str,str] = None,tipo:Literal['Receita','Despesas','Investimento'] = None,valor:Tuple[float,float] = None) -> Optional[dict]:
    """
    Função para ler registros do banco de dados.

    Parâmetros:
    - data_de_registro (Tuple[str, str]): Período de data de registro (formato: "%d/%m/%Y").
    - tipo (Literal['Receita', 'Despesas', 'Investimento']): Tipo de transação.
    - valor (Tuple[float, float]): Faixa de valores permitidos.

    Retorna:
    - dict: Dicionário contendo os registros correspondentes aos critérios de pesquisa.

    Exceções:
    - FileNotFoundError: Caso o arquivo "database.json" não seja encontrado.
    - ValueError: Caso ocorra um erro específico nos parâmetros de entrada.
    """
    # Verificando se o arquivo de banco de dados existe
    database_path = 'database.json'
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo 'database.json' não encontrado!")
    
    # Verificando as datas
    if data_de_registro is not None:
        data_inicial,data_final = datetime.strptime(data_de_registro[0],"%d/%m/%Y"),datetime.strptime(data_de_registro[1],"%d/%m/%Y")
        if data_inicial < data_final:
            raise ValueError("A data de inicio não pode ser menor que a data de fim!")
    
    # Verificando o tipo
    if tipo is not None:
        if tipo not in ['Receita','Despesas','Investimento']:
            raise ValueError("Este tipo transação não permitido!")
        
    # Verificando o valor
    if valor is not None:
        valor_min, valor_max = valor[0], valor[1]
        if valor_min > valor_max:
            raise ValueError("O valor minimo não pode ser maior que o valor max!")
    

def deletar_registro(id:int):
    '''
    '''
    info(f"Deletando registro de id {id}.")
    # Verificando se o arquivo de banco de dados existe
    database_path = 'database.json'
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo 'database.json' não encontrado!")
    
    # Verifica se o ID existe na base de dados
    if id not in database['id']:
        raise Exception(f"Registro com id {id} não encontrado!")
    
    try:
        
        for i in range(0,len(database['id'])):
            if i == id:
                for key in database.keys():
                    database[key].pop(i)
        database['id'] = [i for i in range(0,len(database['id']))]
            
        with open(database_path,'w') as file:
            json.dump(database,file,indent=4)
        info(f"Registro de id {id} deletado com sucesso!")
    except Exception as err:
        error("Erro ao atualizar os investimentos")
        raise err
    
def alterar_registro(id:int,valor:float=None,tipo:Literal['Receita','Despesas','Investimento'] = None,taxa:float=None) -> bool:
    '''
    '''
    # Verificando se o arquivo de banco de dados existe
    database_path = 'database.json'
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo 'database.json' não encontrado! Registro não alterador!")
    
    # Verifica se o ID existe na base de dados
    if id not in database['id']:
        raise Exception(f"Registro com id {id} não encontrado! Registro não alterador!")
    
    if valor is None and tipo is None:
        raise Exception("Ou tipo ou valor precisame estar preenchidos! Registro não alterador!")
    
    # Verifica a entrada errada o usuário
    if tipo == "Investimento" and taxa is not None:
        if not isinstance(taxa, float):
            raise Exception("Taxa precisa receber um valor float! Registro não alterado!")
        if taxa < 0:
            raise Exception("Taxa precisa ser maior ou igual 0! Registro não alterador!")
    
    try:
        for i in database['id']:
            if i == id:
                database['ultima_atualizacao'][i] = hoje()
                if tipo is None:
                    database['valor'][i] = valor
                else:
                    match(tipo):
                        case "Receita":
                            database['tipo'][i] = tipo
                            database['taxa'][i] = None
                            database['montante'][i] = None
                            if valor is None:
                                database['valor'][i] = database['valor'][i] if database['valor'][i] >= 0 else database['valor'][i]*(-1)
                            else:
                                database['valor'][i] = valor   
                        case "Despesas":
                            database['tipo'][i] = tipo
                            database['taxa'][i] = None
                            database['montante'][i] = None
                            if valor is None:
                                database['valor'][i] = database['valor'][i] if database['valor'][i] <= 0 else database['valor'][i]*(-1)
                            else:
                                database['valor'][i] = valor
                        case "Investimento":
                            database['tipo'][i] = tipo
                            database['taxa'][i] = taxa if  taxa is not None else database['taxa'][i] if database['taxa'][i] is None else 0.0
                            database['montante'][i] = None
                            if valor is None:
                                database['valor'][i] = database['valor'][i] if database['valor'][i] >= 0 else database['valor'][i]*(-1)
                            else:
                                database['valor'][i] = valor
        
        try:
            with open(database_path,'w') as file:
                json.dump(database,file,indent=4)
        except Exception as err:
            error("Erro ao salvar a base de dados!")
            raise err
        
        info("Registro alterado com sucesso!")

    except Exception as err:
        error(f"Erro inesperado ao alterar o registro -> {err}")
        raise err