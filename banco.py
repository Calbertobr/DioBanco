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

# MovimentoValid( 1 , 1 )

# print(CadastraCliente(1))

while True:
    try:
        system("clear")
        Cont = int(input(DigitaConta()))
        Conta = CadastraCliente(Cont)
        break
    except:
        print("Numero de conta invalido.")


while True:
    system("clear")
    opcao =  input( MenuApresenta( MsgErro , Conta ) ).upper()
    MsgErro = ""
    if opcao == 'D' :
        MsgErro = movimento( Conta , 1 )
    elif opcao == 'S' :
        MsgErro = movimento( Conta , 2 )
    elif opcao == 'E' :
        system("clear")
        Extrato(Conta)
    elif opcao == 'Q' :
        system("clear")
        break
    else:
        MsgErro = "Escolher uma opção Valida"


