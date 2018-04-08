######################################################################
#                            Servidor                                #
######################################################################


import paho.mqtt.client as mqtt
from pycpfcnpj import cpfcnpj
import mysql.connector
# FIXME: ADD a parte do BD
import time

cnx = mysql.connector.connect(user='root', password='senha',
                              host='localhost',
                              database='Controle_de_Acesso')

# Funcoes MySQL

add_Alunos = ("INSERT INTO Alunos "
              "(NOME,CPF,SENHA) "
              "VALUES (%s, %s, %s)")


# Funcoes######

def ProcuraSenha(ValorCpf, ValorSenha):
    validador_senha = False
    query = ("SELECT SENHA"
             " FROM Alunos"
             " WHERE CPF = %(cpf_atual)s")

    cursor = cnx.cursor()
    cpf_atual = int(ValorCpf)
    cursor.execute(query, {'cpf_atual': cpf_atual})
    # print (cursor)
    # data = cursor.fetchall()

    for row in cursor:
        print(row)
        print(str(row[0]))
        if str(row[0]) == ValorSenha:
            print("Senha OK")
            validador_senha = True
        else:
            pass
            # validador_senha = False
    cursor.close()
    return validador_senha


def ProcuraCpf(ValorCpf):
    cursor = cnx.cursor()
    query = ("SELECT CPF FROM Alunos ")

    cursor.execute(query)

    validador_cpf = False
    for row in cursor:
        if (ValorCpf in row):
            print(row)
            print("Cpf existe e esta no banco")
            validador_cpf = True
        else:
            print(row)
            print("Cpf nao eh esse")

    cursor.close()
    return validador_cpf


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))

    if message.topic == "celular/dados":
        print("Dados")
        dado = str(message.payload.decode("utf-8")).split("$")
        # Chamar a func que valida o cpf e a senha

        # if dado[0] == cpf and dado[1] == senha:
        if ProcuraCpf(dado[0]) and ProcuraSenha(dado[0], dado[1]):
            # Resp_Env = "ok" + "%" + "Fem"
            client.publish("celular/dados/resposta", "ok")
        else:
            client.publish("celular/dados/resposta", "nao")

    if message.topic == "celular/porta":
        print(">>Topic: celular/porta/Masc")
        resp = str(message.payload.decode("utf-8"))
        print(resp)

        # Buscar no BD so sexo relacionado com o cpf indicado
        # ------------------------
        if message.payload.decode("utf-8") == "ON":
            # Mandar um comando RGPIO para abrir a porta
            print("Ligou!")
        if message.payload.decode("utf-8") == "OFF":
            print("Desligou!")

    if message.topic == "celular/porta/Fem":
        print(">>Topic: celular/porta/Fem")
        resp = str(message.payload.decode("utf-8"))
        print(resp)

        # Buscar no BD so sexo relacionado com o cpf indicado
        # ------------------------
        if message.payload.decode("utf-8") == "ON":
            # Mandar um comando RGPIO para abrir a porta
            print("Ligou!")
        if message.payload.decode("utf-8") == "OFF":
            print("Desligou!")
            # ------------------------

    if message.topic == "software/Add/validacao/Sw2Serv":
        print("Dados")
        dado = str(message.payload.decode("utf-8")).split("%")
        print(dado[1])
        # dado[0]: Nome #dado[1]: CPF #dado[2]: Senha
        if not ProcuraCpf(dado[1]):
            print("Cpf Nao existe no BD :)")
            data_Alunos = (dado[0], dado[1], dado[2])
            cursor = cnx.cursor()
            cursor.execute(add_Alunos, data_Alunos)
            cnx.commit()
            cursor.close()
            client.publish("software/Add/validacao/Serv2Sw", "Valido")
            time.sleep(0.5)
            # cnx.close()
            print("Finalizado!")
        else:
            print("CPF existe no Banco")
            client.publish("software/Add/validacao/Serv2Sw", "Nao Valido")
    # Add no BD
    #     data_Alunos = ("10120230345", "4321")




    if message.topic == "software/cpf/validacao/Env":
        print(">>Topic: software/cpf/validacao/Env")
        #     Procurar no BD se esse cpf existe
        cpf_ = str(message.payload.decode("utf-8"))
        print(cpf_)
        if ProcuraCpf(cpf_):
            client.publish("software/cpf/validacao/Recv", "Existe")
            print("Cpf existe no BD")
        else:
            client.publish("software/cpf/validacao/Recv", "Nao Existe")
            print("Cpf nao existe no BD")

    if message.topic == "software/Add_Aluno":
        print(">>Topic: software/Add_Aluno")
        aluno = str(message.payload.decode("utf-8")).split("%")
        '''
        aluno[0] = Nome do Aluno
        aluno[1] = Cpf do Aluno
        aluno[2] = Sexo do Aluno
        aluno[0] = Senha do Aluno

        '''
        print(aluno[0])

    '''
    if message.topic == "celular/cpf":
        print(">>Topic: celular/cpf")
    #     Buscar no mysql
        if cpf == message.payload.decode("utf-8"):
            print("Cpf igual")
            client.publish("celular/cpf/confirmacao", "ok")

    #         Manda uma msg via mqtt para o celular pra dizer que o cpf exite
        else:
            print("Cpf diferentes")

    if message.topic == "celular/senha":
        #     Buscar no mysql
        print(">>Topic: celular/senha")
        if senha == message.payload.decode("utf-8"):
            print("Senha Iguais")
            client.publish("celular/senha/confirmacao", "ok")
        else:
            print("Senha diferentes")

    '''


    # if message.topic == "software/cpf/Add_cpf":
    #     print("Cpf Add")
    # if message.topic == "software/senha/Add_senha":
    #     print("Senha Add")
    # if message.topic == "software/senha/Change_senha":


# Criando um cliente novo
client = mqtt.Client("Servidor_Ubunto")

# Conectando ao broker
print("Conectando em 192.168.1.3 ...")

client.on_message = on_message

# client.connect("192.168.0.25", 5050)
client.connect("192.168.1.3", 5050)

############## CELULARES ###########
# FIXME: Se inscrever no canal celular/porta/Masc!!!!
client.subscribe("celular/porta")
client.subscribe("celular/porta/Fem")
client.subscribe("celular/cpf")
client.subscribe("celular/senha")
client.subscribe("celular/dados")
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
# client.subscribe("software/Add_Aluno")
# client.subscribe("software/Mudar_Senha")
# client.subscribe("software/cpf/validacao/Env")
# client.subscribe("software/cpf/validacao/Recv")



############## SOFTWARE DO D.A. ###########
# # FIXME Olhar isso!
# client.subscribe("software/cpf/Add_cpf")
# client.subscribe("software/senha/Add_senha")
# client.subscribe("software/cpf/Change_senha")

client.loop_forever()




