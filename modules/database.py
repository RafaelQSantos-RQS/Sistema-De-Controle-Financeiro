import csv
from pathlib import Path
from datetime import datetime
from logging import info, error
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