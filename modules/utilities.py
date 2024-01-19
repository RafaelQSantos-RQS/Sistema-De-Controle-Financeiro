import os
import json
from datetime import datetime

def hoje() -> None:
    '''
    '''
    return datetime.today().strftime("%d/%m/%Y %H:%M:%S")

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
        "data": [],
        "tipo": [],
        "valor": [],
        "montante": []
    }

    # Opens the "database.json" file in write mode
    with open(database_path, "w") as file:
        # Writes the JSON dictionary to the JSON file with an indentation of 4 spaces for better readability
        json.dump(json_base, file, indent=4)

    return None

def insert_values(valor:float,tipo:str) -> None:
    '''
    '''
    database_path = 'database.json'
    with open(database_path,'r') as file:
        database = json.load(file)
    
    database['data'].append(hoje())
    database['tipo'].append(tipo)
    database['valor'].append(valor)
    database['montante'].append(None)

    with open(database_path,'w') as file:
        json.dump(database,file,indent=4)
