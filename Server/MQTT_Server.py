######################################################################
#                              Server                                #
######################################################################

import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
import mysql.connector
import time
import RPi.GPIO as GPIO


# GPIO Setup
LedPin23 = 23
LedPin24 = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(LedPin23 , GPIO.OUT)
GPIO.setup(LedPin24 , GPIO.OUT)
GPIO.output(LedPin23 , False)
GPIO.output(LedPin24 , False)

# Data Base Configuration
cnx = mysql.connector.connect(user='root', password='senha',
                              host='localhost',
                              database='Controle_de_Acesso')

# MySQL Functions
add_Alunos = ("INSERT INTO Alunos "
               "(NOME,CPF,SEXO,SENHA) "
               "VALUES (%s, %s, %s, %s)")

update_senha = ("UPDATE Alunos SET SENHA = %s"
                "WHERE CPF = %s")

select_password  =   ("SELECT SENHA"
                    " FROM Alunos"
                    " WHERE CPF = %(cpf_atual)s")

select_cpf = ("SELECT CPF FROM Alunos ")

select_gender = ("SELECT SEXO "
                "FROM Alunos "
                "WHERE CPF = %(cpf_atual)s")

select_data = ("SELECT NOME,CPF,SEXO "
                "FROM Alunos "
                "WHERE CPF = %(cpf_atual)s")

delete_user = ("DELETE FROM Alunos "
                "WHERE CPF = %(cpf_atual)s")

list_users = ("SELECT NOME, CPF, SEXO FROM Alunos ORDER BY NOME")


# Functions 
def searchPassword(Cpf, password):
    passwordAuth = False
    cursor = cnx.cursor()
    cpf_atual = int(Cpf)
    cursor.execute(select_password, {'cpf_atual': cpf_atual})

    for row in cursor:
        if str(row[0]) == password:
            passwordAuth = True
        else:
            pass
    cursor.close()
    return passwordAuth
def searchCpf(Cpf):
    cpfAuth = False
    cursor = cnx.cursor()
    cursor.execute(select_cpf)
    for row in cursor:
        if (Cpf in row):
            cpfAuth = True
        else:
            pass
    cursor.close()
    return cpfAuth
def searchGender(Cpf):
    cursor = cnx.cursor()
    cpf_atual = int(Cpf)
    cursor.execute(select_gender, {'cpf_atual': cpf_atual})
    for row in cursor:
        if str(row[0]) == "Masculino":
            resposta = "Masc"
        else:
            resposta = "Fem"
    cnx.commit()
    cursor.close()
    return resposta
def searchStudent(Cpf):
    cursor = cnx.cursor()
    cpf_atual = int(Cpf)
    cursor.execute(select_data, {'cpf_atual': cpf_atual})
    data = []
    for row in cursor:
        data = ([row[i] for i in range(0,len(row))])
    data ="$".join(data)
    cnx.commit()
    cursor.close()
    return data
def deleteStudent(Cpf):  
    cursor = cnx.cursor()
    cpf_atual = int(Cpf)
    cursor.execute(delete_user, {'cpf_atual': cpf_atual})
    cnx.commit()
    cursor.close()
def listStudents():
    cursor = cnx.cursor()
    cursor.execute(list_users)
    data = []
    for row in cursor:
        data.append("$".join(row) + "?")
    else:
        pass
    cursor.close()
    return "".join(data)

def on_message(client, userdata, message):
    print ("Message received: " + str(message.payload.decode("utf-8")))
    print ("Topic: " + str (message.topic) )

    # **************** Celular Topics **************************** #
    # Receiving data from cellphones
    if message.topic == "celular/dados":
        data = str(message.payload.decode("utf-8")).split("$")
        if searchCpf(data[0]) and searchPassword(data[0],data[1]):
            client.publish("celular/dados/resposta", searchGender(data[0]))
        else:
            client.publish("celular/dados/resposta", "nao")
    # Open the masculine door
    if message.topic == "celular/porta/Masc":
        print(">>Topic: celular/porta/Masc")
        resp = str(message.payload.decode("utf-8"))
        if message.payload.decode("utf-8") == "ON":
            GPIO.output(LedPin23 , True ) # led on
            time.sleep(0.01)
            GPIO.output(LedPin23 , False) # led off
            print("Open!")
        else:
            pass
    #  Open the feminine door
    if message.topic == "celular/porta/Fem":
        print(">>Topic: celular/porta/Fem")
        resp = str(message.payload.decode("utf-8"))
        if message.payload.decode("utf-8") == "ON":
            GPIO.output(LedPin24 , True ) # led on
            time.sleep(0.01)
            GPIO.output(LedPin24 , False) # led off
            print("Open!")
        else:
            pass
    # **************** Software Topics **************************** #
    # Adding Student
    if message.topic == "software/Add/validacao/Sw2Serv":
        data = str(message.payload.decode("utf-8")).split("%")
        '''Info
            #data[0]: Name #data[1]: CPF #data[2]: gender #data[3]: Password
                                                                         '''
        if not searchCpf(data[1]):
            data_Student = (data[0],data[1],data[2],data[3])
            cursor = cnx.cursor()
            cursor.execute(add_Alunos, data_Student)
            cnx.commit()
            cursor.close()
            client.publish("software/Add/validacao/Serv2Sw","Valido")
            time.sleep(0.5)
        else:
            print ("CPF already exist on data base")
            client.publish("software/Add/validacao/Serv2Sw", "Nao Valido")
    # Changing Password
    if message.topic == "software/Trocar/validacao/Sw2Serv":
        data = str(message.payload.decode("utf-8")).split("%")
        ''' Info
            dado[0]: CPF  dado[1]: New Password
                                            '''
        if searchCpf(data[0]):
            data_Student = (data[1],data[0])
            cursor = cnx.cursor()
            cursor.execute(update_senha, data_Student)
            cnx.commit()
            cursor.close()
            client.publish("software/Trocar/validacao/Serv2Sw","Valido")
            time.sleep(0.5)
        else:
            print ("CPF already exist on data base")
            client.publish("software/Trocar/validacao/Serv2Sw", "Nao Valido")
    # Listing an Especific Student
    if message.topic == "software/Procura/validacao/Sw2Serv":
        data = str(message.payload.decode("utf-8"))
        if searchCpf(data):
            client.publish("software/Procura/validacao/Serv2Sw", "Valido$"+ searchStudent(data))
        else:
            client.publish("software/Procura/validacao/Serv2Sw", "Nao Valido$" + searchStudent(data))
    # Deleting Student
    if message.topic == "software/Apagar/validacao/Sw2Serv":
        data = str(message.payload.decode("utf-8"))
        if searchCpf(data):
            deleteStudent(data)
            client.publish("software/Apagar/validacao/Serv2Sw", "Valido")
        else:
            client.publish("software/Apagar/validacao/Serv2Sw", "Nao Valido")
    # List All Students
    if message.topic == "software/ListarTodos/validacao/Sw2Serv":
        data = str(message.payload.decode("utf-8"))
        if data == "Listar":
            client.publish("software/ListarTodos/validacao/Serv2Sw", listStudents())
            print ("Enviou!",listStudents())

# Creating a new MQTT client
client = mqtt.Client("Raspberry-Server")

client.on_message = on_message

# Connection
client.connect("192.168.1.3", 5050)

# Subscribes
client.subscribe("celular/dados")
client.subscribe("celular/porta/Masc")
client.subscribe("celular/porta/Fem")
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
client.subscribe("software/Trocar/validacao/Sw2Serv")
client.subscribe("software/Procura/validacao/Sw2Serv")
client.subscribe("software/ListarTodos/validacao/Sw2Serv")
client.subscribe("software/Apagar/validacao/Sw2Serv")

client.loop_forever()

