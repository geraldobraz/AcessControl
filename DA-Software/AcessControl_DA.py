from tkinter import *
import time
# import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
import os
from tkinter import messagebox

# TODO
'''
Essa eh a parte do main vamos criar uma tela em branco cheia de botoes!
Cada botao deve levar a uma nova tela:
- Add Novos alunos -- OK! 
- Mudar Senha -- OK!
- Procurar Aluno -- OK!
- Apagar aluno -- OK!
- Listar todos os alunos -- OK!
-Links
- https://www.python-course.eu/tkinter_entry_widgets.php
- http://effbot.org/tkinterbook/entry.htm
- https://www.youtube.com/watch?v=JcFZl75WPUA
>> MQTT
    > Topicos
        >Adicionar Alunos
        - software/Add/validacao/cpf
        - software/Add/nome
        - software/Add/cpf
        - software/Add/senha
        - software/Add/sexo
tati : 10121975495
'''


# TODO: Fazer pegar as funcoes q eu fiz em linha de comando

# ON Message
# Tratando os dados recebidos por MQTT


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))
    # Adicinar Aluno
    if message.topic == "software/Add/validacao/Serv2Sw":
        # Recebeu Confirmacao que o cpf nao esta no BD
        print("Entrou 1")
        if message.payload.decode("utf-8") == "Valido":
            print("Entrou 2")
            messagebox.showinfo("Informação", "Aluno adicionado com sucesso!")

            # e1.delete(0,END)
            # e1.delete(0, END)
            # e2.delete(0, END)
            # e3.delete(0, END)
            # messagebox.showinfo("Informação", "Aluno adicionado com sucesso!")

        if message.payload.decode("utf-8") == "Nao Valido":
            # e1.delete(0, END)
            # e2.delete(0, END)
            # e3.delete(0, END)
            messagebox.showwarning("Erro", "Esse CPF já foi cadastrado")
    # Trocar Senha
    if message.topic == "software/Trocar/validacao/Serv2Sw":
        print("Entrou 1")
        if message.payload.decode("utf-8") == "Valido":
            print("Entrou 2")
            # e4.delete(0, END)
            # e5.delete(0, END)
            # e6.delete(0, END)
            messagebox.showinfo("Informação", "Senha Alterada com sucesso!")
        if message.payload.decode("utf-8") == "Nao Valido":
            # e4.delete(0, END)
            # e5.delete(0, END)
            # e6.delete(0, END)
            messagebox.showwarning("Erro", "Dados Inválidos")
    # Procurar Aluno
    if message.topic == "software/Procura/validacao/Serv2Sw":
        print("!!!Recebeu!!!")
        resposta = str(message.payload.decode("utf-8")).split("$")
        # print(">>" + resposta[0])

        if resposta[0] == "Valido":
            print("Valido")
            messagebox.showinfo("Dados de " + resposta[1],
                                "**********************\n"+"Nome: " + resposta[1] + "\n" +
                                "CPF: " + resposta[2] + "\n" +
                                "Senha: " + resposta[3] + "\n"+
                                "**********************\n")
            # e7.delete(0, END)

        if resposta[0] == "Nao Valido":
            print("Nao valido")
            messagebox.showwarning("Erro", "Esse Aluno não está cadastrado!")
            # e7.delete(0, END)
    # Apagar Aluno
    if message.topic == "software/Apagar/validacao/Serv2Sw":
        if message.payload.decode("utf-8") == "Valido":
            print("Apagou")
            # e8.delete(0, END)
        if message.payload.decode("utf-8") == "Nao Valido":
            # e8.delete(0, END)
            messagebox.showwarning("Erro", "Dados Inválidos")
    # Listar todos os alunos
    if message.topic == "software/Listar/validacao/Serv2Sw":
        if message.payload.decode("utf-8") == "Valido":
            e8.delete(0, END)
        # TODO: Criar uma nova pagina com uma lista dos alunos!
        if message.payload.decode("utf-8") == "Nao Valido":
            e8.delete(0, END)
            messagebox.showwarning("Erro", "Dados Inválidos")


# *****************************************************************************

# Adicao de Alunos
def SalvarDados():
    print("Salvando Dados 2")
    print(e1.get())
    print(e2.get())
    print(e3.get())

    nome = e1.get()
    cpf = e2.get()
    senha = e3.get()

    if cpfcnpj.validate(cpf) and len(senha) == 4:
        print("Senha com tamanho certo")
        # msg = str(nome) + "%" + str(cpf) + "%" + "Sexo" + "%" + str(senha)  # Message sended in Mqtt protocol
        msg = str(nome) + "%" + str(cpf) + "%" + str(senha)  # Message sended in Mqtt protocol
        # client.publish("software/Add_Aluno",msg)
        client.publish("software/Add/validacao/Sw2Serv", msg)
        client.loop_start()
        time.sleep(0.5)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        print(msg)
    else:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        messagebox.showwarning("Erro", "Dados Inválidos")

        print("Dados inválidos")
def AddAluno():
    TelaAddAlunos = Tk()
    TelaAddAlunos.title('Adicionar Alunos')
    TelaAddAlunos.geometry('400x200')
    Label(TelaAddAlunos, text="Nome:").grid(row=0, sticky=E)
    Label(TelaAddAlunos, text="CPF(Só números):").grid(row=1, sticky=E)
    Label(TelaAddAlunos, text="Senha:").grid(row=2, sticky=E)

    # Nome
    global e1
    e1 = Entry(TelaAddAlunos)
    # Cpf
    global e2
    e2 = Entry(TelaAddAlunos)
    # Senha
    global e3
    e3 = Entry(TelaAddAlunos, show="*")
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e1.focus_set()
    # Radio Button
    # Masculino = Radiobutton(TelaAddAlunos,text="Masculino",value=1,variable=teste,command=SelecSexo).grid(row=3,column=1) #FIXME!
    # Feminino = Radiobutton(TelaAddAlunos,text="Feminino",value=2,variable=teste).grid(row=3,column=2)

    Button(TelaAddAlunos, text='Adicionar', command=SalvarDados).grid(row=6, column=1, sticky=W, pady=4)  # row=3
    mainloop()
# Mudança da Senha
def AlterarSenha():
    print("Alterando a senha")
    print(e4.get())
    print(e5.get())
    print(e6.get())

    cpf = e4.get()
    senha_1 = e5.get()
    senha_2 = e6.get()

    if senha_1 == senha_2 and cpfcnpj.validate(cpf) and len(senha_1) == 4:  # FIXME: Lembrar de validar o cpf no BD:
        print("Válido")
        # TODO: Enviar os dados
        msg = str(cpf) + "%" + str(senha_1)
        print(msg)
        client.publish("software/Trocar/validacao/Sw2Serv", msg)
        client.loop_start()
        time.sleep(0.5)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        # messagebox.showinfo("Informação", "Senha Alterada com sucesso!")
    else:
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        messagebox.showwarning("Erro", "Dados Inválidos")
        print("Dado Inválido")
def MudancaSenha():
    print("Mudança de Senha")
    TelaMudancaSenha = Tk()
    '''
    O usuario escreve o cpf dele a senha nova duas vezes e depois confirma! Os dados vao ser enviados para uma func 
    que envia para o bd alterar
    '''
    TelaMudancaSenha.title("Adicionar Alunos")
    TelaMudancaSenha.geometry('400x200')
    Label(TelaMudancaSenha, text="CPF(Só números):").grid(row=0, sticky=E)
    Label(TelaMudancaSenha, text="Nova Senha:").grid(row=1, sticky=E)
    Label(TelaMudancaSenha, text="Digite novamente a Senha:").grid(row=2, sticky=E)
    # CPF
    global e4
    e4 = Entry(TelaMudancaSenha)
    # Senha_1
    global e5
    e5 = Entry(TelaMudancaSenha, show="*")
    # Senha_2
    global e6
    e6 = Entry(TelaMudancaSenha, show="*")
    e4.grid(row=0, column=1)
    e5.grid(row=1, column=1)
    e6.grid(row=2, column=1)
    e4.focus_set()
    Button(TelaMudancaSenha, text='Mudar Senha', command=AlterarSenha).grid(row=3, column=1, sticky=W, pady=4)
    mainloop()
# Procura de Aluno
def Procurar():
    print("Procurando...")

    if cpfcnpj.validate(e7.get()):
        print(e7.get())
        msg = str(e7.get())
        client.publish("software/Procura/validacao/Sw2Serv", msg)
        client.loop_start()
        # e7.delete(0, END)

    #     No onmessage ele deve criar outra tela com as informacoes do estudante
    else:
        print("Dados Inválidos")
        messagebox.showwarning("Erro", "Cpf Inválido!")
        e7.delete(0, END)
def ProcuraAluno():
    print("Procurando Aluno")
    TelaProcuraAluno = Tk()
    TelaProcuraAluno.title("Procura de Alunos")
    TelaProcuraAluno.geometry('500x250')
    Label(TelaProcuraAluno, text="Digite o CPF do aluno desejado:").grid(row=0, sticky=E)
    # CPF
    global e7
    e7 = Entry(TelaProcuraAluno)
    e7.grid(row=0, column=1)
    e7.focus_set()
    Button(TelaProcuraAluno, text="Procurar", command=Procurar).grid(row=3, column=1, sticky=W, pady=2)
    mainloop()
# Apagar Alunos
def Apagar():
    print("Apagando...")
    if cpfcnpj.validate(e8.get()):  # FIXME: Fazer a leitura do Banco de Dados
        # Mandar uma msg mqtt com o cpf e escutar a resposta
        print(e8.get())
        if messagebox.askyesno("Alerta", "Deseja realmente apagar esse aluno?"):
            msg = str(e8.get())
            client.publish("software/Apagar/validacao/Sw2Serv", msg)
            client.loop_start()
            # messagebox.showinfo("Informação", "Aluno apagado com sucesso!")
            # e8.delete(0, END)
        else:
            pass
    else:
        print("Dados Inválidos")
        messagebox.showwarning("Erro", "Dados Inválidos")
        e8.delete(0, END)
def ApagarAluno():
    print("Apagar Aluno")
    TelaApagarAluno = Tk()
    TelaApagarAluno.title("Apagar Alunos")
    TelaApagarAluno.geometry('400x250')
    Label(TelaApagarAluno, text="Digite o CPF do aluno desejado:").grid(row=0, sticky=E)
    # CPF
    global e8
    e8 = Entry(TelaApagarAluno)
    e8.grid(row=0, column=1)
    Button(TelaApagarAluno, text="Apagar", command=Apagar).grid(row=3, column=1, sticky=W, pady=2)
    mainloop()
# Listar Todos os Alunos
def ListarAlunos():
    print("Listando Alunos")
    client.publish("software/Listar/validacao/Sw2Serv", "Listar")


#     TODO: Msg em MQTT dizendo para retornar todos os alunos:


# Tela Inicial
TelaPrincipal = Tk()
TelaPrincipal.title('Tela Principal')
TelaPrincipal.geometry('500x300')
telaPrincipalLabel = Label(TelaPrincipal, height=2, text="Selecione o que deseja fazer:", font="Arial 22 normal")
# telaPrincipalLabel.grid(row= 0, column = 0 )
telaPrincipalLabel.grid(row=0, column=0, sticky=E)

AddAlunosbutton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Adicionar Alunos        ",
                         command=AddAluno)
MudarSenahbutton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Mudar Senha             ",
                          command=MudancaSenha)
ProcurarAlunobutton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Procurar Aluno           ",
                             command=ProcuraAluno)
ApagarAlunobutton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Apagar Aluno             ",
                           command=ApagarAluno)
ListarTodosbutton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Listar todos os Alunos",
                           command=ListarAlunos)

AddAlunosbutton.grid(row=1, column=0, sticky=W)
MudarSenahbutton.grid(row=2, column=0, sticky=W)
ProcurarAlunobutton.grid(row=3, column=0, sticky=W)
ApagarAlunobutton.grid(row=4, column=0, sticky=W)
ListarTodosbutton.grid(row=5, column=0, sticky=W)

# MQTT
client = mqtt.Client("Software DA")
client.on_message = on_message
client.connect("192.168.1.2", 5050)  # todo: Testar com o servidor!
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
client.subscribe("software/Trocar/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Sw2Serv")
client.subscribe("software/Apagar/validacao/Serv2Sw")
client.subscribe("software/Apagar/validacao/Sw2Serv")


telaPrincipalLabel.mainloop()
