#!/bin/python3

from datetime import date, datetime
from os import system
from os.path import isfile
from lib import *

####################################################
#
# Variaveis
#
MsgErro = ""
SaquesDiarios = 3
#Limite = 0 

####################################################

CheckBanco()

while True:
    try:
        system("clear")
        Conta = int(input(DigitaConta()))
        if Conta > 0 and Conta < 1000 :
            print( CheckConta(Conta) )
        else:
            print("Numero de conta invalido!")
            continue
        break
    except:
        print("Numero de conta invalido.")

while True:
    system("clear")
    opcao =  input( MenuApresenta(MsgErro,Conta) ).upper()
    MsgErro = ""
    if opcao == 'D' :
        MsgErro = movimento(Conta,1)
    elif opcao == 'S' :
        MsgErro = movimento(Conta,2)
    elif opcao == 'E' :
        system("clear")
        Extrato(Conta)
    elif opcao == 'Q' :
        system("clear")
        break
    else:
        MsgErro = "Escolher uma opção Valida"


