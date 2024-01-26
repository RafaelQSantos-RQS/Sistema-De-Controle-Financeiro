import os
import csv
import json
from pathlib import Path
from datetime import datetime
from logging import info, error
from prettytable import PrettyTable
from typing import NoReturn,Literal,Optional
from modules.utilities import hoje,calc_montante

class Localbase:
    '''
    '''
    def __init__(self,database_file:str) -> None:
        self.database_path = database_file
        self.inicializar_base_de_dados()

    def ultimo_id(self) -> int:
        '''
        Retorna o último ID na base de dados incrementado de 1.
        Se a base de dados estiver vazia, retorna 0.
        '''
        info("Obtendo o último ID na base de dados.")
        database_path = self.database_path
        
        # Obter todos os IDs existentes
        todos_ids = []
        with open(database_path, 'r', newline='', encoding='utf-8') as database:
            leitor = csv.reader(database, delimiter=';')
            next(leitor, None)  # Ignorar cabeçalho
            todos_ids = [int(linha[0]) for linha in leitor]
        
        # Calcular o novo ID
        novo_id = todos_ids[-1] if todos_ids else 0
        return novo_id

    def inicializar_base_de_dados(self) -> NoReturn:
        info("Verificando se já existe uma base de dados.")
        database_path = self.database_path
        
        if not Path(database_path).is_file():
            info("Base de dados não existente! Criando uma nova.")
            header = [
                'id',
                'data_de_criacao',
                'ultima_atualizacao',
                'tipo',
                'valor',
                'taxa',
                'montante']
            
            try:
                with open(database_path, 'w', newline='', encoding='utf-8') as database:
                    leitor = csv.writer(database, delimiter=';')
                    leitor.writerow(header)
            except FileNotFoundError as e:
                error(f"O diretório para a base de dados não foi encontrado.")
                raise e
            except PermissionError as e:
                error(f"Permissão negada para criar a base de dados.")
                raise e
            except csv.Error as e:
                error(f"Erro ao criar a base de dados -> {e}")
                raise e
            except Exception as e:
                error(f"Um erro inesperado aconteceu! -> {e}")
                raise e

        else:
            info("Base de dados já existente. Nenhuma ação necessária.")

    def atualiza_rendimento(self) -> NoReturn:
        '''
        '''
        database_path = self.database_path
        try:
            with open(database_path,'r',newline='',encoding='utf-8') as database_inicial:
                leitor = csv.reader(database_inicial,delimiter=';')
                cabecalho = next(leitor)
                linhas = list(leitor)

                for linha in linhas:
                    if linha[3] == "Investimento": # Tipo
                        dia_da_transacao,dia_atual = datetime.strptime(linha[1],"%d/%m/%Y %H:%M:%S"),datetime.today()
                        dias_passados = abs((dia_atual - dia_da_transacao).days)
                        linha[2] = hoje() # Última atualização
                        linha[-1] = round(calc_montante(capital=float(linha[-3]),taxa=float(linha[-2]),tempo=dias_passados),2) # montante
            
            with open(database_path,'w',newline='',encoding='utf-8') as database_final:
                escritor = csv.writer(database_final,delimiter=';')
                escritor.writerow(cabecalho)
                escritor.writerows(linhas)
            
            info("Rendimento(s) atualizado(s) com sucesso!!")
        except FileNotFoundError as err:
            error(f"O diretório para a base de dados não foi encontrado.")
            raise err
        except Exception as err:
            error(f"Erro estranho ao atualizar os rendimentos!! -> {err}")
            raise err

    def inserir_registro(self,valor:float,tipo:Literal['Receita','Despesas','Investimento'],taxa:float=None) -> NoReturn:
        '''
        '''
        info("Inserindo valor no banco de dados.")
        if tipo not in ['Receita','Despesas','Investimento']:
            raise ValueError("Este tipo transação não permitido!")

        # Verificando se é investimento e se a taxa está preenchida
        info("Verificando se o registro será de investimento e se a taxa está preenchida")
        if tipo.casefold() == "Investimento".casefold() and taxa is None:
            raise ValueError("Taxa não pode ser None.")
        elif tipo.casefold() == "Investimento".casefold() and not isinstance(taxa,float):
            raise ValueError("Taxa precisa ser float.")
        
        try:
            novo_id = self.ultimo_id() + 1
            data_de_criacao = hoje()
            ultima_atualizacao = hoje()
            tipo = tipo
            valor = valor if tipo != "Despesas" else -valor
            taxa = taxa if tipo == "Investimento" else None
            montante = None

            database_path = self.database_path
            with open(database_path, 'a', newline='', encoding='utf-8') as database:
                escritor = csv.writer(database, delimiter=';')
                escritor.writerow([novo_id, data_de_criacao, ultima_atualizacao, tipo, valor, taxa, montante])

            info("Valores inseridos com sucesso!")

        except FileExistsError as err:
            error("Base de dados não existente! Reexecute o código para a criação de uma nova!")
            raise err
        except Exception as err:
            error(f"Erro desconhecido! -> {err}")
            raise err
        
    def ler_registros(self,data:tuple=None,tipo:Literal['Receita','Despesas','Investimento']=None,valor:tuple=None,print_table:bool=False) -> Optional[list]:
        '''
        Lê registros do banco de dados com base nos filtros fornecidos.

        Parâmetros
        ----------
        - data (tuple): Um intervalo de datas representado por uma tupla de duas strings no formato '%d/%m/%Y'. 
                        Se fornecido, filtra registros com data dentro desse intervalo.
        - tipo (Literal['Receita', 'Despesas', 'Investimento']): Tipo de transação a ser filtrado. Se fornecido,
                        filtra registros apenas pelo tipo especificado.
        - valor (tuple): Um intervalo de valores representado por uma tupla de dois floats. Se fornecido,
                        filtra registros com valores dentro desse intervalo.
        - print_table (bool): Se True, imprime os resultados em forma de tabela. Se False, retorna os resultados como uma lista.

        Retorna
        -------
        - Se print_table for `True`, imprime os resultados na forma de uma tabela. 
        - Se print_table for `False`, retorna uma lista contendo os registros filtrados, onde cada registro é uma lista de valores.

        Raises
        ------
        - ValueError: Se os parâmetros fornecidos não estiverem no formato esperado ou se houver um erro ao processar os dados.

        Exemplos
        --------
        - Para ler registros entre '01/01/2022' e '31/01/2022' do tipo 'Receita':
        `ler_registros(data=('01/01/2022', '31/01/2022'), tipo='Receita', print_table=True)`
        - Para ler registros com valores entre 1000.0 e 2000.0:
        `ler_registros(valor=(1000.0, 2000.0), print_table=False)`
        '''
        try:
            database_path = self.database_path
            with open(database_path,'r',newline='',encoding='utf-8') as database:
                leitor = csv.reader(database,delimiter=';')
                cabecalho = next(leitor)
                linhas = list(leitor)

                # Filtro de data
                if data is not None:

                    # Verificação de entrada do usuário
                    if not isinstance(data, tuple) or len(data) != 2:
                        raise ValueError("A entrada de data deve ser uma tupla contendo duas strings.")
                    for data_str in data:
                        try:
                            datetime.strptime(data_str, "%d/%m/%Y")
                        except ValueError:
                            raise ValueError(f"Formato de data inválido: {data_str}. Utilize o formato %d/%m/%Y.")
                        
                    data_inicial,data_final = datetime.strptime(data[0],"%d/%m/%Y"),datetime.strptime(data[1],"%d/%m/%Y").replace(hour=23,minute=59,second=59)
                    linhas_filtro_data = [linha for linha in linhas if data_inicial <= datetime.strptime(linha[1],"%d/%m/%Y %H:%M:%S") <= data_final]
                else:
                    linhas_filtro_data = [linha for linha in linhas]

                # Filtro de tipo
                if tipo is not None:
                    
                    # Verificação de entrada do usuário
                    if tipo not in ['Receita','Despesas','Investimento']:
                        raise ValueError("Este tipo transação não permitido!")
                    
                    linhas_filtro_tipo = [linha for linha in linhas_filtro_data if linha[-4] == tipo]
                else:
                    linhas_filtro_tipo = [linha for linha in linhas_filtro_data]

                # Filtro
                if valor is not None:

                    # Verificação de entrada do usuário
                    if not isinstance(valor, tuple) or len(valor) != 2:
                        raise ValueError("A entrada de valor deve ser uma tupla contendo dois floats.")
                    
                    for valor_str in valor:
                        try:
                            float(valor_str)
                        except ValueError:
                            raise ValueError(f"Formato de valor inválido: {valor_str}. Utilize valores numéricos.")

                    valor_inicial,valor_final = float(valor[0]),float(valor[1])
                    linhas_filtro_valor = [linha for linha in linhas_filtro_tipo if valor_inicial <= float(linha[-3]) <= valor_final]
                else:
                    linhas_filtro_valor = [linha for linha in linhas_filtro_tipo]

                # Imprimindo tabela ou retornando
                if not isinstance(print_table,bool):
                    raise ValueError("Valor inserido na variável print_table deve ser booleana (True | False)")
                    
                if print_table:
                    table = PrettyTable()
                    table.field_names = cabecalho
                    table.add_rows(linhas_filtro_valor)
                    print(table)
                else:
                    linhas_filtro_valor.insert(0,list(cabecalho))
                    return linhas_filtro_valor

        except Exception as err:
            error(f"Erro ao ler registros -> {err}")
            raise err
        
    def deletar_registro(self,id:int) -> NoReturn:
        """
        Deleta um registro da base de dados com base no ID fornecido.

        Parâmetros:
        -----------
            - id (int): O ID do registro a ser deletado.

        Retorna:
        --------
            - None

        Exceções:
        ---------
            - FileNotFoundError: Caso o arquivo da base de dados não seja encontrado.
            - csv.Error: Caso ocorra um erro ao processar o arquivo CSV.
            - ValueError: Caso o ID fornecido não exista na base de dados.
            - Exception: Para outros erros inesperados durante a execução.

        Observações:
        ------------
            - A função realiza a leitura do arquivo CSV, verifica a existência do ID,
            cria uma nova lista de linhas sem o registro correspondente e escreve
            as novas linhas de volta no arquivo.
            - Certifique-se de utilizar a função em instâncias da classe onde ela está definida.

        Exemplo:
        --------
            localbase_instance.deletar_registro(123)
        """
        try:
            database_path = self.database_path
            with open(database_path,'r',newline='',encoding='utf-8') as database:
                leitor = csv.reader(database,delimiter=';')
                cabecalho = next(leitor)
                linhas = list(leitor)
                lista_de_ids = [int(linha[0]) for linha in linhas]
                if id not in lista_de_ids:
                    raise ValueError("O id fornecido não existe!")
                
                # Criar nova lista de linhas sem a linha a ser excluída
                novas_linhas = [linha for linha in linhas if int(linha[0]) != id]

            with open(database_path,'w',newline='',encoding='utf-8') as database:
                escritor = csv.writer(database,delimiter=';')
                escritor.writerow(cabecalho)
                escritor.writerows(novas_linhas)
            info(f"O registro de {id} foi deletado com sucesso!!")

        except FileNotFoundError as err:
            error(f"Arquivo não encontrado: {database_path}")
            raise err

        except csv.Error as err:
            error(f"Erro ao processar arquivo CSV: {err}")
            raise err

        except ValueError as err:
            error(f"Erro ao deletar registro: {err}")
            raise err

        except Exception as err:
            error(f"Erro inesperado ao deletar registro: {err}")
            raise err
        
    def alterar_registro(self,id:int,valor:Optional[float]=None,tipo:Optional[Literal['Receita','Despesas','Investimento']] = None,taxa:Optional[float]=None):
        '''
        '''
        try:
            if not isinstance(id,int):
                raise ValueError("O id tem que ser Inteiro.")
            if valor is None and tipo is None and taxa is None:
                raise ValueError("Pelo menos um dos parâmetros (valor, tipo, taxa) deve ser diferente de None.")
            if taxa is not None and not isinstance(taxa,float):
                raise ValueError("Taxa precisa ser um valor float")
            if tipo is not None and tipo not in ['Receita','Despesas','Investimento']:
                raise ValueError("O tipo informado não é reconhecido pelo sistema.")
            if tipo == "Investimento" and taxa is None:
                raise ValueError("Para alterar um registro para investimento é preciso informar uma taxa associada!")
            
            database_path = self.database_path
            with open(database_path,'r',newline='',encoding='utf-8') as database:
                leitor = csv.reader(database,delimiter=';')
                cabecalho = next(leitor)
                linhas = list(leitor)
                lista_de_ids = [int(linha[0]) for linha in linhas]
                if id not in lista_de_ids:
                    raise ValueError("O id fornecido não existe!")
                
                for linha in linhas:
                    if int(linha[0]) == id:
                        if valor is not None and tipo is None and taxa is None: # Caso 1 (Só valor)
                            linha[-3] = valor if linha[-4] != "Despesas" else abs(valor)*-1
                        if valor is None and tipo is not None: # Caso 2 (Só Tipo)
                            tipo_anterior = linha[-4]
                            linha[-3] = abs(float(linha[-3])) * (-1 if tipo_anterior == "Despesas" else 1)  # Valor
                            linha[-1] = None if tipo in ["Receita","Despesas"] else linha[-1] # Montante
                            linha[-2] = taxa if tipo == "Investimento" else None # Taxa
                            linha[-4] = tipo # Tipo
                            linha[2] = hoje() # Última atualização
                        if valor is None and tipo is None and taxa is not None: # Caso 3 (Só Taxa)
                            if linha[-4] != "Investimento":
                                raise ValueError("A operação não pode ser feita, taxa só pode se alterado em registro de investimento")
                            else:
                                linha[-2] = taxa

        except Exception as err:
            pass

    def exportar_relatorio(self,path:str = '.',formato:Literal['csv','json'] = 'csv',**kwargs):
        '''
        Exporta um relatório para o formato especificado.

        Parâmetros
        ----------
        - path (str): O caminho do diretório onde o relatório será exportado. Padrão: diretório atual.
        - formato (Literal['csv', 'json']): O formato de exportação do relatório. Padrão: 'csv'.
        - **kwargs: Parâmetros adicionais a serem passados para a função ler_registros.

        Parâmetros Extras (via **kwargs)
        ---------------------------------
        - tipo (Literal['Receita', 'Despesas', 'Investimento']): Filtro por tipo de transação.
        - valor (tuple): Filtro por faixa de valores.
        - data (tuple): Filtro por intervalo de datas no formato ("%d/%m/%Y", "%d/%m/%Y").

        Raises
        ------
        - ValueError: Se o formato fornecido não for 'csv' ou 'json'.
        - ValueError: Se o diretório fornecido não existir.
        - ValueError: Se não houver permissão de escrita no diretório fornecido.
        - Exception: Qualquer erro durante o processo de exportação.

        Exemplos
        --------
        - Exportar um relatório CSV no diretório atual:
            exportar_relatorio(formato='csv')
        - Exportar um relatório JSON em um diretório específico:
            exportar_relatorio(path='/caminho/do/diretorio', formato='json', tipo='Receita', valor=(100, 500))
        '''
        try:
            # Verificar se o formato é válido
            info("Verificando se o formato é válido")
            if formato not in ['csv','json']:
                raise ValueError("O formato inserido não é válido")
            
            # Verificar se o diretório existe
            info("Verificando se o diretório existe")
            if not os.path.exists(path):
                raise ValueError("O diretório fornecido não existe.")

            # Verificar se o diretório é acessível
            info("Verificando se o diretório é acessível")
            if not os.access(path, os.W_OK):
                raise ValueError("Sem permissão para escrever no diretório fornecido.")
            
            kwargs.pop('print_table',None)
            dados = self.ler_registros(**kwargs)

            match(formato):
                case 'csv':
                    try:
                        info("Exportando para csv")
                        with open(os.path.join(path,'relatorio.csv'),'w',newline='',encoding='utf-8') as csv_file:
                            escritor = csv.writer(csv_file,delimiter=';')
                            escritor.writerows(dados)
                    except Exception as err:
                        error("Erro ao exportar para csv!")
                        raise err
                case 'json':
                    try:
                        info("Exportando para json")
                        cabecalho = dados[0]
                        lista_de_dicionarios = [dict(zip(cabecalho, linha)) for linha in dados[1:]]
                        dicionario = {
                            'data_de_exportacao':hoje(),
                            'dados':lista_de_dicionarios
                        }
                        with open(os.path.join(path,'relatorio.json'),'w') as json_file:
                            json_file.write(json.dumps(dicionario,indent=2))
                    except Exception as err:
                        error("Erro ao exportar para json!")
                        raise err
            info("Exportação feita com sucesso!!")
        except Exception as err:
            error(f"Erro ao exportar o relatório -> {err}")
            raise err