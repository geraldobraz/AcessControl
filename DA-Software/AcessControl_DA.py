from tkinter import *
import time
import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
from tkinter import messagebox
import datetime


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))
    # Add Student
    if message.topic == "software/Add/validacao/Serv2Sw":
        if message.payload.decode("utf-8") == "Valido":
            messagebox.showinfo("Informação", "Aluno adicionado com sucesso!")
        if message.payload.decode("utf-8") == "Nao Valido":
            messagebox.showwarning("Erro", "Esse CPF já foi cadastrado")
    # Change Password
    if message.topic == "software/Trocar/validacao/Serv2Sw":
        if message.payload.decode("utf-8") == "Valido":
            messagebox.showinfo("Informação", "Senha Alterada com sucesso!")
        if message.payload.decode("utf-8") == "Nao Valido":
            messagebox.showwarning("Erro", "Dados Inválidos")
    # Search Student
    if message.topic == "software/Procura/validacao/Serv2Sw":
        resposta = str(message.payload.decode("utf-8")).split("$")
        if resposta[0] == "Valido":
            messagebox.showinfo("Dados de " + resposta[1],
                                "**********************\n"+"Nome: " + resposta[1] + "\n" +
                                "CPF: " + resposta[2] + "\n" +
                                "Sexo: " + resposta[3] + "\n"+
                                "**********************\n")

        if resposta[0] == "Nao Valido":
            messagebox.showwarning("Erro", "Esse Aluno não está cadastrado!")
    # Delete Student
    if message.topic == "software/Apagar/validacao/Serv2Sw":
        if message.payload.decode("utf-8") == "Valido":
            messagebox.showwarning("Aviso", "Aluno Apagado com Sucesso!")
        if message.payload.decode("utf-8") == "Nao Valido":
            messagebox.showwarning("Erro", "Dados Inválidos")
    # List all Students
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


# Functions *************************************************************************************************************************
# Add Students
def addStudent():
    name = e1.get()
    cpf = "".join([str(s) for s in list(e2.get()) if s.isdigit()])
    password = e3.get()
    gender = e4.get()

    if name and cpf and password and gender and (gender == "M" or gender == "F"):
        if gender == "M":
            gender="Masculino"
        else:
            gender="Feminino"

        if cpfcnpj.validate(cpf) and len(password) == 4:
            msg = str(name) + "%" + str(cpf) + "%" + str(gender) + "%" + str(password)
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
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e1.focus_set()
            messagebox.showwarning("Erro", "Dados Inválidos")

    else:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()
        messagebox.showwarning("Erro", "Dados Incompletos")
def addStudentDisplay():
    TelaAddAlunos = Tk()
    TelaAddAlunos.title('Adicionar Alunos')
    TelaAddAlunos.geometry('400x200')
    Label(TelaAddAlunos, text="Nome:").grid(row=0, sticky=E)
    Label(TelaAddAlunos, text="CPF:").grid(row=1, sticky=E)
    Label(TelaAddAlunos, text="Senha:").grid(row=2, sticky=E)
    Label(TelaAddAlunos, text="Sexo (M ou F):").grid(row=3, sticky=E)

    # Name
    global e1
    e1 = Entry(TelaAddAlunos)
    # Cpf
    global e2
    e2 = Entry(TelaAddAlunos)
    # Password
    global e3
    e3 = Entry(TelaAddAlunos, show="*")
    # Gender
    global e4
    e4 = Entry(TelaAddAlunos)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e1.focus_set()
    Button(TelaAddAlunos, text='Adicionar', command=addStudent).grid(row=7, column=1, sticky=W, pady=4)
    mainloop()
# Change Password
def changePassword():
    cpf = "".join([str(s) for s in list(e4.get()) if s.isdigit()])
    password1 = e5.get()
    password2 = e6.get()
    if password1 and password2 and cpf:
        if password1 == password2 and cpfcnpj.validate(cpf) and len(password1) == 4:
            print("Válido")
            msg = str(cpf) + "%" + str(password1)
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
    else:
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e4.focus_set()
        messagebox.showwarning("Erro", "Dados Incompletos")
def changePasswordDisplay():
    TelaMudancaSenha = Tk()
    TelaMudancaSenha.title("Mudar Senha")
    TelaMudancaSenha.geometry('400x200')
    Label(TelaMudancaSenha, text="CPF:").grid(row=0, sticky=E)
    Label(TelaMudancaSenha, text="Nova Senha:").grid(row=1, sticky=E)
    Label(TelaMudancaSenha, text="Digite novamente a Senha:").grid(row=2, sticky=E)
    # CPF
    global e4
    e4 = Entry(TelaMudancaSenha)
    # password1
    global e5
    e5 = Entry(TelaMudancaSenha, show="*")
    # password2
    global e6
    e6 = Entry(TelaMudancaSenha, show="*")
    e4.grid(row=0, column=1)
    e5.grid(row=1, column=1)
    e6.grid(row=2, column=1)
    e4.focus_set()
    Button(TelaMudancaSenha, text='Mudar Senha', command=changePassword).grid(row=3, column=1, sticky=W, pady=4)
    mainloop()
# Search Student
def searchStudent():
    cpf = "".join([str(s) for s in list(e7.get()) if s.isdigit()])
    if cpfcnpj.validate(cpf):
        client.publish("software/Procura/validacao/Sw2Serv", cpf)
        client.loop_start()
    else:
        messagebox.showwarning("Erro", "Cpf Inválido!")
        e7.delete(0, END)
def searchStudentDisplay():
    TelaProcuraAluno = Tk()
    TelaProcuraAluno.title("Procura de Alunos")
    TelaProcuraAluno.geometry('500x250')
    Label(TelaProcuraAluno, text="Digite o CPF do aluno desejado:").grid(row=0, sticky=E)
    # cpf
    global e7
    e7 = Entry(TelaProcuraAluno)
    e7.grid(row=0, column=1)
    e7.focus_set()
    Button(TelaProcuraAluno, text="Procurar", command=searchStudent).grid(row=3, column=1, sticky=W, pady=2)
    mainloop()
# Delete Student
def deleteStudent():
    cpf = "".join([str(s) for s in list(e8.get()) if s.isdigit()])
    if cpfcnpj.validate(cpf):
        if messagebox.askyesno("Alerta", "Deseja realmente apagar o aluno com CPF: "+ str(cpf)+ " ?"):
            client.publish("software/Apagar/validacao/Sw2Serv", cpf)
            client.loop_start()
            e8.delete(0, END)
        else:
            pass
    else:
        messagebox.showwarning("Erro", "Dados Inválidos")
        e8.delete(0, END)
def deleteStudentDisplay():
    TelaApagarAluno = Tk()
    TelaApagarAluno.title("Apagar Alunos")
    TelaApagarAluno.geometry('500x250')
    Label(TelaApagarAluno, text="Digite o CPF do aluno desejado:").grid(row=0, sticky=E)
    # CPF
    global e8
    e8 = Entry(TelaApagarAluno)
    e8.grid(row=0, column=1)
    e8.focus_set()
    Button(TelaApagarAluno, text="Apagar", command=deleteStudent).grid(row=3, column=1, sticky=W, pady=2)
    mainloop()
# Listar Todos os Alunos
def listStudents():
    client.publish("software/ListarTodos/validacao/Sw2Serv", "Listar")
    client.loop_start()

# Home Configuration ****************************************************************************************************************
TelaPrincipal = Tk()
TelaPrincipal.title('Tela Principal')
TelaPrincipal.geometry('500x300')
telaPrincipalLabel = Label(TelaPrincipal, height=2, text="Selecione o que deseja fazer:", font="Arial 22 normal")

telaPrincipalLabel.grid(row=0, column=0, sticky=E)

addStudentButton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Adicionar Alunos        ",
                          command=addStudentDisplay)
changePasswordButton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Mudar Senha             ",
                              command=changePasswordDisplay)
searchStudentButton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Procurar Aluno           ",
                             command=searchStudentDisplay)
deleteStudentButton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Apagar Aluno             ",
                             command=deleteStudentDisplay)
listAllStudentsButton = Button(TelaPrincipal, height=1, font="Arial 20 normal", text="Listar todos os Alunos",
                               command=listStudents)

addStudentButton.grid(row=1, column=0, sticky=W)
changePasswordButton.grid(row=2, column=0, sticky=W)
searchStudentButton.grid(row=3, column=0, sticky=W)
deleteStudentButton.grid(row=4, column=0, sticky=W)
listAllStudentsButton.grid(row=5, column=0, sticky=W)

# MQTT Connection *****************************************************************************************************************
client = mqtt.Client("Software DA")
client.on_message = on_message
client.connect("192.168.1.3", 5050)


# MQTT Subscribe *******************************************************************************************************************
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
client.subscribe("software/Trocar/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Serv2Sw")
client.subscribe("software/Procura/validacao/Sw2Serv")
client.subscribe("software/Apagar/validacao/Serv2Sw")
client.subscribe("software/Apagar/validacao/Sw2Serv")
client.subscribe("software/ListarTodos/validacao/Serv2Sw")

telaPrincipalLabel.mainloop()
