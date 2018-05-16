from tkinter import *
import time
# import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
import os
from tkinter import messagebox
import datetime

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
                                "Sexo: " + resposta[3] + "\n"+
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
    if message.topic == "software/ListarTodos/validacao/Serv2Sw":
        info = open("ListaAlunos.txt", "w")
        info.write("*************************************************\n############ Lista de Todos os Alunos ###########\n*************************************************\n")
        info.write("Data: " + str(datetime.date.today()) + "\n")
        info.write("------------------------------------------------\n")
        info.write("|     NOME          |     CPF     |    SEXO     |\n")
        info.write("------------------------------------------------\n")

        dados = message.payload.decode("utf-8")
        if dados == "":
            info.write("\n    Banco de Dados Vazio    \n")
        else:
            alunos = (str(dados).split("?"))
            alunos.pop()

            for row in alunos:
                dados_alunos = row.split("$")
                info.write("| " + dados_alunos[0] + (18 - len(dados_alunos[0])) * " " + "| "
                           + dados_alunos[1] + (12 - len(dados_alunos[1])) * " " + "| "
                           + dados_alunos[2] + (12 - len(dados_alunos[2])) * " " + "|\n")
                info.write("------------------------------------------------\n")

        info.close()

# Adicao de Alunos
def SalvarDados():
    print("Salvando Dados 2")
    print(e1.get())
    print(e2.get())
    print(e3.get())
    print(e4.get())



    nome = e1.get()
    cpf = "".join([str(s) for s in list(e2.get()) if s.isdigit()]) #Aceitando cpfs com "." e "-"
    senha = e3.get()
    sexo = e4.get()

    if sexo == "M" or sexo == "F":
        if sexo == "M":
            sexo="Masculino"
        else:
            sexo="Feminino"

        if cpfcnpj.validate(cpf) and len(senha) == 4:
            print("Senha com tamanho certo")
            msg = str(nome) + "%" + str(cpf) + "%" + str(sexo) + "%" + str(senha)  # Message sended in Mqtt protocol

            client.publish("software/Add/validacao/Sw2Serv", msg)
            client.loop_start()
            time.sleep(0.5)
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e1.focus_set()
            print(msg)

    else:
        print("Dados Incorrentos")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()
        messagebox.showwarning("Erro", "Dados Inválidos")
def AddAluno():
    TelaAddAlunos = Tk()
    TelaAddAlunos.title('Adicionar Alunos')
    TelaAddAlunos.geometry('400x200')
    Label(TelaAddAlunos, text="Nome:").grid(row=0, sticky=E)
    Label(TelaAddAlunos, text="CPF:").grid(row=1, sticky=E)
    Label(TelaAddAlunos, text="Senha:").grid(row=2, sticky=E)
    Label(TelaAddAlunos, text="Sexo (M ou F):").grid(row=3, sticky=E)

    # Nome
    global e1
    e1 = Entry(TelaAddAlunos)
    # Cpf
    global e2
    e2 = Entry(TelaAddAlunos)
    # Senha
    global e3
    e3 = Entry(TelaAddAlunos, show="*")
    # Sexo
    global e4
    e4 = Entry(TelaAddAlunos)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)


    e1.focus_set()
    Button(TelaAddAlunos, text='Adicionar', command=SalvarDados).grid(row=7, column=1, sticky=W, pady=4)
    mainloop()
# Mudança da Senha
def AlterarSenha():
    print("Alterando a senha")
    print(e4.get())
    print(e5.get())
    print(e6.get())

    cpf = "".join([str(s) for s in list(e4.get()) if s.isdigit()]) #Aceitando cpfs com "." e "-"
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
        e4.focus_set()
        # messagebox.showinfo("Informação", "Senha Alterada com sucesso!")
    else:
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e4.focus_set()
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
    Label(TelaMudancaSenha, text="CPF:").grid(row=0, sticky=E)
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

    cpf = "".join([str(s) for s in list(e7.get()) if s.isdigit()])  # Aceitando cpfs com "." e "-"
    if cpfcnpj.validate(cpf):
        print(e7.get())
        msg = cpf
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
    cpf = "".join([str(s) for s in list(e8.get()) if s.isdigit()])
    if cpfcnpj.validate(cpf):
        # Mandar uma msg mqtt com o cpf e escutar a resposta
        print(cpf)
        if messagebox.askyesno("Alerta", "Deseja realmente apagar o aluno com CPF: "+ str(cpf)+ " ?"):
            msg = cpf
            client.publish("software/Apagar/validacao/Sw2Serv", msg)
            client.loop_start()
            e8.delete(0, END)
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
    TelaApagarAluno.geometry('500x250')
    Label(TelaApagarAluno, text="Digite o CPF do aluno desejado:").grid(row=0, sticky=E)
    # CPF
    global e8
    e8 = Entry(TelaApagarAluno)
    e8.grid(row=0, column=1)
    e8.focus_set()
    Button(TelaApagarAluno, text="Apagar", command=Apagar).grid(row=3, column=1, sticky=W, pady=2)
    mainloop()
# Listar Todos os Alunos
def ListarAlunos():
    print("Listando Alunos")
    client.publish("software/ListarTodos/validacao/Sw2Serv", "Listar")
    client.loop_start()

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
client.connect("192.168.1.2", 5050)
# client.connect("192.168.1.2", 5050)
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
client.subscribe("software/Trocar/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Sw2Serv")
client.subscribe("software/Apagar/validacao/Serv2Sw")
client.subscribe("software/Apagar/validacao/Sw2Serv")
client.subscribe("software/ListarTodos/validacao/Serv2Sw")

telaPrincipalLabel.mainloop()
