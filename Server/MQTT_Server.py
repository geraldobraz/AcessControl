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
               "(NOME,CPF,SEXO,SENHA) "
               "VALUES (%s, %s, %s, %s)")

update_senha = ("UPDATE Alunos SET SENHA = %s"
              "WHERE CPF = %s")

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
        print (str(row[0]))
        if str(row[0]) == ValorSenha:
            print ("Senha OK")
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
            print (row)
            print ("Cpf existe e esta no banco")
            validador_cpf = True
        else:
            print (row)
            print ("Cpf nao eh esse")

    cursor.close()
    return validador_cpf
def ProcuraGenero(ValorCpf):
    procura_genero = ("SELECT SEXO "
                     "FROM Alunos "
                     "WHERE CPF = %(cpf_atual)s")
    cursor = cnx.cursor()
    cpf_atual = int(ValorCpf)
    cursor.execute(procura_genero, {'cpf_atual': cpf_atual})
    dados = []
    for row in cursor:
        print(row)
        print (str(row[0]))
        if str(row[0]) == "Masculino":
            print (">> Masculino")
            resposta = "Masc"
        else:
            print (">> Feminino")
            resposta = "Fem"
    
     
    cnx.commit()
    cursor.close()
    print(">> resposta: " + resposta)
    return resposta

def ProcuraAluno(ValorCpf):
    procura_dados = ("SELECT NOME,CPF,SEXO "
                     "FROM Alunos "
                     "WHERE CPF = %(cpf_atual)s")
    cursor = cnx.cursor()
    cpf_atual = int(ValorCpf)
    cursor.execute(procura_dados, {'cpf_atual': cpf_atual})
    dados = []
    for row in cursor:
        dados = ([row[i] for i in range(0,len(row))])
    dados ="$".join(dados)
    cnx.commit()
    cursor.close()
    return dados
def ApagarAluno(ValorCpf):
    apagar_aluno = ("DELETE FROM Alunos "
                         "WHERE CPF = %(cpf_atual)s")
    cursor = cnx.cursor()
    cpf_atual = int(ValorCpf)
    cursor.execute(apagar_aluno, {'cpf_atual': cpf_atual})
    cnx.commit()
    cursor.close()
    print ("Apagou o Aluno: ", ValorCpf)
def ListarAlunos():
    listar_alunos = ("SELECT NOME, CPF, SEXO FROM Alunos ORDER BY NOME")
    cursor = cnx.cursor()
    cursor.execute(listar_alunos)
    dados = []
    # FIXME: Tratar tabelas vazias!
    for row in cursor:
        # DadosAluno+?+DadosAluno+?+...
        dados.append("$".join(row) + "?")
        print(row)
    else:
        print("Nao entrou!")
    cursor.close()
    return "".join(dados)

def on_message(client, userdata, message):
    print ("Message received: " + str(message.payload.decode("utf-8")))
    print ("Topic: " + str (message.topic) )
    # Receber os dados do celular
    if message.topic == "celular/dados":
        print("Dados")
        dado = str(message.payload.decode("utf-8")).split("$")
        print(dado)
        # Chamar a func que valida o cpf e a senha

        # if dado[0] == cpf and dado[1] == senha:
        if ProcuraCpf(dado[0]) and ProcuraSenha(dado[0],dado[1]):
            client.publish("celular/dados/resposta", ProcuraGenero(dado[0]))
        else:
            client.publish("celular/dados/resposta", "nao")
    # Abrir porta Masc
    if message.topic == "celular/porta/Masc":
        print(">>Topic: celular/porta/Masc")
        resp = str(message.payload.decode("utf-8"))
        print(resp)

        # Buscar no BD so sexo relacionado com o cpf indicado
        #------------------------
        if message.payload.decode("utf-8") == "ON":
            # Mandar um comando RGPIO para abrir a porta
            print("Ligou!")
        else:
            pass
    # Abrir porta Fem
    if message.topic == "celular/porta/Fem":
        print(">>Topic: celular/porta/Fem")
        resp = str(message.payload.decode("utf-8"))
        print(resp)

        # Buscar no BD so sexo relacionado com o cpf indicado
        # ------------------------
        if message.payload.decode("utf-8") == "ON":
            # Mandar um comando RGPIO para abrir a porta
            print("Ligou!")
        else:
            pass
        #------------------------
    # Adicao de Aluno
    if message.topic == "software/Add/validacao/Sw2Serv":
        print("Dados")
        dado = str(message.payload.decode("utf-8")).split("%")
        print (dado[1])
        #dado[0]: Nome #dado[1]: CPF #dado[2]: Sexo #dado[3]: Senha
        if not ProcuraCpf(dado[1]):
            print ("Cpf Nao existe no BD :)")
            data_Alunos = (dado[0],dado[1],dado[2],dado[3])
            cursor = cnx.cursor()
            cursor.execute(add_Alunos, data_Alunos)
            cnx.commit()
            cursor.close()
            client.publish("software/Add/validacao/Serv2Sw","Valido")
            time.sleep(0.5)
            # cnx.close()
            print ("Finalizado!")
        else:
            print ("CPF existe no Banco")
            client.publish("software/Add/validacao/Serv2Sw", "Nao Valido")
    # Trocar Senha
    if message.topic == "software/Trocar/validacao/Sw2Serv":
        print("Dados")
        dado = str(message.payload.decode("utf-8")).split("%")
        print (dado[0],dado[1])
        #dado[0]: CPF #dado[1]: Nova Senha
        if ProcuraCpf(dado[0]):
            print ("CPF encontrado)")
            data_Alunos = (dado[1],dado[0])
            cursor = cnx.cursor()
            cursor.execute(update_senha, data_Alunos)

            cnx.commit()
            cursor.close()
            client.publish("software/Trocar/validacao/Serv2Sw","Valido")
            time.sleep(0.5)
            # cnx.close()
            print ("Finalizado!")
        else:
            print ("CPF existe no Banco")
            client.publish("software/Trocar/validacao/Serv2Sw", "Nao Valido")
    # Listar Aluno Especifico
    if message.topic == "software/Procura/validacao/Sw2Serv":
        print("1")
        dado = str(message.payload.decode("utf-8"))
        print("2")
        if ProcuraCpf(dado):
            print("3")
            print (type(ProcuraAluno(dado)))
            client.publish("software/Procura/validacao/Serv2Sw", "Valido$"+ ProcuraAluno(dado))
            print ("Enviou!")
        else:
            client.publish("software/Procura/validacao/Serv2Sw", "Nao Valido$" + ProcuraAluno(dado))
    # Apagar Aluno
    if message.topic == "software/Apagar/validacao/Sw2Serv":
        dado = str(message.payload.decode("utf-8"))
        if ProcuraCpf(dado):
            ApagarAluno(dado)
            client.publish("software/Apagar/validacao/Serv2Sw", "Valido")
            # print ("Enviou!")
        else:
            client.publish("software/Apagar/validacao/Serv2Sw", "Nao Valido")
    # Listar todos os Alunos
    if message.topic == "software/ListarTodos/validacao/Sw2Serv":
        dado = str(message.payload.decode("utf-8"))
        if dado == "Listar":
            client.publish("software/ListarTodos/validacao/Serv2Sw", ListarAlunos())
            print ("Enviou!",ListarAlunos())


# Criando um cliente novo
client = mqtt.Client("Servidor_Raspberry")

# Conectando ao broker
print ("Conectando em 192.168.0.37 ...")

client.on_message = on_message

# client.connect("192.168.0.25", 5050)
client.connect("192.168.1.3", 5050)

############## CELULARES ###########
# FIXME: Se inscrever no canal celular/porta/Masc!!!!
client.subscribe("celular/porta/Masc")
client.subscribe("celular/porta/Fem")
client.subscribe("celular/cpf")
client.subscribe("celular/senha")
client.subscribe("celular/dados")
client.subscribe("software/Add/validacao/Sw2Serv")
client.subscribe("software/Add/validacao/Serv2Sw")
client.subscribe("software/Trocar/validacao/Sw2Serv")
client.subscribe("software/Procura/validacao/Sw2Serv")
client.subscribe("software/ListarTodos/validacao/Sw2Serv")
client.subscribe("software/Apagar/validacao/Sw2Serv")


client.loop_forever()

