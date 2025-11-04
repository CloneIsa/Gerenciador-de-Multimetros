#Anderson Cerqueira - 0031
#Danieli Aguiar - 0015
#Giovanni Araújo - 0006
#Kaylane Brandão - 0013
#Larissa Isabelle - 0029

#Bibliotecas para janela gráfica
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

#Biblioteca para conexão com o mongoDB
from pymongo import MongoClient #Usar o comando pip install pymongo no terminal

class Conexao_bd:
    #Conexão com o banco de dados
    def __init__(self):
        self.conexao_mongo = MongoClient('localhost', 27017)
        self.db = self.conexao_mongo['MeuBancodeDados']
        self.multimetros = self.db['multimetros']
        self.manutencoes = self.db['manutencoes']

    #Cadastrar um novo multímetro
    def inserir_multimetro(self, id, marca, modelo, status, observacoes, patrimonio):
        self.multimetros.insert_one({
            "_id": id,
            "marca": marca,
            "modelo": modelo,
            "status": status,
            "observacoes": observacoes,
            "patrimonio": patrimonio
        })

    #Remover multímetro existente
    def remover_multimetros(self, id):
        self.multimetros.delete_one({'_id': id})

    #Lista com todos os multímetros cadastrados
    def todos_multimetros(self):
        return list(self.multimetros.find())
    
    #Lista de multímetros disponíveis
    def multimetros_disponiveis(self):
        return list(self.multimetros.find({'status': 'Disponível'}))
    
    #Buscar multímetro pelo id
    def buscar_multimetro(self, id):
        return self.multimetros.find_one({'_id': id})
    
    #Buscar multímetro pelo ipatrimônio
    def buscar_pat(self, patrimonio):
        return self.multimetros.find_one({'patrimonio': patrimonio})
    
      #Atualização de status ao adicionar manutenção
    def atualizar_status(self,id,novo_status):
        self.multimetros.update_one(
            {"_id": id},
            {"$set":{"status": novo_status}}
        )

    #Para manutenção
    def inserir_manutencao(self, manut_id, mult_id, tipo, data, tecnico, observacao):
        self.manutencoes.insert_one({
            '_id': manut_id,
            'multimetro_id': mult_id,
            'tipo': tipo,
            'data': data,
            'tecnico': tecnico,
            'observacao': observacao
        })

    def remover_manutencao(self, manut_id):
        self.manutencoes.delete_one({'_id': manut_id})

    def todas_manutencoes(self):
        return list(self.manutencoes.find())

#Janela
class Aplicativo():
    def __init__(self, parent :tk.Tk):
        #Definindo tamanho da janela
        parent.geometry('1000x850')

        #Frame criado para conter todas as demais funções da tela
        self.lbl_busca = ttk.Label(parent, text= "Gerenciamento de Multímetros",
                                        font=('Arial', 12, 'bold'),
                                        background= 'lightblue')
        self.frm_busca = ttk.LabelFrame(parent)

        #Para manutenções
        self.lbl_manut = ttk.Label(parent, text= "Gerenciamento da Manutenção dos Multímetros",
                                        font=('Arial', 12, 'bold'),
                                        background= 'lightblue')
        self.frm_manut = ttk.LabelFrame(parent)

        #Definição dos textbox/combobox
        self.txb_id = ttk.Entry(self.frm_busca)
        self.txb_marca = ttk.Entry(self.frm_busca)
        self.txb_modelo = ttk.Entry(self.frm_busca)
        self.cmb_disponibilidade = ttk.Combobox(self.frm_busca,
                                                values= ["Disponível", "Indisponível"],
                                                width=17)
        self.txb_observacoes = ttk.Entry(self.frm_busca)
        self.txb_pat = ttk.Entry(self.frm_busca)
        self.txb_buscar = ttk.Entry(self.frm_busca)
        self.txb_buscar_pat = ttk.Entry(self.frm_busca)

        #Definição dos textbox p/manut
        self.txb_manut_id = ttk.Entry(self.frm_manut)
        self.txb_mult_id = ttk.Entry(self.frm_manut)
        self.txb_tipo = ttk.Entry(self.frm_manut)
        self.txb_data = ttk.Entry(self.frm_manut)
        self.txb_tecn = ttk.Entry(self.frm_manut)
        self.txb_obs = ttk.Entry(self.frm_manut)

        #Janela scroll
        self.txb_lista_multimetros = ScrolledText(self.frm_busca)
        self.txb_lista_manut = ScrolledText(self.frm_manut)

        #Configura o tamanho (em caracteres) da caixa de texto
        self.txb_lista_multimetros.configure(width= 120, height= 10)
        self.txb_lista_manut.configure(width= 120, height= 10)

        #Montagem
            #Labels
        self.lbl_busca.pack()
        self.frm_busca.pack(fill= 'both', expand= True)
        ttk.Label(self.frm_busca, text= 'id').grid(row= 0, column= 0)
        ttk.Label(self.frm_busca, text= 'Marca').grid(row= 1, column= 0)
        ttk.Label(self.frm_busca, text= 'Modelo').grid(row= 2, column= 0)
        ttk.Label(self.frm_busca, text= 'Disponibilidade').grid(row= 3, column= 0)
        ttk.Label(self.frm_busca, text= 'Observações').grid(row= 4, column= 0)
        ttk.Label(self.frm_busca, text= 'Patrimônio').grid(row= 5, column= 0)
        ttk.Label(self.frm_busca, text= 'Buscar multímetro (id)').grid(row= 0, column= 3)
        ttk.Label(self.frm_busca, text= 'Buscar Patrimônio').grid(row= 1, column= 3)

        self.lbl_manut.pack()
        self.frm_manut.pack(fill= 'both', expand= True)
        ttk.Label(self.frm_manut, text= 'id de manutenção').grid(row= 0, column= 0)
        ttk.Label(self.frm_manut, text= 'id do multímetro').grid(row= 1, column= 0)
        ttk.Label(self.frm_manut, text= 'Data').grid(row= 2, column= 0)
        ttk.Label(self.frm_manut, text= 'Tipo').grid(row= 3, column= 0)
        ttk.Label(self.frm_manut, text= 'Técnico').grid(row= 4, column= 0)
        ttk.Label(self.frm_manut, text= 'Observações').grid(row= 5, column= 0)

            #Entrada de dados pelo usuário - Multímetros
        self.txb_id.grid(row= 0, column= 1)
        self.txb_marca.grid(row= 1, column= 1)
        self.txb_modelo.grid(row= 2, column= 1)
        self.cmb_disponibilidade.grid(row= 3, column= 1)
        self.txb_observacoes.grid(row= 4, column= 1)
        self.txb_pat.grid(row= 5, column= 1)
        self.txb_buscar.grid(row=0, column=4)
        self.txb_buscar_pat.grid(row=1, column=4)
    
            #Entrada de dados pelo usuário - Manutenções
        self.txb_manut_id.grid(row= 0, column= 1)
        self.txb_mult_id.grid(row= 1, column= 1)
        self.txb_data.grid(row= 2, column= 1)
        self.txb_tipo.grid(row= 3, column= 1)
        self.txb_tecn.grid(row= 4, column= 1)
        self.txb_obs.grid(row= 5, column= 1)

            #Botões de ação - Multímetros
        ttk.Button(self.frm_busca, text= 'Inserir', command= self.acao_inserir_multimetro).grid(row= 0, column= 2, rowspan= 1, sticky= 'ns')
        ttk.Button(self.frm_busca, text= 'Remover', command= self.acao_remover_multimetros).grid(row= 1, column= 2, rowspan= 1, sticky= 'ns')
        ttk.Button(self.frm_busca, text= 'Listar', command= self.acao_listar_multimetros).grid(row= 2, column= 2)
        ttk.Button(self.frm_busca, text= 'Listar Disp.', command= self.acao_listar_multimetros_disponiveis).grid(row= 3, column= 2)
        ttk.Button(self.frm_busca, text= 'Atualizar status', command= self.acao_atualizar_status).grid(row= 4, column= 2)
        ttk.Button(self.frm_busca, text= 'Buscar', command= self.acao_buscar_multimetro).grid(row= 0, column= 5)
        ttk.Button(self.frm_busca, text= 'Buscar', command= self.acao_buscar_pat).grid(row= 1, column= 5)
        self.txb_lista_multimetros.grid(row= 7, column= 0, columnspan= 10, sticky= 'news')

            #Botões de ação - Manutenções
        ttk.Button(self.frm_manut, text= 'Inserir', command= self.acao_inserir_manutencao).grid(row= 0, column= 2, rowspan= 1, sticky= 'ns')
        ttk.Button(self.frm_manut, text= 'Remover', command= self.acao_remover_manutencao).grid(row= 1, column= 2, rowspan= 1, sticky= 'ns')
        ttk.Button(self.frm_manut, text= 'Listar', command= self.acao_listar_manutencao).grid(row= 2, column= 2)
        self.txb_lista_manut.grid(row= 6, column= 0, columnspan= 10, sticky= 'news')
        
    def acao_inserir_multimetro(self):
        conexao = Conexao_bd()
        try:
            #Acessa o método para inserção de um novo documento na coleção multimetros
            conexao.inserir_multimetro(id= int(self.txb_id.get()),
                                    marca=self.txb_marca.get(),
                                    modelo=self.txb_modelo.get(),
                                    status=self.cmb_disponibilidade.get(),
                                    observacoes=self.txb_observacoes.get(),
                                    patrimonio=self.txb_pat.get())
            messagebox.showinfo('Sucesso', "Registro adicionado com sucesso!!!")
        except:
            messagebox.showerror('Erro', "O registro não pôde ser inserido. Verifique se o código é pré-existente.")

    def acao_atualizar_status(self):
        conexao = Conexao_bd()
        id = int(self.txb_id.get())
        disponibilidade = self.cmb_disponibilidade.get()
        try:
            conexao.atualizar_status(id= id, novo_status=disponibilidade)
            messagebox.showinfo('Sucesso', "Status atualizado!!")
        except:
            messagebox.showerror('Erro', "O registro não pôde ser encontrado")


    def acao_listar_multimetros(self):
        conexao = Conexao_bd()
        #Instrução para remover todo o conteúdo de texto da ferramenta
        self.txb_lista_multimetros.delete(1.0, 'end')
        #Instrução para inserir texto na ferramenta
        for registro in conexao.todos_multimetros():
            self.txb_lista_multimetros.insert('end', f"{registro['_id']} - {registro['marca']} {registro['modelo']} | Status: {registro['status']} | Obs: {registro['observacoes']}\n")

    def acao_listar_multimetros_disponiveis(self):
        conexao = Conexao_bd()
        #Instrução para remover todo o conteúdo de texto da ferramenta
        self.txb_lista_multimetros.delete(1.0, 'end')
        #Instrução para inserir texto na ferramenta
        for registro in conexao.multimetros_disponiveis():
            self.txb_lista_multimetros.insert('end', f"{registro['_id']} - {registro['patrimonio']} {registro['marca']} {registro['modelo']} | Status: {registro['status']} | Obs: {registro['observacoes']}\n")

    def acao_remover_multimetros(self):
        conexao = Conexao_bd()
        conexao.remover_multimetros(int(self.txb_id.get()))
        messagebox.showinfo('Remoção', 'Multímetro removido (se existia).')

    def acao_buscar_multimetro(self):
        conexao = Conexao_bd()
        self.txb_lista_multimetros.delete(1.0, 'end')
        id = self.txb_buscar.get()
        registro = conexao.buscar_multimetro(id= int(id))
        if registro:
            self.txb_lista_multimetros.insert('end', f"{registro['_id']} - {registro['marca']} {registro['modelo']} | Status: {registro['status']} | Obs: {registro['observacoes']}\n")
        else:
            self.txb_lista_multimetros.insert('end', "Multímetro não encontrado")

    def acao_buscar_pat(self):
        conexao = Conexao_bd()
        self.txb_lista_multimetros.delete(1.0, 'end')
        patrimonio = self.txb_buscar_pat.get()
        registro = conexao.buscar_pat(patrimonio= str(patrimonio))
        if registro:
            self.txb_lista_multimetros.insert('end', f"{registro['_id']} - {registro['marca']} {registro['modelo']} |Status: {registro['status']} | Obs: {registro['observacoes']}\n")
        else:
            self.txb_lista_multimetros.insert('end', "Multímetro não encontrado")

    def acao_inserir_manutencao(self):
        conexao = Conexao_bd()
        try:
            #Acessa o método para inserção de um novo documento na coleção multimetros
            conexao.inserir_manutencao(
                                    manut_id=int(self.txb_manut_id.get()),
                                    mult_id= int(self.txb_mult_id.get()),
                                    tipo= self.txb_tipo.get(),
                                    data= self.txb_data.get(),
                                    tecnico= self.txb_tecn.get(),
                                    observacao= self.txb_obs.get())
            #Atualizar status do multímetro pra indisponível toda vez que adicionar uma manutenção
            conexao.atualizar_status(id=int(self.txb_mult_id.get()),novo_status="Indisponível")
            messagebox.showinfo('Sucesso', "Registro adicionado com sucesso!!!")
        except:
            messagebox.showerror('Erro', "O registro não pôde ser inserido. Verifique se o código é pré-existente.")

    def acao_listar_manutencao(self):
        conexao = Conexao_bd()
        #Instrução para remover todo o conteúdo de texto da ferramenta
        self.txb_lista_manut.delete(1.0, 'end')
        #Instrução para inserir texto na ferramenta
        for registro in conexao.todas_manutencoes():
            self.txb_lista_manut.insert('end', f" Id de Manunteção: {registro['_id']} | Id do Multímetro: {registro['multimetro_id']} | Tipo: {registro['tipo']} | Data: {registro['data']} | Técnico: {registro['tecnico']} | Obs: {registro['observacao']}\n")

    def acao_remover_manutencao(self):
        conexao = Conexao_bd()
        conexao.remover_manutencao(int(self.txb_manut_id.get()))
        messagebox.showinfo('Remoção', 'Manutenção removida (se existia).')

if __name__ == '__main__':
    janela = tk.Tk()
    janela.title("Gerenciar Multímetros")
    Aplicativo(janela)
    janela.mainloop()