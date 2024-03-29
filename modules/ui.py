from tkinter import *
from tkinter import ttk,Tk, Label, Button
from modules.database import Localbase

class JanelaPrincipal:
    def __init__(self):
        # Cria a janela principal
        self.janela = Tk()

        # Inicializando as camadas
        self.init_camadas()

        # Inicializando os labels
        self.init_labels()

        # Inicializa os botões
        self.init_buttons()

    def inicializar(self):

        # Define o título da janela
        self.janela.title("Sistema de Controle Financeiro")

        # Centraliza a janela
        self.janela.eval('tk::PlaceWindow . center')

        # Configurações
        self.config()
    
    def config(self):
        self.janela.config(borderwidth=0,relief='ridge')

    def init_camadas(self):
        '''
        '''
        self.primeiracamada = Frame(self.janela)
        self.primeiracamada.pack()

        self.segundacamada = Frame(self.janela)
        self.segundacamada.pack()

        self.terceiracamada = Frame(self.janela)
        self.terceiracamada.pack()

        self.quartacamada = Frame(self.janela)
        self.quartacamada.pack()
    
    def init_labels(self):
        '''
        '''
        self.label = Label(self.primeiracamada, text="O que deseja fazer hoje?")
        self.label.pack()
    
    def init_buttons(self):
        '''
        '''
        width = 15
        # Botão de Criar
        self.create_bttn = Button(self.segundacamada, text="Criar",command=self.criar,width=width)
        self.create_bttn.pack(side=LEFT,pady=5,padx=5)

        # Botão de Ler
        self.read_bttn = Button(self.segundacamada, text="Ler",width=width)
        self.read_bttn.pack(side=RIGHT,pady=5,padx=5)

        # Botão de Atualizar
        self.att_bttn = Button(self.terceiracamada, text="Atualizar",width=width)
        self.att_bttn.pack(side=LEFT,pady=5,padx=5)

        # Botão de Deletar
        self.del_bttn = Button(self.terceiracamada, text="Deletar",width=width)
        self.del_bttn.pack(side=RIGHT,pady=5,padx=5)

        # Botão de Exportar
        self.exportar_btn = Button(self.quartacamada, text="Exportar",width=width)
        self.exportar_btn.pack(side=LEFT,pady=5,padx=5)

        # Botão de Sair
        self.exit_bttn = Button(self.quartacamada, text="Sair", command=self.sair,width=width)
        self.exit_bttn.pack(side=RIGHT,pady=5,padx=5)

    def criar(self):
        '''
        '''
        janela_de_criar = JanelaCriar()
        janela_de_criar.inicializar()
        janela_de_criar.rodar()


    def sair(self):
        # Fecha a janela
        self.janela.destroy()

    def rodar(self):
        # Mostra a janela
        self.janela.mainloop()

class JanelaDeInformacao:
    def __init__(self, mensagem):
        self.janela = Tk()
        self.janela.title("Informação")

        self.label_mensagem = Label(self.janela, text=mensagem)
        self.label_mensagem.pack(padx=20, pady=10)

        self.botao_ok = Button(self.janela, text="OK", command=self.fechar_janela)
        self.botao_ok.pack(pady=10)

        self.janela.eval('tk::PlaceWindow . center')

    def fechar_janela(self):
        self.janela.destroy()

    def mostrar(self):
        self.janela.mainloop()

class JanelaCriar:
    def __init__(self):
        # Cria a janela principal
        self.janela = Tk()

        # Inicializando as camadas
        self.init_camadas()

        # Inicializando os labels
        self.init_labels()

        # Inicializa os botões
        self.init_components()

    def inicializar(self):
        '''
        '''
        # Define o título da janela
        self.janela.title("Novos registros")

        # Centraliza a janela
        self.janela.eval('tk::PlaceWindow . center')

    def init_camadas(self):
        '''
        '''
        self.primeira_camada = Frame(self.janela)
        self.primeira_camada['pady'] = 10
        self.primeira_camada.pack()

        self.segunda_camada = Frame(self.janela)
        self.segunda_camada['padx'] = 10
        self.segunda_camada['pady'] = 5
        self.segunda_camada.pack()

        self.terceira_camada = Frame(self.janela)
        self.terceira_camada['padx'] = 10
        self.terceira_camada['pady'] = 5
        self.terceira_camada.pack()

        self.quarta_camada = Frame(self.janela)
        self.quarta_camada['padx'] = 10
        self.quarta_camada['pady'] = 5
        self.quarta_camada.pack()

        self.quinta_camada = Frame(self.janela)
        self.quinta_camada['padx'] = 10
        self.quinta_camada['pady'] = 5
        self.quinta_camada.pack()
    
    def init_labels(self):
        '''
        '''
        self.label = Label(self.primeira_camada, text="Insira as informações desejadas:")
        self.label.pack()
    
    def init_components(self):
        '''
        '''
        width = 20
        # Transação
        self.type_label = Label(self.segunda_camada, text="Tipo de transação",width=width)
        self.type_label.pack(side=LEFT)
        self.type_combobx = ttk.Combobox(self.segunda_camada,values=['Receita','Despesas','Investimento'],width=width)
        self.type_combobx.config(state='readonly')
        self.type_combobx.pack(side=LEFT)

        # Valor da Transação
        self.label_valor_da_transacao = Label(self.terceira_camada, text="Insira o valor da transação",width=width)
        self.label_valor_da_transacao.pack(side=LEFT)
        self.valor_da_transacao = Entry(self.terceira_camada,width=width)
        self.valor_da_transacao.pack(side=LEFT)

        # Valor da Taxa
        self.label_valor_da_taxa = Label(self.quarta_camada, text="Insira o valor da taxa ()",width=width)
        self.label_valor_da_taxa.pack(side=LEFT)
        self.valor_da_taxa = Entry(self.quarta_camada,width=width)
        self.valor_da_taxa.pack(side=LEFT)

        # Botão de Confirmar
        self.confirm_bttn = Button(self.quinta_camada,text="Confirmar",command=self.inserir_registros,width=15)
        self.confirm_bttn.pack(side=LEFT,padx=5)

        # Botão de Sair
        self.exit_bttn = Button(self.quinta_camada, text="Sair", command=self.sair, width=15)
        self.exit_bttn.pack(side=RIGHT,padx=5)

    def sair(self):
        # Fecha a janela
        self.janela.destroy()

    def rodar(self):
        # Mostra a janela
        self.janela.mainloop()

    def inserir_registros(self):
        '''
        '''
        try:
            database = Localbase(database_file='database.csv')
            tipo = self.type_combobx.get()
            valor = float(self.valor_da_transacao.get().strip()) if self.valor_da_transacao.get() != '' else None
            taxa = float(self.valor_da_taxa.get()) if self.valor_da_taxa.get() != '' else None
            database.inserir_registro(valor=valor,tipo=tipo,taxa=taxa)
            JanelaDeInformacao("Valor inserido com sucesso!!").mostrar()
        except Exception as err:
            JanelaDeInformacao(f"Eerro ao inserir um valor:\n{err}").mostrar()

class JanelaDeLeitura:
    def __init__(self):
        # Cria a janela principal
        self.janela = Tk()

        # Inicializando as camadas
        self.init_camadas()

        # Inicializando os labels
        self.init_labels()

        # Inicializa os botões
        self.init_components()

    def inicializar(self):
        '''
        '''
        # Define o título da janela
        self.janela.title("Novos registros")

        # Centraliza a janela
        self.janela.eval('tk::PlaceWindow . center')

    def init_camadas(self):
        '''
        '''
        self.primeira_camada = Frame(self.janela)
        self.primeira_camada['pady'] = 10
        self.primeira_camada.pack()

        self.segunda_camada = Frame(self.janela)
        self.segunda_camada['padx'] = 10
        self.segunda_camada['pady'] = 5
        self.segunda_camada.pack()

        self.terceira_camada = Frame(self.janela)
        self.terceira_camada['padx'] = 10
        self.terceira_camada['pady'] = 5
        self.terceira_camada.pack()

        self.quarta_camada = Frame(self.janela)
        self.quarta_camada['padx'] = 10
        self.quarta_camada['pady'] = 5
        self.quarta_camada.pack()

        self.quinta_camada = Frame(self.janela)
        self.quinta_camada['padx'] = 10
        self.quinta_camada['pady'] = 5
        self.quinta_camada.pack()
    
    def init_labels(self):
        '''
        '''
        self.label = Label(self.primeira_camada, text="Selecione as informações desejadas:")
        self.label.pack()
    
    def init_components(self):
        '''
        '''
        width = 20
        # Transação
        self.type_label = Label(self.segunda_camada, text="Tipo de transação",width=width)
        self.type_label.pack(side=LEFT)
        self.type_combobx = ttk.Combobox(self.segunda_camada,values=['Receita','Despesas','Investimento'],width=width)
        self.type_combobx.config(state='readonly')
        self.type_combobx.pack(side=LEFT)

        # Valor da Transação
        self.label_valor_da_transacao = Label(self.terceira_camada, text="Insira o valor da transação",width=width)
        self.label_valor_da_transacao.pack(side=LEFT)
        self.valor_da_transacao = Entry(self.terceira_camada,width=width)
        self.valor_da_transacao.pack(side=LEFT)

        # Valor da Taxa
        self.label_valor_da_taxa = Label(self.quarta_camada, text="Insira o valor da taxa ()",width=width)
        self.label_valor_da_taxa.pack(side=LEFT)
        self.valor_da_taxa = Entry(self.quarta_camada,width=width)
        self.valor_da_taxa.pack(side=LEFT)

        # Botão de Confirmar
        self.confirm_bttn = Button(self.quinta_camada,text="Confirmar",command=self.inserir_registros,width=15)
        self.confirm_bttn.pack(side=LEFT,padx=5)

        # Botão de Sair
        self.exit_bttn = Button(self.quinta_camada, text="Sair", command=self.sair, width=15)
        self.exit_bttn.pack(side=RIGHT,padx=5)

    def sair(self):
        # Fecha a janela
        self.janela.destroy()

    def rodar(self):
        # Mostra a janela
        self.janela.mainloop()