from tkinter import *
import time
import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
import os


creds = 'tempfile.temp'  # This just sets the variable creds to 'tempfile.temp'


def Signup():  # This is the signup definition,
    global pwordE  # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global roots

    roots = Tk()  # This creates the window, just a blank one.
    roots.title('Signup')  # This renames the title of said window to 'signup'
    intruction = Label(roots,
                       text='Please Enter new Credidentials\n')  # This puts a label, so just a piece of text saying 'please enter blah'
    intruction.grid(row=0, column=0,
                    sticky=E)  # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)

    nameL = Label(roots, text='New Username: ')  # This just does the same as above, instead with the text new username.
    pwordL = Label(roots, text='New Password: ')  # ^^
    nameL.grid(row=1, column=0,
               sticky=W)  # Same thing as the instruction var just on different rows. :) Tkinter is like that.
    pwordL.grid(row=2, column=0, sticky=W)  # ^^

    nameE = Entry(roots)  # This now puts a text box waiting for input.
    pwordE = Entry(roots,
                   show='*')  # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    nameE.grid(row=1, column=1)  # You know what this does now :D
    pwordE.grid(row=2, column=1)  # ^^

    signupButton = Button(roots, text='Signup',
                          command=FSSignup)  # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(columnspan=2, sticky=W)
    roots.mainloop()  # This just makes the window keep open, we will destroy it soon


def FSSignup():
    with open(creds, 'w') as f:  # Creates a document using the variable we made at the top.
        f.write(
            nameE.get())  # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
        f.write('\n')  # Splits the line so both variables are on different lines.
        f.write(pwordE.get())  # Same as nameE just with pword var
        f.close()  # Closes the file

    roots.destroy()  # This will destroy the signup window. :)
    Login()  # This will move us onto the login definition :D


def Login():
    global nameEL
    global pwordEL  # More globals :D
    global rootA

    rootA = Tk()  # This now makes a new window.
    rootA.title('Login')  # This makes the window title 'login'

    intruction = Label(rootA, text='Please Login\n')  # More labels to tell us what they do
    intruction.grid(sticky=E)  # Blahdy Blah

    nameL = Label(rootA, text='Username: ')  # More labels
    pwordL = Label(rootA, text='Password: ')  # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)

    nameEL = Entry(rootA)  # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)

    loginB = Button(rootA, text='Login',
                    command=CheckLogin)  # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)

    rmuser = Button(rootA, text='Delete User', fg='red',
                    command=DelUser)  # This makes the deluser button. blah go to the deluser def.
    rmuser.grid(columnspan=2, sticky=W)
    rootA.mainloop()


def CheckLogin():
    with open(creds) as f:
        data = f.readlines()  # This takes the entire document we put the info into and puts it into the data variable
        uname = data[0].rstrip()  # Data[0], 0 is the first line, 1 is the second and so on.
        pword = data[1].rstrip()  # Using .rstrip() will remove the \n (new line) word from before when we input it

    if nameEL.get() == uname and pwordEL.get() == pword:  # Checks to see if you entered the correct data.
        r = Tk()  # Opens new window
        r.title(':D')
        r.geometry('150x50')  # Makes the window a certain size
        rlbl = Label(r, text='\n[+] Logged In')  # "logged in" label
        rlbl.pack()  # Pack is like .grid(), just different
        r.mainloop()
    else:
        r = Tk()
        r.title('D:')
        r.geometry('150x50')
        rlbl = Label(r, text='\n[!] Invalid Login')
        rlbl.pack()
        r.mainloop()


def DelUser():
    os.remove(creds)  # Removes the file
    rootA.destroy()  # Destroys the login window
    Signup()  # And goes back to the start!


# Main
# TODO
'''
Essa eh a parte do main vamos criar uma tela em branco cheia de botoes!
Cada botao deve levar a uma nova tela:
- Add Novos alunos -- Fazendo! 
- Mudar Senha
- Procurar Aluno
- Apagar aluno
- Listar todos os alunos

-Links
- https://www.python-course.eu/tkinter_entry_widgets.php
- http://effbot.org/tkinterbook/entry.htm
'''
# todo: Fazer pegar as funcoes q eu fiz em linha de comando

def EnviarDados():
    print("Enviando os dados...")
    print(e1.get())
    print(e2.get())
    print(e3.get())


    nome = e1.get()
    cpf = e2.get()
    senha = e3.get()
    if(cpfcnpj.validate(cpf)):
        print("Cpf validado")
        # time.sleep(0.5)

        if True: #         FIXME: Validar o cpf no BD
            print("Cpf nao existe no BD")
            if len(senha)== 4:
                print("Senha com tamanho certo")
                msg = str(nome) + "%" + str(cpf) + "%" + "Sexo" + "%" + str(
                senha)  # Message sended in Mqtt protocol
                # client.publish("software/Add_Aluno",msg)
                print(msg)
            else:
                print("Tamanho da Senha errado")
        else:
            print("Cpf ja existe no BD")
    else:
        e1.delete(0, END)
        # TODO: Deletar os dados dos campos

        print("Cpf nao é valido")
# TODO: Mostrar uma msg para o usuario falando que ocorreu um erro!
def AddAluno():
    TelaAddAlunos = Tk()
    TelaAddAlunos.title('Adicionar Alunos')
    TelaAddAlunos.geometry('400x200')
    Label(TelaAddAlunos,text="Nome:").grid(row=0)
    Label(TelaAddAlunos,text="CPF:").grid(row=1)
    Label(TelaAddAlunos,text="Senha:").grid(row=2)
    #Nome
    global e1
    e1 = Entry(TelaAddAlunos)
    #Cpf
    global e2
    e2 = Entry(TelaAddAlunos)
    # Senha
    global  e3
    e3 = Entry(TelaAddAlunos)
    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    e3.grid(row=2,column=1)
    Button(TelaAddAlunos, text='Adicionar', command=EnviarDados).grid(row=3, column=1, sticky=W, pady=4)
    mainloop()


# effbot.org/tkinterbook/grid.htm
TelaPrincipal = Tk()
TelaPrincipal.title('Tela Principal')
TelaPrincipal.geometry('500x300')
telaPrincipalLabel = Label(TelaPrincipal, height=2, text="Selecione o que deseja fazer:", font="Arial 22 normal")
# telaPrincipalLabel.grid(row= 0, column = 0 )
telaPrincipalLabel.grid(row=0, column=0, sticky=E)

# Tela Inicial
AddAlunosbutton = Button(TelaPrincipal,height=1,font = "Arial 20 normal",text=   "Adicionar Alunos        ",command = AddAluno)
MudarSenahbutton = Button(TelaPrincipal,height=1,font = "Arial 20 normal", text= "Mudar Senha             ",command = AddAluno)
ProcurarAlunobutton = Button(TelaPrincipal,height=1,font ="Arial 20 normal",text="Procurar Aluno           ",command = AddAluno)
ApagarAlunobutton = Button(TelaPrincipal,height=1, font = "Arial 20 normal",text="Apagar Aluno             ",command = AddAluno)
ListarTodosbutton = Button(TelaPrincipal,height=1,font = "Arial 20 normal", text="Listar todos os Alunos",command = AddAluno)


AddAlunosbutton.grid(row=1, column=0,sticky=W)
MudarSenahbutton.grid(row=2, column=0,sticky=W)
ProcurarAlunobutton.grid(row=3, column=0,sticky=W)
ApagarAlunobutton.grid(row=4, column=0,sticky=W)
ListarTodosbutton.grid(row=5, column=0,sticky=W)

telaPrincipalLabel.mainloop()






# if os.path.isfile(creds):
#     Login()
# else:  # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
#     Signup()