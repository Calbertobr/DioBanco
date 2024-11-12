
from os.path import isfile
from datetime import datetime
import sqlite3

#####################################################################################
#
# Interação de banco de dados
#
def BancoWrite(Sql):
    with sqlite3.connect('data.db') as conn:
        Database = conn.cursor( )
        Database.execute(Sql)
        return Database.fetchall()
    
#####################################################################################
#
#   Verifica a existencia de dados e caso não exista cria base de dados
#
def CheckBanco():
    if isfile('data.db') :
        Sql = ('select count(*) from movimentacao ;')
        Result = BancoWrite(Sql)
        print(f'Banco com {Result[0][0]} registros.')
        Sql = ('select count(*) from cliente ;')
        Result = BancoWrite(Sql)
        print(f'Banco com {Result[0][0]} clientes.')
    else:
        DataBaseCreate = (
    """
    CREATE TABLE Cliente (
    CONTA INTEGER NOT NULL, NOME TEXT NOT NULL, CPF INTEGER NOT NULL, CEP INTEGER NOT NULL, NUMERO INTEGER NOT NULL,
    PRIMARY KEY(CONTA AUTOINCREMENT));
    """,
    """
    CREATE TABLE movimentacao (
    ID INTEGER NOT NULL UNIQUE, DATA TEXT NOT NULL, CONTA INTEGER NOT NULL, TRANSACAO INTEGER NOT NULL, VALOR_TRANSACAO INTEGER,
    SALDO INTEGER, PRIMARY KEY("ID" AUTOINCREMENT),
    FOREIGN KEY(CONTA) REFERENCES CLIENTE ( CONTA ));
    """)
        BancoWrite(DataBaseCreate[0])
        BancoWrite(DataBaseCreate[1])
        print(f'Banco com 0 itens.')

#####################################################################################
#
# Formata a data vinda do banco que e um str. 
#
def FormtData(data):
    return datetime.strptime(data,"%Y%m%d%H%M%S").strftime("%d/%m/%Y %H:%M:%S")

#####################################################################################
#
# Mota form cadastro cliente
#
def CadastraCliente(Conta):
    Sql = f"Select ifnull(count(*),0) qtd from cliente where conta = {Conta}" 
    Results = BancoWrite(Sql)
    if Results[0][0] != 1 :
        form   = ("Favor fornecer seu Nome: ", "Informe seu cpf: ", "Qual cep de sua moradia: ", "Qual numero: ")
        Cpf    = input(form[1])
        Sql = f"Select conta qtd from cliente where cpf = {Cpf}" 
        Results = BancoWrite(Sql)
        if len(Results) == 1 :
            print(f"Este ja tem conta vinculada de numero {Results[0][0]}")
            input('Tecle "S" para continuar')
            return Results[0][0]
        Nome   = input(form[0])
        Cep    = input(form[2])
        Numero = input(form[3])
        Sql = f" insert into cliente ( nome, cpf, cep, numero ) values ('{Nome}',{Cpf},{Cep},{Numero} ) ;"
        BancoWrite(Sql)
        Sql = f" select conta from cliente where cpf = '{Cpf}' ;"
        Results = BancoWrite(Sql)
        CheckConta(Results[0][0])
        Conta = Results[0][0]
        return Conta
    else:
        CheckConta(Conta)
        return Conta

#####################################################################################
#
# 
#
def DataAtual(db='n'):
    if db == 'n': 
        return datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    else:
        return datetime.today().strftime("%Y%m%d")

#####################################################################################
#
# 
#
def MovimentoTipo(Tipo):
    Moviment = ('Abertura', 'Deposito', 'Saque', 'Saldo Insuficiente')
    return Moviment[Tipo]

#####################################################################################
#
# Cria linha das telas
#
def Line(char = '-', msg = '',size = 0):
    linha = msg.center(size,char)
    linha = f'|{linha}|'
    return linha

#####################################################################################
#
# Valida Transações
#
def MovimentoValid(Conta,Tipo):
    Sql = f"""  select ifnull(count(*),0) as Movimentos from movimentacao where conta = {Conta} and substring(data,0,9) = '{DataAtual('s')}' group by substring(data,0,9) ;"""
    Movim = BancoWrite(Sql)
    if len(Movim) == 0 :
        return
    else:
        Movim = Movim[0][0]
        Sql = f"""  select ifnull(count(*),0) as Saques from movimentacao where conta = {Conta} and transacao in (0,2) and substring(data,0,9) = '{DataAtual('s')}' group by substring(data,0,9) ;"""
        Saque = BancoWrite(Sql)[0][0]

        if Movim >= 10 :
            return "Limite de movimentação diaria alcançada"
        else:
            if Saque > 3 and Tipo == 2 :
                return "Limite de saque diario alcançado"
            else:
                return    


#####################################################################################
#
# Monta Menu inicial 
#
def DigitaConta():
    MenuConta = f"""
{Line(msg='MENU', size=60, char ='-')}
{Line(size = 60, char = ' ' )}
{Line(msg='Digite o numero de sua conta: ', size=60, char =' ')} 
{Line(size = 60, char = ' ' )}
{Line(msg='', size=60, char ='-')}
"""
    return MenuConta

#####################################################################################
#
# Monta Menu inicial 
#
def MenuApresenta(MsgErro,Conta):
    MenuInterativo = f"""
{Line(msg='MENU', size=40, char ='-')}
{Line(size = 40, char = ' ' )}
|                             \033[34mcc: {Conta:3}\033[m    |
|   \033[32mDigite a opção desejada\033[m              |
|                                        |
|   \033[34mD\033[m - Deposito                         |
|   \033[34mS\033[m - Saque                            |
|   \033[34mE\033[m - Extrato                          |
|                                        |
|   \033[31mQ\033[m - Para Sair                        |
"""
    if MsgErro != "":
        MenuInterativo += f"|                                        |\n"
        MenuInterativo += f"|\033[31m{ MsgErro.center(40,' ')}\033[m|\n"
    MenuInterativo += f"{Line(size=40, char =' ')}\n"
    MenuInterativo += f"{Line(msg=str(DataAtual()), size=40, char ='-')}\n"
    return MenuInterativo

#####################################################################################
#
# Função de Movimento Financeiro 
#
def movimento(Conta,Tipo):
    Status = MovimentoValid(Conta,Tipo)
    if Status == None:
        try:
            Msg = ("Abertura Conta","Valor a depositar: R$ ","Valor do Saque: R$ ")
            data = datetime.now().strftime("%Y%m%d%H%M%S")
            Valor = float(input(Msg[Tipo]))
            Sql = (f'select "SALDO" from "movimentacao" where "CONTA" = {Conta} and "DATA" = ( select max("DATA") from "movimentacao" where "CONTA" = {Conta} ) ;')
            DataQuery = BancoWrite(Sql)
            Saldo = DataQuery[0][0]
            if Tipo == 1 :
                Saldo += Valor 
                Sql = f''' insert into movimentacao ( "DATA", "CONTA", "TRANSACAO", "VALOR_TRANSACAO", "SALDO" ) 
                values ({data}, {Conta},1,{Valor} , {Saldo} ) ; '''
                Result = BancoWrite(Sql)        
                return "Deposito Realizado."
            elif Tipo == 2 :
                if Valor <= DataQuery[0][0]:
                    Saldo -= Valor 
                    Sql = f''' insert into movimentacao ( "DATA", "CONTA", "TRANSACAO", "VALOR_TRANSACAO", "SALDO" ) 
                    values ({data}, {Conta},2,{Valor} , {Saldo} ) ; '''
                    Result = BancoWrite(Sql)
                    return "Saque Realizado."
                else:
                    Sql = f''' insert into movimentacao ( "DATA", "CONTA", "TRANSACAO", "VALOR_TRANSACAO", "SALDO" ) 
                    values ({data}, {Conta},3,{Valor} , {Saldo} ) ; '''
                    Result = BancoWrite(Sql)
                    return "Saldo insuficiente"
            else:
                return "Erro sistemico"    
        except:
            return "Valor digitado e invalido."
    else:
        return Status

#####################################################################################
#
# 
#
def CheckConta(Conta):
    Sql = (f'select "SALDO" from "movimentacao" where "CONTA" = {Conta} ;')
    Result = BancoWrite(Sql)
    Rows = len(Result) 
    if Rows == 0 :
        data = datetime.now().strftime("%Y%m%d%H%M%S")
        Sql = f''' insert into movimentacao ( "DATA", "CONTA", "TRANSACAO", "VALOR_TRANSACAO", "SALDO" ) 
        values ({data}, {Conta},0,0,0) ; '''
        Result = BancoWrite(Sql)
        return "Conta Iniciada"
    else:
        return "Conta Existente"

#####################################################################################
#
# Extrato 
#
def Extrato(Conta):
    ExtratoHeader = ('id','Data Evento', 'Conta', 'Tipo Evento', 'Valor', 'Saldo Atual')
    ClienteHeader  = ('Conta','Nome','Cep','Numero','Cpf')
    ExtratoCompleto = f"{ Line(size = 84 ) }\n"
    ExtratoCompleto += f"| {ClienteHeader[0]} | {ClienteHeader[1]:37} | {ClienteHeader[2]:8} | {ClienteHeader[3]:5} | {ClienteHeader[4]:14} |\n"
    ExtratoCompleto = f"{ Line(size = 84 ) }\n"
    Sql = f"select * from cliente where conta = {Conta};"
    Results = BancoWrite(Sql)
    for data in Results:
        cpf = str(data[2])
        Cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[-2:]}'
        ExtratoCompleto += f"| {data[0]:5} | {data[1]:37} | {data[3]:8} | {data[4]:6} | {Cpf} |\n"
    ExtratoCompleto += f"{ Line(char=' ',size = 84 )}\n"
    ExtratoCompleto += f'{Line(size = 84 )}\n'
    ExtratoCompleto += f'| {ExtratoHeader[0]:3} | {ExtratoHeader[1]:20}| {ExtratoHeader[3]:25}| {ExtratoHeader[4]:12} | {ExtratoHeader[5]:12} |\n'
    ExtratoCompleto += f'{Line(size = 84 )}\n'
    Sql = f'select * from movimentacao where CONTA = {Conta}'
    Result = BancoWrite(Sql)
    for moviment in Result :
        ExtratoCompleto += f'| {moviment[0]:3} | {FormtData(moviment[1])} | {MovimentoTipo(moviment[3]):24} | {moviment[4]:12.2f} | {moviment[5]:12.2f} |\n'
    ExtratoCompleto += f"{ Line(char=' ',size = 84 )}\n"
    ExtratoCompleto += f'{ Line(msg=str(DataAtual()),size = 84 ) }\n'
    print(ExtratoCompleto)
    input("Clique 'S' para continuar.")
