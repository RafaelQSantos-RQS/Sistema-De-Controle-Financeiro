
from datetime import datetime

def hoje() -> str:
    '''
    '''
    return datetime.today().strftime("%d/%m/%Y %H:%M:%S")

def calc_montante(capital:float,taxa:float,tempo:int) -> float:
    '''
    '''
    return  0.0 if tempo == 0 else capital*(1+taxa)**tempo