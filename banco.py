#!/bin/python3

from datetime import date, datetime
from os import system
from os.path import isfile 
if isfile('data.py') :
    from data import data
    ExtratoHistorico = data()
    SaldoAtual = float(ExtratoHistorico[len(ExtratoHistorico)-1][3])
else:
    ExtratoHistorico = []
    SaldoAtual = float(0)

Data = date.today()
SaquesDiarios = 3
Limite = 0 
Data = datetime.today().strftime("%d/%m/%Y %H:%M")
MsgErro = ""
ExtratoHeader = [ 'Data Evento', 'Tipo Evento', 'Valor operação', 'Saldo Atual' ]


def Line(char = '-', msg = '',size = 0):
    linha = msg.center(size,char)
    linha = f'|{linha}|'
    return linha

def MenuApresenta(MsgErro):
    MenuInterativo = f"""
{Line(msg='MENU', size=40, char ='-')}
{Line(size = 40, char = ' ' )}
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
    MenuInterativo += f"{Line(msg=str(Data), size=40, char ='-')}\n"
    return MenuInterativo


def Extrato():
    global ExtratoHeader
    ExtratoCompletoHed = f'\n{ Line(size = 81) }\n|  {ExtratoHeader[0]:16}| {ExtratoHeader[1]:19}| {ExtratoHeader[2]:19}| {ExtratoHeader[3]:19}|\n{Line(size = 81)}' 
    print(ExtratoCompletoHed)
    global ExtratoHistorico
    ExtratoCompleto = ''
    for a in ExtratoHistorico:
        ExtratoCompleto += f"| {a[0]}{'':1}| {a[1]:19}| R$ {a[2]:15.2f} | R$ {a[3]:15.2f} |\n"
    ExtratoCompleto += f"{ Line(msg=str(Data),size = 81)}\n"
    print(ExtratoCompleto)
    input("Clique 'S' para continuar.")


def Deposito():
    try:
        Valor = float(input("Valor a depositar: R$"))
        global SaldoAtual        
        SaldoAtual += float(Valor)
        reg=( str(Data), 'Deposito', Valor, SaldoAtual )
        ExtratoHistorico.append( reg )
        return "Deposito Realizado."
    except:
        return "Valor digitado e invalido."


def Saque():
    try :
        Valor = float(input( "Valor a Sacar: R$ " ))
        global SaldoAtual
        if Valor <= SaldoAtual :
            SaldoAtual -= float(Valor)
            reg=( str(Data), 'Saque', Valor, SaldoAtual )
            ExtratoHistorico.append( reg )
            return "Saque Realizado."
        else:
            reg=( str(Data), 'Tentetiva de Saque', Valor, SaldoAtual )
            ExtratoHistorico.append( reg )
            return "Saldo Insuficiente."
    except:
        return "Valor digitado e invalido."


def Gravar():
    FileData = open('data.py','w')
    StrData = f"""
def data():
    dados = {ExtratoHistorico}
    return dados
"""
    FileData.write(StrData)


while True:
    system("clear")
    opcao =  input( MenuApresenta(MsgErro) ).upper()
    MsgErro = ""
    if opcao == 'D' :
        MsgErro = Deposito()
    elif opcao == 'S' :
        MsgErro = Saque()
    elif opcao == 'E' :
        system("clear")
        Extrato()
    elif opcao == 'Q' :
        Gravar()
        break
    else:
        MsgErro = "Escolher uma opção Valida"
