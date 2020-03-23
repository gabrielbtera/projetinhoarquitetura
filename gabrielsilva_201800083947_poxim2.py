import sys
import ctypes
from ctypes import *
import math
from math import *
import struct


#master
#poxim 2.1
arquivo_entrada1 = open("entrada.txt", 'r')
arquivo_entrada = arquivo_entrada1.readlines()
arquivo_saida = open("saida.txt", 'w')


#transforma em hexa de 32 bits
def hex8(hexa):
    hexa = hex(hexa).upper()
    if len(hexa[2:]) < 2:
        c = hexa[2:].zfill(2)
        return "0x" + c
    else:
        return "0x" + hexa[2:]



def converteListastr(lista):
    s = ''
    for i in lista:
        s += i
    return s


def hex16(hexa):
    hexa = hex(hexa).upper()
    if len(hexa[2:]) < 4:
        c = hexa[2:].zfill(4)
        return "0x" + c
    else:
        return "0x" + hexa[2:]

def hex24(hexa):
    hexa = hex(hexa).upper()
    if len(hexa[2:]) < 6:
        c = hexa[2:].zfill(6)
        return "0x" + c
    else:
        return "0x" + hexa[2:]

def hex32(hexa):
        hexa = hex(hexa).upper()
        if len(hexa[2:]) < 8:
                c = hexa[2:].zfill(8)
                return "0x" + c
        else:
                return "0x" + hexa[2:]


def bin_hex(binario):
    lista_hexa = {"0000":"0", "0001":"1", "0010":"2", "0011":"3", "0100":"4", "0101":"5",
                 "0110":"6", "0111":"7", "1000":"8", "1001":"9", "1010":"A", "1011":"B", 
                 "1100":"C", "1101":"D","1110" :"E", "1111":"F"}

    hexadecimal = ""
    quatro = ""
    for i in binario:
        quatro += i
        if len(quatro) == 4:
            hexadecimal += lista_hexa[quatro].upper()  
            quatro = ""
    return "0x" + hexadecimal


def hex64(hexa):
    hexa = hex(hexa).upper()
    if len(hexa[2:]) < 16:
            c = hexa[2:].zfill(16)
            return "0x" + c
    else:
            return "0x" + hexa[2:]


###################################FUNCOES DO IEEE-754########################################
# converte float para binario
def converte_float_binario(numero):
    
    inteiro, fracionario = str(numero).split(".")
    inteiro = bin(int(inteiro))[2:]
    
    if inteiro[0] == "b":
        inteiro = inteiro[1:]

    manipulacao = float("0." + fracionario)
    n = manipulacao
    s = ""
    while n != 0:
        n = manipulacao * 2
        s += str(n)[0]
        if n >= 1:
            n -= 1
        manipulacao = n

    return inteiro + "." + s


# extrai um expoente de um dado real
def extrai_expoente(numero1):
    numero = converte_float_binario(numero1)
    cont = 0
    if int(numero[0]) > 0:
        num_1 = numero.split(".")[0]
        for i in range(len(num_1)):
            if num_1[i] == "1":
                cont = len(num_1) - (i + 1)
                break
    elif int(numero[0]) == 0:
        num_1 = numero.split(".")[1]
        for i in range(len(num_1)):
            if num_1[i] == "1":
                cont = (i) - len(num_1)
                break
    
    if numero1 < 0:
        var = "1" + (bin(cont + 127)[2:]).zfill(8)
    else:
        var = "0" + bin(cont + 127)[2:].zfill(8)
    return (var, cont)


# extrai a mantissa de um dado Real
def extrai_mantissa(numero1):
    qnt = extrai_expoente(numero1)[1]
    numero, n2 = converte_float_binario(numero1).split(".")
    if numero[0] != "0":
        num = numero[::-1][:qnt]
        final =  num[::-1] + n2
    elif numero[0] == "0":
        num = n2[qnt + 1:]
        final = num
    
    if len(final) > 23:
        final = final[:24]
    else:
        final = final[::-1].zfill(23)[::-1]
    return final

def ieee_754(numero1):
    return extrai_expoente(numero1)[0] + extrai_mantissa(numero1)


# converte para inteiro a parte do expoente
def converte_expoente(binario):
    binario = binario[1:9]
    return int(binario, 2) - 127

# converte para float a parte de mantissa
def converte_mantissa(binario1):
    mantissa = binario1[9:]
    elevado = -1
    m = 0
    for i in mantissa:
        numero = 2 ** elevado
        m += int(i) * numero
        elevado -= 1
    return m

# extrai o valor float do ieee 754
def extrai_ieee_754(binario):
    return ((-1) ** int(binario[0]))* (1 + converte_mantissa(binario)) * 2 ** converte_expoente(binario)


############################################ funcoes da cash ###########################################################
def inicializa_cash():
    lista_fim = dict()
    for i in range(0, 8):
        lista = [[0, False, None, 0, 1, 2, 3], [0,False, None , 0, 1, 2, 3]]
        lista_fim[bin(i)[2:].zfill(3)] = lista
    return lista_fim
#########################################################################################################################

#32 registradores sendo R28=IR, R29=PC, R30=SP, R31=SR, 
class Registradores():
    
    def __init__ (self,registradores):
        self.registradores = registradores


    # seta todos os outros registradores
    def setRegistradores(self, operacao, indice):
        if indice != 0:
            self.registradores[indice] = operacao.zfill(32)
        else:
            self.registradores[0] = "0".zfill(32)


    # armazena a instrucao carregada em memoria
    def setRegistradorSR(self,indice,zn, zd, sn, ov, cy, iv):
        lista = list(self.registradores[31])
        if zn != -1:
            lista[25] = str(int(zn)) 
        if zd != -1:
            lista[26] = str(int(zd))
        if sn != -1:
            lista[27] = str(int(sn))
        if ov != -1:
            lista[28] = str(int(ov))
        if iv != -1:
            lista[29] = str(int(iv))
        if cy != -1:
            lista[31] = str(int(cy))
        regis = ''
        for i in lista:
            regis += i
        self.registradores[31] = regis
    

    def setRegistrador_interruption_SR(self,indice,zn, zd, sn, ov, iv, ie, cy):
        lista = list(self.registradores[31])
        if zn != -1:
            lista[25] = str(int(zn)) 
        if zd != -1:
            lista[26] = str(int(zd))
        if sn != -1:
            lista[27] = str(int(sn))
        if ov != -1:
            lista[28] = str(int(ov))
        if iv != -1:
            lista[29] = str(int(iv))
        if ie != -1:
            lista[30] = str(int(ie)) # controle de interrupcao ->   0: desabilitada; 1: habilitada
        if cy != -1:
            lista[31] = str(int(cy))
        regis = ''
        for i in lista:
            regis += i
        self.registradores[31] = regis


    # get memory ram
    def setRegistradorSP(self, instrucao_memoria):
        self.registradores[30] = bin(instrucao_memoria)[2:].zfill(32)


    def setRegistradorPC(self, pc_c):
        self.registradores[29] = bin(pc_c)[2:].zfill(32)


    def setRegistradorIR(self, instrucao):
        self.registradores[28] = bin(int(instrucao, 2))[2:].zfill(32)


    def setRegistradorIPC(self, instrucao):
        if type(instrucao) == type(1):
            self.registradores[27] = bin(instrucao)[2:].zfill(32)
        elif type(instrucao) == type("str"):
            self.registradores[27] = instrucao


    def setRegistradorCR(self, instrucao):
        if type(instrucao) == type(1):
            self.registradores[26] = bin(instrucao)[2:].zfill(32)
        elif type(instrucao) == type("str"):
            self.registradores[26] = instrucao
    

    def set_bit_registrador(self,indice_registrador, posicao_no_registrador, bit):
        lista = list(self.registradores[indice_registrador])
        lista.reverse()
        lista[posicao_no_registrador] = bit
        lista.reverse()

        s = ""
        for i in lista:
            s += i
        self.registradores[indice_registrador] = s



    def get32Registradores(self, indice):
        return self.registradores[indice]
    

    def getHexaRegistrador(self, indiceRegister):
        return hex32(self.registradores[indiceRegister])



class Memoria():
    def __init__ (self, memoria, registradores):
        self.memoria = memoria
        self.registradores = registradores
    

    def setMemoriaNoRegister(self, posi_pc, indice_R):  # ecreve no registrador
        temp = ''
        for i in range(posi_pc, posi_pc + 4):
            temp += self.memoria[i]
        self.registradores[indice_R] = temp
    

    def setRegistradorMemoria(self, indice_mem, indice_register, quantidade): # escreve na memoria
        cont = 0
        no_register = int(self.registradores[indice_register], 2) + quantidade
        no_register = bin(no_register)[2:].zfill(32)
        for i in range(4):
            self.memoria[indice_mem] = no_register[cont:cont + 8]
            cont += 8
            indice_mem += 1


    def setRegistradorMemoria2(self, indice_mem, indice_register):
        cont = 0
        no_register = self.registradores[indice_register]
        for i in range(4):
            self.memoria[indice_mem] = no_register[cont:cont + 8]
            cont += 8
            indice_mem += 1


def escreveInstrucaoMemoria(arquivo, memoria):
    n = 0
    for i in arquivo:
        instrucao = bin(int(i.rstrip(), 16))[2:].zfill(32)
        s = ''
        for bit in instrucao:
            s += bit
            if len(s) == 8:
                memoria[n] = s
                s = ''
                n += 1
    return memoria 


# dog = 0, x = 1, y = 2, z = 3,  f4 = 4

class interuption_hwe():                   # classe [INTERRUPTIO HARDWARE]
    def __init__ (self, registradores):
        self.registradores = registradores

    
    def set_watch_dog(self, valor, bole):
        if valor[0] == "b":
            valor = valor[1:]
        binario = valor.zfill(32)
        
        if bole:
            lista = list(binario)
            lista[0] = "1"
            s = ""
            for i in lista:
                s += i
            self.registradores[0] = s
        else:
            self.registradores[0] = valor.zfill(32)

    def set_FPU_x(self, registradores_x):
        self.registradores[1] = registradores_x
    

    def set_FPU_y(self, registradores_y):
       
        self.registradores[2] = registradores_y
    

    def set_FPU_z(self, registradores_z):
        
        self.registradores[3] = registradores_z
    
    def set_opcode(self):
        lista = list(self.registradores[4])
       
        for i in range(len(lista)):
            if i == 26:
               
                continue
            else:
                lista[i] = "0"
        s = ""
        for i in lista:
            s += i
        self.registradores[4] = s.zfill(32)
        

    def set_FPU_4(self, registradores_4, boleano):
        self.registradores[4] = registradores_4
        

    def set_st(self, st):
        lista = list(self.registradores[4])
        lista[26] = st
        for i in range(27,len(lista)):
            lista[i] = "0"
        s = ""
        for i in lista:
            s += i
        self.registradores[4] = s
        
    def set_out(self, registrador):
        registrador = registrador[25:]
        self.registradores[6] = registrador.zfill(32)
        

    def get_watch_dog(self):
        return self.registradores[0]

         

###################instancias das classes##################################
                                                                          
registradores_32 = ['0' * 32 for i in range(32)]                          
memoria_32kbys = ['0'* 8 for i in range(32 * 1024)]                          
memoria_32kbys = escreveInstrucaoMemoria(arquivo_entrada, memoria_32kbys)
registradores_hwe = ["0" * 32 for i in range(7)]

obj_interrupt_hwe = interuption_hwe(registradores_hwe)
objregistradores = Registradores(registradores_32)                        
objmemoria = Memoria(memoria_32kbys, registradores_32)                  

# ajuste
ajuste = 32

# variaveis dos indices
cr = 26
ipc = 27
pc = 29
ir = 28
sr = 31
sp = 30
cpu_pc = 0
veri = -1

# INDICES DE SR:
zn, zd, sn, ov, iv, ie, cy = 25, 26, 27, 28, 29, 30, 31

# variaveis watch dog
endereco_watch_dog = int("0x80808080", 16)
watch_dog_var = 0

# variaveis Fpu
ciclo_fpu = 0
fpu_controle = 0

var_fpu_x = int("0x80808880", 16)
var_fpu_y = int("0x80808884", 16)
var_fpu_z = int("0x80808888", 16)
var_fpu_4 = int("0x8080888C", 16)
var_fpu_op = int("0x8080888F", 16)
var_terminal = int(0x8888888B)

lista_fpu = [i for i in range(int(0x80808880), int(0x8080888C) + 4)]

fpu_x = 1
fpu_y = 2
fpu_z = 3
fpu_control = 4

verifica_x = False
verifica_y = False

# inicializacao de ambas as cash's
cash_instrucao = inicializa_cash()
cash_dado = inicializa_cash()

acertos_cash_I = 0
erros_cash_I = 0
acertos_cash_D = 0
erros_cash_D = 0


############################################## fucoes de uso geral#
def arredondamento_n(n):
    n1 = abs(int(n) - n)
    if n1 > 5:
        n = ceil(n)
    elif n1 < 5:
        n = math.floor(n)
    return n

def conta_ciclo():
    global verifica_x, verifica_y

    if int("0x24e69595", 16) <= int(registradores_hwe[fpu_x], 2):
        x = int(registradores_hwe[fpu_x][1:9], 2) - 127
        
    else:
        x = int(bin(int(struct.pack(">f", int(registradores_hwe[fpu_x], 2)).hex(), 16))[2:].zfill(32)[1:9], 2) - 127
        
    if int("0x24e69595", 16) <= int(registradores_hwe[fpu_y], 2):
        y = int(registradores_hwe[fpu_y][1:9], 2) - 127
    else:
        y = int(bin(int(struct.pack(">f", int(registradores_hwe[fpu_y], 2)).hex(), 16))[2:].zfill(32)[1:9], 2) - 127
   
    return abs(x-y) + 1

def nomeRgsMai(registradores, indice): #retorna os nomes/indices maiusculos
    if indice == 26:
        return "CR"
    elif indice == 27:
        return "IPC"
    elif indice == 28:
        return "IR"
    elif indice == 29:
        return "PC"
    elif indice == 30:
        return "SP"
    elif indice == 31:
        return "SR"
    else:
        return f"R{indice}"


def nomeRgsmin(registradores, indice): #retorna os nomes/indices minusculos
    if indice == 26:
        return "cr"
    elif indice == 27:
        return "ipc"
    elif indice == 28:
        return "ir"
    elif indice == 29:
        return "pc"
    elif indice == 30:
        return "sp"
    elif indice == 31:
        return "sr"
    else:
        return f"r{indice}"            

def ler_bytes(registrador, memoria, indice_mem, qnt):
    # pega da memoria

    de = indice_mem
    if qnt == 8:
        ate = indice_mem + 1
    if qnt == 16:
        ate = indice_mem + 2
    if qnt == 32:
        ate = indice_mem + 4
    s = ""
    for i in range(de, ate):
        s += str(memoria[i])  
   
    lista_atual = list(registrador)
    new_list = lista_atual[:(len(registrador) - qnt) + 1]

    strig = ""
    for i in new_list:
        strig += i
    return strig + s
        

# extene sinal das funcoes
def extende32Sinal(binario):
    if "b" in binario:
        binario = binario[1:]
    if binario[0] == "1":
        s = ''
        for i in range(0, 32-len(binario)):
            s+= "1"
        return s + binario
    elif binario[0] == "0":
        s = ''
        for i in range(0, 32-len(binario)):
            s+= "0"
        return s + binario


def extende64Sinal(binario):
    if "b" == binario[0]:
        binario = binario[1:]
    if binario[0] == "1":
        s = ''
        for i in range(0, 64-len(binario)):
            s+= "1"
        return s + binario
    elif binario[0] == "0":
        s = ''
        for i in range(0, 64-len(binario)):
            s+= "0"
        return s + binario


# distribui instrucoes na memoria de byte a byte
def pegaIstrucaoMemoria(memoria, de, ate):
    s = ''
    instrucao = ''
    for i in range(de, ate + 1):
        if len(s) == 32:
            instrucao = s
        s += memoria[i]
    return instrucao


def converteInteiroEmBinario32Bits(decimal):  # converter inteiro binario
    return bin(decimal)[2:].zfill(32)


def procuraIndiceMemoria(lista, de, ate):
    s = ""
    for i in range(de, ate):
        s += str(lista[i])
    return s.zfill(32)


# faz a escrita na memoria podend ser implementada entradas invalidas
def funcaoEscrevenaRgistradorMemoria(registradores, memoria, indice_memoria, qnt_bits):
    s = ''
    for i in range(abs(len(registradores)-qnt_bits), len(registradores)):
        s += registradores[i]
        if len(s) == 8:
            memoria[indice_memoria] = s
            indice_memoria += 1
            s = ''
    return memoria

# ao contrario da funcaoEscrevenaRgistradorMemoria esla escreve nomente indice global da memoria
def funcaoEcreveRegistradorEmIndiceMemoria(registradores, indice_memoria, qnt_bits):
    s = ''
    for i in range(abs(len(registradores)-qnt_bits), len(registradores)):
        s += registradores[i]
        if len(s) == 8:
            memoria_32kbys[indice_memoria] = s
            indice_memoria += 1
            s = ''

def converteHexaemBinario32Bits(entrada):  # converter hexa em binario
    binario = bin(int(entrada, 16))[2:].zfill(32)
    return binario

# Format U (OP, Z, X, Y, L)
# leitura dos campos de entrada op, z, x, y, l:
def opRead(entrada):
    return entrada[0:6]


def zRead(entrada):
    return entrada[6:11]


def xRead(entrada):
    return entrada[11:16]


def yRead(entrada):
    return entrada[16:21]


def lRead(entrada):
    return entrada[21:32]


def lReadF(entrada):   # funcao de leitura da instruacao l - Formato F
    return entrada[16:32]


def lReadS(entrada): # funcao de leituea da instrucao l = formado S
    return entrada[6:32]

def lRead_fpu(entrada):
    return entrada[27:]
# ela retorna o que está no indice da memoria, recebendo a memoria uma instruçao e um comando
def chamaIndiciesDeR(memoria, instrucao, comando):
    if comando == "x":
        return memoria[int(xRead(instrucao), 2)]
    elif comando == "y":
        return memoria[int(yRead(instrucao), 2)]
    elif comando == "z":
        return  memoria[int(zRead(instrucao), 2)]
    elif comando == "l":
        return memoria[int(lRead(instrucao), 2)]
    elif comando == "lf":
        return memoria[int(lReadF(instrucao), 2)]
    else:
        return 0


############################################  UNIDADE 3  #################################################################
def pega_linha(regs):
    return regs[25:28]


def pega_id(regs):
    return regs[:25]


def pega_palavra(regs):
    return regs[28:30]


def incrementa_Idade(cash, registIR):
    linha = pega_linha(registIR[pc])
    chaves = cash.keys()
    for chave in chaves:
        if cash[chave][0][1]:
            if cash[chave][0][0] <= 7:
                idade1 = cash[chave][0][0] + 1
                cash[chave][0][0] = idade1
                
        if cash[chave][1][1]:
            if cash[chave][1][0] <= 7:
                idade1 = cash[chave][1][0] + 1
                cash[chave][1][0] = idade1
    

def busca_mem(regIR):
    endereco = int(regIR, 2)
    while endereco % 16 != 0:
        endereco -= 1
    
    lista_mem = list()
    for i in range(4):
        lista_mem.append(converteListastr(memoria_32kbys[endereco : endereco + 4]))
        endereco += 4
    return lista_mem

def busca_escreve_mem():
    pass

def processamento(item, linha_atual, identificador, dados_mem): #opcao = "+" ou "-"
    linha_atual[item][0] = 0
    linha_atual[item][1] = True
    linha_atual[item][2] = identificador
    c = 3
    for data in dados_mem:
        linha_atual[item][c] = data
        c += 1
    return linha_atual


def pega_data_cash(cash, registrador, identificador, indice):
    linha = pega_linha(registrador)
    dados_mem = cash[linha][indice][3:]
    return dados_mem


def read_hit(cash, registrador, identificador, opc, indice):
    global acertos_cash_I, acertos_cash_D
    if opc == "D":
        acertos_cash_D += 1
    else:
        acertos_cash_I += 1
    linha = pega_linha(registrador)
    linha1 = int(linha, 2)
    val1 = int(cash[linha][0][1])
    val2 = int(cash[linha][1][1])
    cp = int(registrador, 2)

    dados_mem = pega_data_cash(cash, registrador, identificador, indice)
    dados_mem1 = ""
    for i in dados_mem:
        dados_mem1 += hex32(int(i,2)) + ","
    dados_mem1 = dados_mem1.rstrip(",")

    dados = str(dados_mem1).replace(" ", "").lstrip("[").rstrip("]")
    coluna3 = f"ID={hex24(int(identificador, 2))},DATA=" + "{" + dados + "}"
    coluna2 = f"{opc}_read_hit [{linha1}]->[{indice}]".ljust(ajuste)
    arquivo_saida.write(f"{hex32(cp)}:\t{coluna2}{coluna3}\n")


def read_miss(cash, registrador, opc): #opc I D
    global erros_cash_D, erros_cash_I
    if opc == "D":
        erros_cash_D += 1
    else:
        erros_cash_I += 1
    linha1 = int(pega_linha(registrador), 2)
    linha = pega_linha(registrador)
    val1 = int(cash[linha][0][1])
    val2 = int(cash[linha][1][1])
    cp = int(registrador, 2)
    if cash[linha][0][2] != None:
        idem1 = int(cash[linha][0][2], 2)
    if cash[linha][1][2] != None:
        idem2 = int(cash[linha][1][2], 2)
    if cash[linha][0][2] == None:
        idem1 = 0
    if cash[linha][1][2] == None:
        idem2 = 0
    
    coluna3 = "[0]{" + f"VAL={val1},AGE={0},ID={hex24(idem1)}" + "}" + ",[1]{" + f"VAL={val2},AGE={0},ID={hex24(idem2)}" + "}\n"
    coluna2 = f"{opc}_read_miss [{linha1}]".ljust(ajuste)
    arquivo_saida.write(f"{hex32(cp)}:\t{coluna2}{coluna3}")


def substitui_LRU(cash, registrador, campo):
    registrador = registrador
    identificador = pega_id(registrador)
    linha = pega_linha(registrador)
    dados_mem = busca_mem(registrador)
    
    linha_atual = cash[linha]
    
    if not linha_atual[0][1] and not linha_atual[1][1]:
        read_miss(cash, registrador, campo)
        cash[linha] = processamento(0, linha_atual, identificador, dados_mem)
    elif linha_atual[0][1] and identificador != linha_atual[0][2] and not linha_atual[1][1]:
        read_miss(cash, registrador, campo)
        cash[linha] = processamento(1, linha_atual, identificador, dados_mem)
    elif linha_atual[1][1] and identificador != linha_atual[1][2] and not linha_atual[0][1]:
        read_miss(cash, registrador, campo)
        cash[linha] = processamento(0, linha_atual, identificador, dados_mem)

    elif linha_atual[1][1] and linha_atual[0][1] and identificador != linha_atual[1][2] and identificador != linha_atual[0][2]:
        read_miss(cash, registrador, campo)
        if linha_atual[1][0] > linha_atual[0][0]:
            cash[linha] = processamento(1, linha_atual, identificador, dados_mem)
        if linha_atual[1][0] < linha_atual[0][0]:
            cash[linha] = processamento(0, linha_atual, identificador, dados_mem) # adicionar a condição de igual
    
    elif linha_atual[0][1] and identificador == linha_atual[0][2]:
        read_hit(cash, registrador, identificador, campo, 0)
    elif linha_atual[1][1] and identificador == linha_atual[1][2]:
        read_hit(cash, registrador, identificador, campo, 1)


def main_cash(cash, registrador, campo):
    linha = pega_linha(registrador)
    idem = pega_id(registrador)
    substitui_LRU(cash, registrador, campo)


def write_miss(cash, registrador, opc):
    global erros_cash_D
    erros_cash_D += 1
    linha1 = int(pega_linha(registrador), 2) 
    linha = pega_linha(registrador)
    val1 = int(cash[linha][0][1])
    val2 = int(cash[linha][1][1])
    cp = int(registrador, 2)
    if cash[linha][0][2] != None:
        idem1 = int(cash[linha][0][2], 2)
    if cash[linha][1][2] != None:
        idem2 = int(cash[linha][1][2], 2)
    if cash[linha][0][2] == None:
        idem1 = 0
    if cash[linha][1][2] == None:
        idem2 = 0
    
    coluna3 = "[0]{" + f"VAL={val1},AGE={0},ID={hex24(idem1)}" + "}" + "[1]{" + f"VAL={val2},AGE={0},ID={hex24(idem2)}" + "}\n"
    coluna2 = f"{opc}_write_miss [{linha1}]".ljust(ajuste)
    arquivo_saida.write(f"{hex32(cp)}:\t{coluna2}{coluna3}")


def write_hit(cash, registrador, identificador, opc, indice):
    global acertos_cash_D
    acertos_cash_D += 1
    linha = pega_linha(registrador)
    linha1 = int(linha, 2)
    val1 = int(cash[linha][0][1])
    val2 = int(cash[linha][1][1])
    cp = int(registrador, 2)

    dados_mem = pega_data_cash(cash, registrador, identificador, indice)
    dados_mem1 = ""
    for i in dados_mem:
        dados_mem1 += hex32(int(i,2)) + ","
    dados_mem1 = dados_mem1.rstrip(",")

    dados = str(dados_mem1).replace(" ", "").lstrip("[").rstrip("]")
    coluna3 = f"ID={hex24(int(identificador, 2))},DATA=" + "{" + dados + "}"
    coluna2 = f"{opc}_write_hit [{linha1}]->[{indice}]".ljust(ajuste)
    arquivo_saida.write(f"{hex32(cp)}:\t{coluna2}{coluna3}\n")

def substitui_write(cash, registrador, campo):
    registrador = registrador
    identificador = pega_id(registrador)
    linha = pega_linha(registrador)
    dados_mem = busca_mem(registrador)
    
    linha_atual = cash[linha]
    
   
    
    if linha_atual[0][1] and identificador == linha_atual[0][2]:
        write_hit(cash, registrador, identificador, campo, 0)
    elif linha_atual[1][1] and identificador == linha_atual[1][2]:
        write_hit(cash, registrador, identificador, campo, 1)
    else:
        write_miss(cash, registrador, campo)


def percent_hit():
    total_I = acertos_cash_I + erros_cash_I
    total_D = acertos_cash_D + erros_cash_D
    perc_I = acertos_cash_I * 100 / total_I
    perc_D = acertos_cash_D * 100 / total_D
    arquivo_saida.write("[CASH]\nD_hit_rate: %.2f \nI_hit_rate: %.2f\n"%(perc_D, perc_I))
##########################################################################################################################

############################################################### INTERRUPCAO POR SOFTWARE #####################################################
var_checa_desvios = False
var_desvioativo = False

lista_pega_nao_masc= list()
def printa_write_depois():
    global lista_pega_nao_masc
    for i in lista_pega_nao_masc:
        substitui_write(cash_dado, bin(i)[2:].zfill(32), "D")
    lista_pega_nao_masc = list()


# interrupacao nao mascarada

def interrupt_nao_masc(registradores, instrucao, memoria):
    SPv = int(registradores[sp], 2)
    lista_pega_nao_masc.append(SPv)
    objmemoria.setRegistradorMemoria(SPv, pc, 4); SPv -= 4
    lista_pega_nao_masc.append(SPv)
    objmemoria.setRegistradorMemoria2(SPv, cr); SPv -= 4 
    lista_pega_nao_masc.append(SPv)
    objmemoria.setRegistradorMemoria2(SPv, ipc); SPv -= 4
    objregistradores.setRegistradorSP(SPv)
    
    
# interrupacao mascarada
checa_dog = False
def interrupt_masc(registradores, instrucao, memoria):
    if registradores[sr][ie] == "1":
        if var_desvioativo:
            SPv = int(registradores[sp], 2)
            objmemoria.setRegistradorMemoria2(SPv, pc) ; SPv -= 4
            objmemoria.setRegistradorMemoria2(SPv, cr)   ; SPv -= 4
            objmemoria.setRegistradorMemoria2(SPv, ipc)  ; SPv -= 4
            objregistradores.setRegistradorSP(SPv)
        else:
            SPv = int(registradores[sp], 2)
            objmemoria.setRegistradorMemoria(SPv, pc, 4) ; SPv -= 4
            objmemoria.setRegistradorMemoria2(SPv, cr)   ; SPv -= 4
            objmemoria.setRegistradorMemoria2(SPv, ipc)  ; SPv -= 4
            objregistradores.setRegistradorSP(SPv)


def inter_dog(registradores, instrucao, memoria):
    global checa_dog
    arquivo_saida.write("[HARDWARE INTERRUPTION 1]\n")
    if checa_dog:
        SPv = int(registradores[sp], 2)
        substitui_write(cash_dado,bin(SPv)[2:].zfill(32) , "D")
        objmemoria.setRegistradorMemoria2(SPv, pc) ; SPv -= 4
        substitui_write(cash_dado, bin(SPv)[2:].zfill(32), "D")
        objmemoria.setRegistradorMemoria2(SPv, cr)   ; SPv -= 4
        substitui_write(cash_dado, bin(SPv)[2:].zfill(32), "D")
        objmemoria.setRegistradorMemoria2(SPv, ipc)  ; SPv -= 4
        objregistradores.setRegistradorSP(SPv)
    else:
        SPv = int(registradores[sp], 2)
        objmemoria.setRegistradorMemoria(SPv, pc, 4) ; SPv -= 4
        objmemoria.setRegistradorMemoria2(SPv, cr)   ; SPv -= 4
        objmemoria.setRegistradorMemoria2(SPv, ipc)  ; SPv -= 4
        objregistradores.setRegistradorSP(SPv)



def interrupt_masc_1(registradores, instrucao, memoria):
    if registradores[sr][ie] == "1":
        SPv = int(registradores[sp], 2)
        objmemoria.setRegistradorMemoria(SPv, pc, 4) ; SPv -= 4
        objmemoria.setRegistradorMemoria2(SPv, cr)   ; SPv -= 4
        objmemoria.setRegistradorMemoria2(SPv, ipc)  ; SPv -= 4
        objregistradores.setRegistradorSP(SPv)
        

#Operação de retorno de interrupção (reti)
def reti(registradores):
    global cpu_pc
    p = cpu_pc - 4
    Spv = int(registradores[sp], 2)
    Spv += 4 ; objmemoria.setMemoriaNoRegister(Spv, ipc)
    Spv += 4 ; objmemoria.setMemoriaNoRegister(Spv, cr)
    Spv += 4 ; objmemoria.setMemoriaNoRegister(Spv, pc)
    cpu_pc = int(registradores[pc], 2)
    objregistradores.setRegistradorSP(Spv)

    coluna2 = f"reti".ljust(ajuste)
    coluna3 = f"IPC=MEM[{hex32(Spv-8)}]={hex32(int(registradores[ipc], 2))},CR=MEM[{hex32(Spv-4)}]={hex32(int(registradores[cr], 2))},PC=MEM[{hex32(Spv)}]={hex32(int(registradores[pc], 2))}"
    arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}\n")
    
    
# operacoes de ajuste e limpeza de bit
def op_ajuste_limpeza(instrucao):  # (cbr) -- Tipo F / (sbr) -- Tipo F
    opex_F = lReadF(instrucao)[15]
    p = int(registradores_32[pc],2)
    z = int(zRead(instrucao), 2)
    x = int(xRead(instrucao), 2)
    if opex_F == "0":
        #Operação de limpeza de bit de registrador (cbr) -- Tipo F
        objregistradores.set_bit_registrador(z, x, "0")
        nome = "cbr"
    elif opex_F == "1":
        # Operação de ajuste de bit de registrador (sbr) -- Tipo F
        objregistradores.set_bit_registrador(z, x, "1")
        nome = "sbr"
    coluna2 = f"{nome} {nomeRgsmin(registradores_32, z)}[{x}]".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32, z)}={hex32(int(registradores_32[z], 2))}\n"
    arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}")
    

# instrucao de interrupcao
def inT(registradores, instrucao):
    global cpu_pc
    p = int(registradores[pc],2)
    antigo_cr = registradores[cr]
    interrupt_nao_masc(registradores, instrucao, memoria_32kbys)
    if int(lReadS(instrucao), 2) != 0:
        registradores[cr] = lReadS(instrucao).zfill(32)
        registradores[ipc] = registradores[pc]
        registradores[pc] = bin(int("0x0000000C", 16))[2:].zfill(32)
        cpu_pc = int("0x0000000C", 16)
        coluna2 = f"int {c_int32(int(lReadS(instrucao), 2)).value}".ljust(ajuste)
        coluna3 = f"CR={hex32(int(antigo_cr, 2))},PC={hex32(p + 4)}\n"
        msg = f"[SOFTWARE INTERRUPTION]\n"
        arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}{msg}")
        printa_write_depois()

    else:
        registradores[cr] = lReadS(instrucao).zfill(32)
        registradores[pc] = "0".zfill(32)
        cpu_pc = 0
        coluna2 = f"int {c_int32(int(lReadS(instrucao), 2)).value}".ljust(ajuste)
        coluna3 = f"CR={hex32(0)},PC={hex32(0)}\n"
        arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}")


def instrucao_invalida(registradores, instrucao, memoria):
    global cpu_pc
    p = cpu_pc
    codigo_pc = "0x00000004"
    if registradores[sr][ie] == "1":
        interrupt_masc_1(registradores, instrucao, memoria)
        objregistradores.setRegistradorSR(sr, veri, veri, veri, veri, veri, True)
        atual = registradores[ir][:6]
        registradores[cr] = atual.zfill(32)
        registradores[ipc] = registradores[pc]
        registradores[pc] = bin(int(codigo_pc, 16))[2:]
        cpu_pc = int(codigo_pc, 16)
        arquivo_saida.write(f'[INVALID INSTRUCTION @ {hex32(p - 4)}]\n[SOFTWARE INTERRUPTION]\n')



lista_div_zero = []
def divisao_por_zero(registradores, instruncao): # II unidade
    global cpu_pc
    if registradores[sr][ie] == "1" and registradores[sr][zd] == "1":
        interrupt_masc_1(registradores, instruncao, memoria_32kbys)
        registradores[cr] = "0".zfill(32) 
        registradores[ipc] = registradores[pc]
        cpu_pc = int("0x00000008", 16)
        msg = "[SOFTWARE INTERRUPTION]\n"
        arquivo_saida.write(msg)
        
    
    


################################################################[HARDWARE INTERRUPTION]######################################################

def fuction_watch_dog():
    global watch_dog_var, cpu_pc, var_checa_desvios, var_desvioativo, checa_dog
    if watch_dog_var > 0:
        watch_dog_var -= 1
    elif registradores_32[sr][ie] == "1":
        inter_dog(registradores_32, registradores_32[ir], memoria_32kbys)
        registradores_32[cr] = bin(int("0xE1AC04DA", 16))[2:]
        registradores_32[ipc] = registradores_32[pc]
        cpu_pc = int("0x00000010", 16)
        obj_interrupt_hwe.set_watch_dog("0".zfill(32), False)
        
        checa_dog = False
        
        
def hardware_4(controle):
    global ciclo_fpu, cpu_pc, var_checa_desvios, var_desvioativo

    ciclo_fpu = 0
    p = (cpu_pc) - 4
    for i in range(controle):
        if i == controle - 1:
            var_checa_desvios = True
        instrucaoAtual = pegaIstrucaoMemoria(memoria_32kbys, cpu_pc, cpu_pc + 4)
        objregistradores.setRegistradorIR(instrucaoAtual)
        objregistradores.setRegistradorPC(cpu_pc)
        testesInstrucoes(registradores_32, instrucaoAtual, memoria_32kbys)
        cpu_pc += 4
        p += 4
    
    interrupt_masc(registradores_32, registradores_32[ir], memoria_32kbys)
    registradores_32[cr] = bin(int("0x01EEE754", 16))[2:]
    registradores_32[ipc] = bin(p)[2:]
    cpu_pc = int(0x0000001C)
    var_checa_desvios = False
    var_desvioativo = False
    if obj_interrupt_hwe.get_watch_dog()[0] == "1":
        fuction_watch_dog()


def hardware_3 (controle):
    global cpu_pc, ciclo_fpu, var_checa_desvios, var_desvioativo
    endereco_pc = 0
    for i in range(controle):
        if i == (controle - 1):
            endereco_pc = cpu_pc
            var_checa_desvios = True
        instrucaoAtual = pegaIstrucaoMemoria(memoria_32kbys, cpu_pc, cpu_pc + 4)
        objregistradores.setRegistradorIR(instrucaoAtual)
        objregistradores.setRegistradorPC(cpu_pc)
        cpu_pc = int(registradores_32[pc], 2) + 4
        testesInstrucoes(registradores_32, instrucaoAtual, memoria_32kbys)
        if obj_interrupt_hwe.get_watch_dog()[0] == "1":
            fuction_watch_dog()

    if controle == 0:
        endereco_pc = cpu_pc

    interrupt_masc(registradores_32, registradores_32[ir], memoria_32kbys)
    
  
    registradores_32[ipc] = bin(endereco_pc)[2:].zfill(32)

    registradores_32[cr] = bin(int("0x01EEE754", 16))[2:]
    
    ciclo_fpu = 0
    cpu_pc = int(0x00000018)
    var_checa_desvios = False
    var_desvioativo = False
    

def nop_fpu():
    pass


def add_fpu():
    hardware_3(ciclo_fpu)
    registradores_hwe[fpu_z]  = ieee_754(float(int(registradores_hwe[fpu_x], 2) + int(registradores_hwe[fpu_y], 2))).zfill(32)
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)
    arquivo_saida.write("[HARDWARE INTERRUPTION 3]\n")

def sub_fpu():
    hardware_3(ciclo_fpu)
    registradores_hwe[fpu_z]  = ieee_754(extrai_ieee_754(registradores_hwe[fpu_x]) - extrai_ieee_754(ieee_754(float(int(registradores_hwe[fpu_y], 2)))))
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)
    arquivo_saida.write("[HARDWARE INTERRUPTION 3]\n")
    

def mul_fpu():
    hardware_3(ciclo_fpu)
    if int(0x24e69595) <= int(registradores_hwe[fpu_x], 2):
        x = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_x], 2)))[0]
    else:
        x = int(registradores_hwe[fpu_x], 2)

    if int(0x24e69595) <= int(registradores_hwe[fpu_y], 2):
        y = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_y], 2)))[0]
    else:
        y = int(registradores_hwe[fpu_y], 2)

    registradores_hwe[fpu_z]  = bin(int(struct.pack(">f", x * y).hex(), 16))[2:].zfill(32)
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)
    arquivo_saida.write("[HARDWARE INTERRUPTION 3]\n")


def div_fpu():
    global cpu_pc
    hardware_3(ciclo_fpu)
    if int(0x24e69595) <= int(registradores_hwe[fpu_x], 2):
        x = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_x], 2)))[0]
    else:
        x = int(registradores_hwe[fpu_x], 2)

    if int(0x24e69595) <= int(registradores_hwe[fpu_y], 2):
        y = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_y], 2)))[0]
    else:
        y = int(registradores_hwe[fpu_y], 2)

    if y != 0:
        registradores_hwe[fpu_z]  = bin(int(struct.pack(">f", x / y).hex(), 16))[2:].zfill(32)
        obj_interrupt_hwe.set_FPU_4("0" * 32, False)
        arquivo_saida.write("[HARDWARE INTERRUPTION 3]\n")
    else:
        arquivo_saida.write("[HARDWARE INTERRUPTION 2]\n")
        obj_interrupt_hwe.set_st("1")
        cpu_pc = (0x00000014)
       
     
def mov_x_fpu():
    hardware_4(1)
    registradores_hwe[fpu_x] = registradores_hwe[fpu_z]
    arquivo_saida.write("[HARDWARE INTERRUPTION 4]\n")
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)
    

def mov_y_fpu():
    hardware_4(1)
    registradores_hwe[fpu_y] = registradores_hwe[fpu_z]
    arquivo_saida.write("[HARDWARE INTERRUPTION 4]\n")
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)


def teto():
    hardware_4(1)
    if int(0x24e69595) <= int(registradores_hwe[fpu_x], 2):
        z = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_z], 2)))[0]
    else:
        z = int(registradores_hwe[fpu_z], 2)
    registradores_hwe[fpu_z] = bin(ceil(z))[2:].zfill(32)
    arquivo_saida.write("[HARDWARE INTERRUPTION 4]\n")
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)
    

def piso():
    hardware_4(1)
    if int(0x24e69595) <= int(registradores_hwe[fpu_x], 2):
        z = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_z], 2)))[0]
    else:
        z = int(registradores_hwe[fpu_z], 2)
    registradores_hwe[fpu_z] = bin(math.floor(z))[2:].zfill(32)
    arquivo_saida.write("[HARDWARE INTERRUPTION 4]\n")
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)


def arredondamento():
    hardware_4(1)
    if int(0x24e69595) <= int(registradores_hwe[fpu_x], 2):
        z = struct.unpack(">f", struct.pack(">i", int(registradores_hwe[fpu_z], 2)))[0]
    else:
        z = int(registradores_hwe[fpu_z], 2)
    registradores_hwe[fpu_z] = bin(arredondamento_n(z))[2:].zfill(32)
    obj_interrupt_hwe.set_opcode()
    arquivo_saida.write("[HARDWARE INTERRUPTION 4]\n")
    obj_interrupt_hwe.set_FPU_4("0" * 32, False)


def hardware_2():
    global ciclo_fpu, cpu_pc
    hardware_3(1)
    obj_interrupt_hwe.set_opcode()
    obj_interrupt_hwe.set_st("1")
    cpu_pc = int(0x00000014)
    arquivo_saida.write("[HARDWARE INTERRUPTION 2]\n")
    

def op_code_fpu(registradores):
    op_code = lRead_fpu(registradores[4])

    switch = {
        "00000" : nop_fpu,
        "00001" : add_fpu,
        "00010" : sub_fpu,
        "00011" : mul_fpu,
        "00100" : div_fpu,
        "00101" : mov_x_fpu,
        "00110" : mov_y_fpu,
        "00111" : teto,
        "01000" : piso,
        "01001" : arredondamento
    }
    
    v = switch.get(op_code, hardware_2)
    v()


def function_FPU(mem, registrador_z, comando):
    
    global ciclo_fpu, verifica_x, verifica_y
    if mem >= int(0x80808880) and mem <= int(0x80808880) + 3 and comando[0] == "s":
        obj_interrupt_hwe.set_FPU_x(registrador_z)
        verifica_x = True
    elif mem >=  int(0x80808884) and mem <= int(0x80808884) + 3 and comando[0] == "s":
        obj_interrupt_hwe.set_FPU_y(registrador_z)
        verifica_y = True
    elif mem >= int(0x80808888) and mem <= int(0x80808888) + 3 and comando[0] == "s":
        obj_interrupt_hwe.set_FPU_z(registrador_z)
    elif mem >=  int(0x8080888C) and mem <= int(0x8080888C) + 3 and comando[0] == "s":
        obj_interrupt_hwe.set_FPU_4(registrador_z, True)
        if registradores_32[sr][ie] == "1":
            ciclo_fpu = conta_ciclo()
            op_code_fpu(registradores_hwe)
     
bytes_terminal = list()

def terminal(mem, registrador):
    obj_interrupt_hwe.set_out(registrador)
    bytes_terminal.append(registrador[25:])


def print_terminal():
    global bytes_terminal
    arquivo_saida.write("[TERMINAL]\n")
    s = ""
    for i in bytes_terminal:
        s += chr(int(i, 2))
    
    if s[::-1][0:1] == "\n":
        arquivo_saida.write(f"{s}\n")
    else:
        arquivo_saida.write(f"{s}")


# Operação de atribuição imediata (mov) (Sem extensão de sinal)
def mov(registradores, instrucao):
    concatenacao = xRead(instrucao) + yRead(instrucao) + lRead(instrucao)
    registradores[int(zRead(instrucao), 2)] = concatenacao.zfill(32)
    # escrita
    
    registradorcol2 = nomeRgsmin(registradores_32, int(zRead(instrucao), 2))
    asse = str(f"mov {registradorcol2},{int(concatenacao,2)}".ljust(ajuste))
    rgis = nomeRgsMai(registradores_32, int(zRead(instrucao), 2) )
    arquivo_saida.write(f"{hex32(int(registradores_32[29],2))}:\t{asse}{rgis}={hex32(int(concatenacao, 2))}\n")


# Operação de atribuição imediata (movs) (Com extensão de sinal)
def movS(registradores, instrucao):
    concatenacao = xRead(instrucao) + yRead(instrucao) + lRead(instrucao)
    campo_x = xRead(instrucao)
    Rz = int(zRead(instrucao), 2)
    registradores[Rz] = (11 * campo_x[0]) + concatenacao
    registradores = registradores
    # escrita
    regiscol3 = nomeRgsMai(registradores, Rz)
    operacao = c_int32(int(registradores[Rz], 2)).value
    registradorcol2 = nomeRgsmin(registradores, int(zRead(instrucao), 2))
    asse = str(f"movs {registradorcol2},{operacao}".ljust(ajuste))
    arquivo_saida.write(f"{hex32(int(registradores_32[29],2))}:\t{asse}{regiscol3}={hex32(int(registradores[Rz], 2))}\n")


# Funcao: Operação de adição com registradores (add)
def add(registradores, instrucao):
    # operacao principal
    Rx = registradores[int(xRead(instrucao), 2)]
    Ry = registradores[int(yRead(instrucao), 2)]
    Rz = int(zRead(instrucao), 2)
    registradores[Rz] = bin(int(Rx, 2) + int(Ry, 2))[2:]
    # campos afetados
    if registradores[Rz][0] == "b":
        registradores[Rz] = registradores[Rz][1:]
    if len(registradores[Rz]) >= 33:
        s = registradores[Rz][::-1]
        CY = int(s[32], 2) == 1
        registradores[Rz] = s[:32][::-1]
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(Rx[0], 2) == int(Ry[0], 2)) and (
                int(registradores[Rz][0], 2) != int(Rx[0], 2))
    else:
        s = registradores[Rz].zfill(32)
        registradores[Rz] = s
        CY = False
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(Rx[0], 2) == int(Ry[0], 2)) and (
                int(registradores[Rz][0], 2) != int(Rx[0], 2))
    objregistradores.setRegistradorSR(sr,ZN,veri,SN,OV,CY,veri)
    
    rx = int(xRead(instrucao), 2)
    ry = int(yRead(instrucao), 2)
    regscol2 = f"add {nomeRgsmin(registradores_32, Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
    regscol3 = f"{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}+{nomeRgsMai(registradores_32, ry)}="
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{regscol2}{regscol3}{hex32(int(registradores_32[Rz],2))},SR={hex32((int(registradores_32[sr],2)))}\n")


# operacao de subtracao de registradores
def sub(registradores, instrucao):
    # operacao principal
    Rx = registradores[int(xRead(instrucao), 2)]
    Ry = registradores[int(yRead(instrucao), 2)]
    Rz = int(zRead(instrucao), 2)
    registradores[Rz] = bin(int(Rx, 2) - int(Ry, 2))[2:]
    # campos afetados
    CY = False
    s = registradores[Rz] 
    if registradores[Rz][0] == "b":
        s = registradores[Rz][1:]
        CY = True
    if len(s) >= 33:
        s = s[::-1]
        CY = int(s[32]) == 1
        registradores[Rz] = s[:32][::-1]
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(Rx[0], 2) != int(Ry[0], 2)) and (
                int(registradores[Rz][0], 2) != int(Rx[0], 2))
    else:
        registradores[Rz] = s.zfill(32)
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(Rx [0],2) != int(Ry[0], 2)) and (
                int(registradores[Rz][0],2) != int(Rx[0],2))
    
    objregistradores.setRegistradorSR(sr,ZN, veri, SN, OV, CY, veri)
    rx = int(xRead(instrucao), 2)
    ry = int(yRead(instrucao), 2)
    regstrcol2 = f"sub {nomeRgsmin(registradores_32, Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste) 
    regscol3 = f"{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}-{nomeRgsMai(registradores_32, ry)}={hex32(int(registradores[Rz],2))}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{regstrcol2}{regscol3},SR={hex32(int(registradores_32[sr], 2))}\n")


# Operação de multiplicacaoo com registradores (mul) - sem sinal
def mul(registradores, instrucao):
    # operacao principal
    Rx = chamaIndiciesDeR(registradores, instrucao, "x") # alterei a forma mecanica pela funcao
    Ry = registradores[int(yRead(instrucao), 2)]
    Rz = int(zRead(instrucao), 2)
    Rl = int((lRead(instrucao)[6:]), 2)
    mult = bin(int(Rx, 2) * int(Ry, 2))[2:]
    if mult[0] == "b":
        mult = mult[1:]
    if len(mult) <= 64:
        mult = mult.zfill(64)
        if Rl == 0:
            registradores[Rl] = "0".zfill(32)
        else:
            registradores[Rl] = mult[:32]

        registradores[Rz] = mult[32:]
        # campos afetados
        ZN = int(registradores[Rl] + registradores[Rz], 2) == 0  # campos afetados
        CY = int(registradores[Rl], 2) != 0
    else:
        
        mult = mult[::-1][:64][::-1]
        registradores[Rl] = mult[:32]
        registradores[Rz] = mult[32:64]
        # campos afetados
        ZN = int(registradores[Rl] + registradores[Rz], 2) == 0  # campos afetados
        CY = int(registradores[Rl], 2) != 0
    
    objregistradores.setRegistradorSR(sr, ZN, veri, veri, veri, CY, veri)
    rx = int(xRead(instrucao), 2)
    ry = int(yRead(instrucao), 2)
    coluna2 = f"mul {nomeRgsmin(registradores_32,Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32,Rl)}:{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}*{nomeRgsMai(registradores_32, ry)}={hex64(int(registradores[Rl] + registradores[Rz], 2))}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# Operacao de deslocamento para esquerda (sll) logico sem sinal
def sll(registradores, instrucao):
    Ry = registradores[int(yRead(instrucao), 2)]
    Rz = registradores[int(zRead(instrucao), 2)]
    Rl = int(lRead(instrucao)[6:], 2)
    desloca = bin(int(Rz + Ry, 2) << (Rl + 1))[2:]
    if len(desloca) <= 64:
        desloca = desloca.zfill(64)
        registradores[int(zRead(instrucao), 2)] = desloca[:32]
        registradores[int(xRead(instrucao), 2)] = desloca[32:]
        # campos afetados
        ZN = int(registradores[int(zRead(instrucao), 2)] + registradores[int(xRead(instrucao), 2)], 2) == 0
        CY = int(registradores[int(zRead(instrucao), 2)]) != 0
        
    else:
        desloca = desloca[::-1][:64][::-1]
        registradores[int(zRead(instrucao), 2)] = desloca[:32]
        registradores[int(xRead(instrucao), 2)] = desloca[32:64]
        # campos afetados
        ZN = int(registradores[int(zRead(instrucao), 2)] + registradores[int(xRead(instrucao), 2)], 2) == 0
        CY = int(registradores[int(zRead(instrucao), 2)]) != 0
    objregistradores.setRegistradorSR(sr,ZN,veri,veri,veri,CY,veri)
    ry = int(yRead(instrucao), 2)
    rz = int(zRead(instrucao), 2)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"sll {nomeRgsmin(registradores_32,rz)},{nomeRgsmin(registradores_32,rx)},{nomeRgsmin(registradores_32, ry)},{int(lRead(instrucao)[6:], 2)}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32,rz)}:{nomeRgsMai(registradores_32, rx)}={nomeRgsMai(registradores_32, rz)}:{nomeRgsMai(registradores_32, ry)}<<{(Rl + 1)}={hex64(int(Rz + Ry, 2) * 2 ** (Rl + 1))}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# Operação de multiplicação com registradores (muls) com sinal
def muls(registradores, instrucao):
    Rx = c_int64(int(chamaIndiciesDeR(registradores, instrucao, "x"),2)).value
    Ry = c_int64(int(chamaIndiciesDeR(registradores, instrucao, "y"),2)).value
    Rl = int(lRead(instrucao)[6:], 2)
    Rz = int(zRead(instrucao), 2)
    mult = c_uint(Rx * Ry).value
    mulsing = bin(mult)[2:] 
    if mulsing[0] == "b":
        mulsing = mulsing[1:]
    if len(mulsing) <= 64:
        mulsing = extende64Sinal(mulsing)
        registradores[Rl] = mulsing[:32]
        registradores[Rz] = mulsing[32:]
        # campos afetados
        ZN = int(registradores[Rl] + registradores[Rz], 2) == 0
        OV = int(registradores[Rl], 2) != 0
    else:
        mulsing  = extende64Sinal(mulsing[::-1][:64][::-1])
        registradores[Rl], registradores[Rz]  = mulsing[:32], mulsing[32:64]
        # campos afetados
        ZN = int(registradores[Rl] + registradores[Rz], 2) == 0
        OV = int(registradores[Rl], 2) != 0
    objregistradores.setRegistradorSR(sr,ZN,veri,veri,OV,veri,veri)
    ry = int(yRead(instrucao), 2)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"muls {nomeRgsmin(registradores_32, Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
    coluna3  = f"{nomeRgsMai(registradores_32, Rl)}:{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32,rx)}*{nomeRgsMai(registradores_32, ry)}={bin_hex(mulsing)}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# operacao de deslocamento para esquerda - aritmetico com sinal
def sla(registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rx = int(xRead(instrucao), 2)
    string_Rz = chamaIndiciesDeR(registradores, instrucao, "z")
    string_Ry = chamaIndiciesDeR(registradores, instrucao, "y")
    Rl = int(lRead(instrucao)[7:11], 2)
    desloca = bin(c_int32(int(string_Rz + string_Ry, 2) << (Rl+1)).value)[2:]
    if len(desloca) <= 64:
        if desloca[0] == "b":
            desloca = desloca[1:]
        desloca = desloca.zfill(64)
        registradores[Rz], registradores[Rx] = desloca[:32], desloca[32:]
        # campos afetados
        ZN, OV = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    else:
       
        desloca = desloca[::-1][:64][::-1]
        registradores[Rz], registradores[Rx] = desloca[:32], desloca[32:64]
        # campos afetados
        ZN, OV = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    objregistradores.setRegistradorSR(sr, ZN,veri,veri,OV,veri,veri)
    ry = int(yRead(instrucao), 2)
    rz = int(zRead(instrucao), 2)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"sla {nomeRgsmin(registradores_32,rz)},{nomeRgsmin(registradores_32,rx)},{nomeRgsmin(registradores_32, ry)},{int(lRead(instrucao)[7:12], 2)}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32,rz)}:{nomeRgsMai(registradores_32, rx)}={nomeRgsMai(registradores_32, rz)}:{nomeRgsMai(registradores_32, ry)}<<{Rl + 1}={bin_hex(desloca)}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


#  Operacaoo de divisao com registradores (divs) sem sinal
def div(registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rl = int(lRead(instrucao)[6:], 2)
    
    Ry = int(chamaIndiciesDeR(registradores, instrucao, "y"), 2)
    Rx = int(chamaIndiciesDeR(registradores, instrucao, "x"), 2)
    if Ry != 0:
        
        resto = bin(Rx % Ry)[2:].zfill(32)
        divisao = bin(Rx // Ry)[2:].zfill(32)
        registradores[Rl], registradores[Rz] = resto, divisao
        # campos afetados
        ZN, ZD, CY = int(registradores[Rz], 2) == 0, False, int(registradores[Rl], 2) != 0
        objregistradores.setRegistradorSR(sr, ZN, ZD, veri, veri, CY, veri)
        rx = int(xRead(instrucao),2)
        ry = int(yRead(instrucao),2)
        coluna2 = f"div {nomeRgsmin(registradores_32,Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rl)}={nomeRgsMai(registradores_32, rx)}%{nomeRgsMai(registradores_32, ry)}={hex32(int(resto,2))},{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{nomeRgsMai(registradores_32, ry)}={hex32(int(divisao))}"
        arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")
        
    else:
        
        # campos afetados
        
        objregistradores.setRegistradorSR(sr, veri, True, veri, veri, veri, veri)
        rx = int(xRead(instrucao),2)
        ry = int(yRead(instrucao),2)
        coluna2 = f"div {nomeRgsmin(registradores_32,Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rl)}={nomeRgsMai(registradores_32, rx)}%{nomeRgsMai(registradores_32, ry)}={hex32(int(registradores[Rl],2))},{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{nomeRgsMai(registradores_32, ry)}={hex32(int(registradores[Rz], 2))}"
        arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2)) }:\t{coluna2}{coluna3},SR={hex32(int(registradores[sr],2))}\n")
        divisao_por_zero(registradores_32, registradores[ir])
        

# Operacao de deslocamento para a direita (srl) - logico sem sinal
def srl(registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rx = int(xRead(instrucao), 2)
    regisRz = chamaIndiciesDeR(registradores, instrucao, "z")
    regisRy = chamaIndiciesDeR(registradores, instrucao, "y")
    Rl = int(lRead(instrucao)[7:11], 2)
    operacao = bin(int(regisRz + regisRy, 2) >> (Rl + 1))[2:]
    if len(operacao) <= 64:
        operacao = operacao.zfill(64)
        registradores[Rz], registradores[Rx] = operacao[:32], operacao[32:]
        # campos afetados
        ZN, CY = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    else:
        operacao = operacao[::-1][:64][::-1]
        registradores[Rz], registradores[Rx] = operacao[:32], operacao[32:]
        ZN, CY = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    objregistradores.setRegistradorSR(sr, ZN, veri, veri,veri, CY, veri)
    ry = int(yRead(instrucao), 2)
    rz = int(zRead(instrucao), 2)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"srl {nomeRgsmin(registradores_32,rz)},{nomeRgsmin(registradores_32,rx)},{nomeRgsmin(registradores_32, ry)},{Rl}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32,rz)}:{nomeRgsMai(registradores_32, rx)}={nomeRgsMai(registradores_32, rz)}:{nomeRgsMai(registradores_32, ry)}>>{Rl + 1}={hex64(int(operacao, 2))}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# operacao de divisao com registradores (divs) - com sinal
def divs(registradores, instrucao):
    Rl = int(lRead(instrucao)[7:11], 2)
    Rz = int(zRead(instrucao), 2)
    Ry = c_int32(int(chamaIndiciesDeR(registradores, instrucao, "y"), 2)).value
    Rx = c_int32(int(chamaIndiciesDeR(registradores, instrucao, "x"), 2)).value
    if Ry != 0:
        resto = bin(c_int32(Rx % Ry).value)[2:]
        divisao = bin(c_int32(Rx // Ry).value)[2:]
        if resto[0] == "b" :
            resto = resto[1:]
            resto = extende32Sinal(resto)
            
        if divisao[0] == "b":
            divisao = divisao[1:]
            divisao = extende32Sinal(divisao)

        resto = resto.zfill(32)
        divisao = divisao.zfill(32)
        
        registradores[Rl], registradores[Rz] = resto, divisao
        # campos afetados
        ZN, ZD, OV = int(registradores[Rz], 2) == 0, False, int(registradores[Rl], 2) != 0
        objregistradores.setRegistradorSR(sr,ZN,ZD,veri,OV,veri,veri)
        rx = int(xRead(instrucao),2)
        ry = int(yRead(instrucao),2)
        coluna2 = f"divs {nomeRgsmin(registradores_32,Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rl)}={nomeRgsMai(registradores_32, rx)}%{nomeRgsMai(registradores_32, ry)}={hex32(int(resto,2))},{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{nomeRgsMai(registradores_32, ry)}={hex32(int(divisao))}"
        arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2)) }:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")
    else:
        # campos afetados
        divisao_por_zero(registradores, instrucao)
        #msg = "[SOFTWARE INTERRUPTION]\n"
        rx = int(xRead(instrucao),2)
        ry = int(yRead(instrucao),2)
        coluna2 = f"divs {nomeRgsmin(registradores_32,Rl)},{nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32, rx)},{nomeRgsmin(registradores_32, ry)}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rl)}={nomeRgsMai(registradores_32, rx)}%{nomeRgsMai(registradores_32, ry)}={hex32(int(registradores[Rl],2))},{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{nomeRgsMai(registradores_32, ry)}={hex32(int(registradores[Rz], 2))}"
        arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2)) }:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")
        
        

# Operacao de deslocamento para direita (sra) - aritmetico com sinal
def sra(registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rx = int(xRead(instrucao), 2)
    Rl = int(lRead(instrucao)[6:], 2)
    concatena = c_int64(int(chamaIndiciesDeR(registradores, instrucao, "z") + chamaIndiciesDeR(registradores, instrucao, "y"), 2)).value
    operacao = bin(c_int64(concatena >> (Rl + 1)).value)[2:]
    if operacao[0] == "b":
        operacao = operacao[1:]
        operacao = extende64Sinal(operacao)
    if len(operacao) <= 64:
        operacao = operacao.zfill(64)
        
        registradores[Rz], registradores[Rx] = operacao[:32], operacao[32:]
        # campos afetados
        ZN, OV = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    else:
        operacao = operacao[::-1][:64][::-1].zfill(32)
        registradores[Rz], registradores[Rx] = operacao[:32], operacao[32:64]
        # campos afetados
        ZN, OV = int(registradores[Rz] + registradores[Rx], 2) == 0, int(registradores[Rz], 2) != 0
    # atribuicao dos campos afetados nas variaveis globais
    objregistradores.setRegistradorSR(sr,ZN,veri,veri,OV,veri,veri)
    ry = int(yRead(instrucao), 2)
    rz = int(zRead(instrucao), 2)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"sra {nomeRgsmin(registradores_32,rz)},{nomeRgsmin(registradores_32,rx)},{nomeRgsmin(registradores_32, ry)},{Rl}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32,rz)}:{nomeRgsMai(registradores_32, rx)}={nomeRgsMai(registradores_32, rz)}:{nomeRgsMai(registradores_32, ry)}>>{Rl+1}={bin_hex(operacao)}"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# operacao de comparacao com registradores (cmp)
def cmP(registradores, instrucao):
    Rx, Ry = int(chamaIndiciesDeR(registradores, instrucao, "x"), 2) ,int(chamaIndiciesDeR(registradores, instrucao, "y"), 2)
    stringRx, stringRy = chamaIndiciesDeR(registradores, instrucao, "x"), chamaIndiciesDeR(registradores, instrucao, "y")
    cmpa = bin(c_int32(Rx - Ry).value)[2:]
    if "b" in cmpa:
        cmpa = cmpa[1:]
        cmpa = extende32Sinal(cmpa)
        cmpa = cmpa[0] + cmpa
    if len(cmpa) <= 32:
        cmpa = cmpa.zfill(32)
        # campos afetados
        ZN = int(cmpa, 2) == 0
        SN = int(cmpa[0], 2) == 1
        OV = (int(stringRx[0], 2) != int(stringRy[0], 2))and (int(cmpa[0], 2) != int(stringRx[0], 2))
        CY = False
    else:
        #campos afetados
        cmpa = cmpa[::-1][:33]
        CY = int(cmpa[32], 2) == 1
        ZN = int(cmpa, 2) == 0
        SN = int(cmpa[31], 2) == 1
        OV = (int(stringRx[0], 2) != int(stringRy[0], 2)) and (int(cmpa[31], 2) != int(stringRx[0], 2))
    #atribuicao dos campos afetados nas variaveis globais
    
    objregistradores.setRegistradorSR(sr,ZN,veri,SN,OV,CY,veri)
    coluna2 = f"cmp {nomeRgsmin(registradores_32, int(xRead(instrucao), 2))},{nomeRgsmin(registradores_32, int(yRead(instrucao), 2))}".ljust(ajuste)
    coluna3 = f"SR={hex32(int(registradores_32[sr], 2))}"
    arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3}\n")


# funcao operadores logicos
def funcao_OP_logicos(registradores, instrucao, comando):
    Rz = int(zRead(instrucao), 2)
    Rx = int(chamaIndiciesDeR(registradores, instrucao, "x"), 2)
    Ry = int(chamaIndiciesDeR(registradores, instrucao, "y"), 2)
    global arquivo_saida
    if comando == "anD":#And
        registradores[Rz] = bin(Rx & Ry)[2:].zfill(32)
        ZN, SN = int(registradores[Rz], 2) == 0, int(registradores[Rz][0], 2) == 1
        objregistradores.setRegistradorSR(sr, ZN, veri, SN, veri, veri, veri)
        coluna2 = f"and {nomeRgsmin(registradores, Rz)},{nomeRgsmin(registradores, int(xRead(instrucao),2))},{nomeRgsmin(registradores, int(yRead(instrucao),2))}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores, Rz)}={nomeRgsMai(registradores,int(xRead(instrucao),2))}&{nomeRgsMai(registradores,int(yRead(instrucao),2))}={hex32(int(registradores[Rz], 2))},SR={hex32(int(registradores[sr],2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3}\n")
    elif comando == "oR":
        registradores[Rz] = bin(Rx | Ry)[2:].zfill(32)
        ZN, SN = int(registradores[Rz], 2) == 0, int(registradores[Rz][0], 2) == 1
        objregistradores.setRegistradorSR(sr, ZN, veri, SN, veri, veri, veri)
        coluna2 = f"or {nomeRgsmin(registradores, Rz)},{nomeRgsmin(registradores, int(xRead(instrucao),2))},{nomeRgsmin(registradores, int(yRead(instrucao),2))}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores, Rz)}={nomeRgsMai(registradores,int(xRead(instrucao),2))}|{nomeRgsMai(registradores,int(yRead(instrucao),2))}={hex32(int(registradores[Rz], 2))},SR={hex32(int(registradores[sr],2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3}\n")
        
    elif comando == "noT":
        operacao = bin((c_uint32(~(int(chamaIndiciesDeR(registradores, instrucao, "x"), 2))).value) )[2:]
        if "b" in operacao:
            operacao = extende32Sinal(operacao[1:])
        registradores[Rz] = operacao
        ZN, SN = int(registradores[Rz], 2) == 0, int(registradores[Rz][0], 2) == 1
        objregistradores.setRegistradorSR(sr, ZN, veri, SN, veri, veri, veri)
        coluna2 = f"not {nomeRgsmin(registradores, Rz)},{nomeRgsmin(registradores, int(xRead(instrucao),2))}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores, Rz)}=~{nomeRgsMai(registradores,int(xRead(instrucao),2))}={hex32(int(registradores[Rz], 2))},SR={hex32(int(registradores[sr],2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3}\n")


    elif comando == "xor":
        registradores[Rz] = bin(Rx ^ Ry)[2:].zfill(32)
        ZN, SN = int(registradores[Rz], 2) == 0, int(registradores[Rz][0], 2) == 1
        objregistradores.setRegistradorSR(sr, ZN, veri, SN, veri, veri, veri)
        coluna2 = f"xor {nomeRgsmin(registradores, Rz)},{nomeRgsmin(registradores, int(xRead(instrucao),2))},{nomeRgsmin(registradores, int(yRead(instrucao),2))}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores, Rz)}={nomeRgsMai(registradores,int(xRead(instrucao),2))}^{nomeRgsMai(registradores,int(yRead(instrucao),2))}={hex32(int(registradores[Rz], 2))},SR={hex32(int(registradores[sr],2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3}\n")


#operacao bit a bit (and)
def anD(registradores, instrucao):
    return funcao_OP_logicos(registradores, instrucao, "anD")


#operacao bit a bit (or)
def oR(registradores, instrucao):
    return funcao_OP_logicos(registradores, instrucao, "oR")


# operacao bit a bit (not)
def noT(registradores, instrucao):
    return funcao_OP_logicos(registradores, instrucao, "noT")


# operacao bit a bit (xor)
def xor(registradores, instrucao):
    return  funcao_OP_logicos(registradores, instrucao, "xor")


# operacao de adicao imediata(addi)
def addi(registradores, instrucao):
    # operacao principal
    stringRx = chamaIndiciesDeR(registradores, instrucao, "x")
    Rx, Rl, Rz = int(xRead(instrucao), 2), lReadF(instrucao), int(zRead(instrucao), 2)
    registradores[Rz] = bin(int(stringRx, 2) + int(((Rl[0] * 16) + Rl) , 2))[2:]
    # campos afetados
    if len(registradores[Rz]) >= 33:
        s = registradores[Rz][::-1]
        CY = int(s[32], 2) == 1
        registradores[Rz] = s[:32][::-1]
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(registradores[Rx][0], 2) == int(Rl[0], 2)) and (int(registradores[Rz][0], 2) != int(registradores[Rx][0], 2))
    else:
        registradores[Rz] = registradores[Rz].zfill(32)
        CY, ZN = False, int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = (int(registradores[Rx][0], 2) == int(Rl[0], 2)) and (
                    int(registradores[Rz][0], 2) != int(registradores[Rx][0], 2))
    # atribuicao dos campos afetados nas variaveis globais
    objregistradores.setRegistradorSR(sr, ZN, veri, SN, OV, CY, veri)
    rx = int(xRead(instrucao), 2)
    regscol2 = f"addi {nomeRgsmin(registradores_32, Rz)},{nomeRgsmin(registradores_32, rx)},{int(((Rl[0]* 16) + Rl) , 2)}".ljust(ajuste)
    regscol3 = f"{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}+{hex32(int(((Rl[0]* 16) + Rl) , 2))}={hex32(int(registradores[Rz], 2))}"
    arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{regscol2}{regscol3},SR={hex32((int(registradores_32[sr],2)))}\n")


# Operação de subtração imediata (subi)
def subi(registradores, instrucao):
    # operacao principal
    stringRx = chamaIndiciesDeR(registradores, instrucao, "x")
    Rx = int(xRead(instrucao), 2)
    Rz = int(zRead(instrucao), 2)
    Rl = lReadF(instrucao)
    registradores[Rz] = bin(c_int32(int(stringRx.zfill(32), 2) - int((Rl[0] * 16) + Rl, 2)).value)[2:]
    # campos afetados
    if(registradores[Rz][0] == "b"):
        registradores[Rz] = registradores[Rz][1:]
    if len(registradores[Rz]) >= 33:
        
        s = registradores[Rz][::-1]
        CY = int(s[32], 2) == 1
        registradores[Rz] = s[:32][::-1]
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = int(registradores[Rx][0], 2) != int(Rl, 2) and int(registradores[Rz][0], 2) != int(registradores[Rx][0], 2)
    else:
        
        registradores[Rz] = registradores[Rz].zfill(32)
        CY = False
        ZN = int(registradores[Rz], 2) == 0
        SN = int(registradores[Rz][0], 2) == 1
        OV = int(registradores[Rx][0], 2) != int(Rl[0], 2) and int(registradores[Rz][0], 2) != int(registradores[Rx][0], 2)
    # atribuicao dos campos afetados nas variaveis globais
    objregistradores.setRegistradorSR(sr, ZN, veri, SN, OV, CY, veri)
    rx = int(xRead(instrucao), 2)
    regstrcol2 = f"subi {nomeRgsmin(registradores_32, Rz)},{nomeRgsmin(registradores_32, rx)},{c_int32(int((Rl[0] * 16) + Rl, 2)).value}".ljust(ajuste) 
    regscol3 = f"{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}-{hex32(int((Rl[0] * 16) + Rl, 2))}={hex32(int(registradores[Rz],2))}"
    arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{regstrcol2}{regscol3},SR={hex32(int(registradores[sr], 2))}\n")


#operacao de multiplcacao imediata muli - com sinal
def muli(registradores, instrucao):
    Rx = chamaIndiciesDeR(registradores, instrucao, "x")
    Rl = lReadF(instrucao)
    Rz = int(zRead(instrucao), 2)
    mulsing = bin(c_int32(int(Rx, 2) * int((Rl[0] * 16) + Rl, 2)).value)[2:]
    
    if len(mulsing) <= 64:
        if "b" in mulsing:
            mulsing = mulsing[1:]
            mulsing = extende64Sinal(mulsing)
        mulsing = mulsing.zfill(64)
        registradores[Rz] = mulsing[32:]
        checaover = mulsing[:32]
        # campos afetados
        ZN = int(registradores[Rz], 2) == 0
        OV = int(checaover, 2) != 0
    else:
        manipular  = extende64Sinal(mulsing[::-1][:64][::-1])
        registradores[Rz] = manipular[:32]
        checaover = manipular[32:64]
        # campos afetados
        ZN = int(registradores[Rz], 2) == 0
        OV = int(checaover, 2) != 0
    # atribuicao dos campos afetados nas variaveis globais
    objregistradores.setRegistradorSR(sr,ZN , veri, veri, OV, veri, veri)
    rx = int(xRead(instrucao), 2)
    coluna2 = f"muli {nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32,rx)},{c_int32(int((Rl[0] * 16) + Rl, 2)).value}".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registradores_32, Rz)}={nomeRgsMai(registradores_32, rx)}*{hex32(int((Rl[0] * 16) + Rl, 2))}={hex32(int(registradores[Rz], 2))}"
    arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")


# operacao de divisao imediata (divi) com sinal
def divi(registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rl = c_int32(int((lReadF(instrucao)[0] * 16) + lReadF(instrucao), 2)).value
    Rx = c_int32(int(chamaIndiciesDeR(registradores, instrucao, "x"), 2)).value
    
    saidaRl = bin(Rl)[2:]
    if saidaRl[0] == "b":
        saidaRl = saidaRl[1:]
        saidaRl = extende32Sinal(saidaRl)
    else:
        saidaRl = saidaRl.zfill(32)

    if Rl != 0:
        if Rl > 0 and Rx > 0:
            operacao = bin(c_uint(Rx // Rl).value)[2:]
        if Rl < 0 and Rx < 0:
            operacao = bin(c_uint(Rx // Rl).value)[2:]
        else:
            operacao = bin(c_uint((Rx // Rl)).value)[2:]

        if operacao[0] == "b":
            operacao = operacao[1:]
            operacao = extende32Sinal(operacao)
        registradores[Rz] = operacao.zfill(32)
        ZN, ZD, OV = int(registradores[Rz], 2) == 0, False, False
        # campos afetados
        objregistradores.setRegistradorSR(sr, ZN, ZD, veri, OV, veri, veri)
        rx = int(xRead(instrucao),2)
        coluna2 = f"divi {nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32,rx)},{c_int32(Rl).value}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{hex32(c_uint(Rl).value)}={bin_hex(registradores[Rz])}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores_32[sr],2))}\n")
       
    else:
        # campos afetados
        objregistradores.setRegistradorSR(sr, veri, True, veri, veri, veri, veri)
        rx = int(xRead(instrucao),2)
        coluna2 = f"divi {nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32,rx)},{c_int32(Rl).value}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}/{bin_hex(saidaRl)}={bin_hex(registradores[Rz])}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores[sr],2))}\n")
        divisao_por_zero(registradores_32, registradores[ir])
    # atribuicao dos campos afetados nas variaveis globais


# operacao de modulo imediato(modi)
def modi (registradores, instrucao):
    Rz = int(zRead(instrucao), 2)
    Rx = c_int32(int(chamaIndiciesDeR(registradores, instrucao, "x"), 2)).value
    Rl = c_int32(int((lReadF(instrucao)[0] * 16) + lReadF(instrucao), 2)).value
    if (int(Rl), 2) != 0:
        if Rx > 0 and Rl > 0:
            operacao = bin(Rx % Rl)[2:].zfill(32)
        if Rx < 0 and Rl > 0:
            Rx = Rx * (-1)
            op = Rx % Rl
            operacao = bin(c_uint(op * (-1)).value)[2:]
            operacao = extende32Sinal(operacao)
        if Rx > 0 and Rl < 0:
            Rl = Rl * (-1)
            op = Rx % Rl
            operacao = bin(c_uint(op * (-1)).value)[2:]
            operacao = extende32Sinal(operacao)
        if Rx < 0 and Rl < 0:
            op = Rx % Rl
            operacao = bin(c_uint(op).value)[2:]
            operacao = extende32Sinal(operacao)

        registradores[Rz] = operacao
        #campos afetados
        ZN, ZD, OV = int(registradores[Rz], 2) == 0 , False , False
        objregistradores.setRegistradorSR(sr, ZN, ZD, veri, OV, veri, veri)
        rx = int(xRead(instrucao),2)
        coluna2 = f"modi {nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32,rx)},{c_int32(Rl).value}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}%{hex32(c_uint(Rl).value)}={hex32(int(registradores[Rz], 2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores[sr],2))}\n")
    else:
        objregistradores.setRegistradorSR(sr, veri, True, veri, veri, veri, veri)
        rx = int(xRead(instrucao),2)
        coluna2 = f"modi {nomeRgsmin(registradores_32,Rz)},{nomeRgsmin(registradores_32,rx)},{c_int32(Rl).value}".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registradores_32,Rz)}={nomeRgsMai(registradores_32, rx)}%{hex32(c_uint(Rl).value)}={hex32(int(registradores[Rz], 2))}"
        arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna2}{coluna3},SR={hex32(int(registradores[sr],2))}\n{msg}")
        divisao_por_zero(registradores_32, registradores[ir])


# operacao de comparacao imediata
def cmpi(registradores, instrucao):
    Rx, Rl = int(chamaIndiciesDeR(registradores, instrucao, "x"), 2), (lReadF(instrucao)[0] * 16) + lReadF(instrucao)
    stringRx = chamaIndiciesDeR(registradores, instrucao, "x")
    cmpI = bin(c_int32(Rx - int(Rl, 2)).value)[2:]
    if cmpI[0] == "b":
        cmpI = cmpI[1:]
        cmpI = extende32Sinal(cmpI)
        cmpI = cmpI[0] + cmpI
    
    if len(cmpI) <= 32:
        cmpI = cmpI.zfill(32)
        # campos afetados
        ZN = int(cmpI, 2) == 0
        SN = int(cmpI[0], 2) == 1
        OV = (int(stringRx[0], 2) != int(lReadF(instrucao)[0], 2)) and (int(cmpI[0], 2) != int(stringRx[0], 2))
        CY = False
    else:
        # campos afetados
        cmpI = cmpI[::-1][:33]
        CY = int(cmpI[32], 2) == 1
        ZN = int(cmpI, 2) == 0
        SN = int(cmpI[31], 2) == 1
        OV = (int(stringRx[0], 2) != int(lReadF(instrucao)[0], 2)) and (int(cmpI[31], 2) != int(stringRx[0], 2))
    # atribuicao dos campos afetados nas variaveis globais
    objregistradores.setRegistradorSR(sr, ZN, veri, SN, OV, CY, veri)
    coluna1 = f"cmpi {nomeRgsmin(registradores, int(xRead(instrucao), 2))},{c_int32(int(Rl, 2)).value}".ljust(ajuste)
    arquivo_saida.write(f"{hex32(int(registradores[pc], 2))}:\t{coluna1}SR={hex32(int(registradores[sr], 2))}\n")


# funcao que escreve intrucoes de escrita e leitura da memoria
def escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem):
    switch = {
        "l8"  : hex8(int(registrador[Rz], 2)) ,
        "l16" : hex16(int(registrador[Rz], 2)),
        "l32" : hex32(int(registrador[Rz], 2)),
        "s8"  : hex8(int(registrador[Rz], 2)),
        "s16" : hex16(int(registrador[Rz], 2)),
        "s32" : hex32(int(registrador[Rz], 2))
    }
    
    hex_person = switch[comando]
    
    # escreve instrucoes l no arquivo
    if comando[0] == "l": 
        coluna2 = f"{comando} {nomeRgsmin(registrador, Rz)},[{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}]".ljust(ajuste)
        coluna3 = f"{nomeRgsMai(registrador, Rz)}=MEM[{hex32(mem)}]={hex_person}\n"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}")
    
    # ecerve instruncoes r no arquivo
    elif comando[0] == "s":
        coluna2 = f"{comando} [{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}],{nomeRgsmin(registrador, Rz)}".ljust(ajuste)
        coluna3 = f"MEM[{hex32(mem)}]={nomeRgsMai(registrador, Rz)}={hex_person}\n"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}")


# escreve nas operacoes de leitura
def ler_l(comando, instrucao, registrador, mem, numero, Rz, Rx, Rl):
    guarda = ""
    if numero == var_fpu_x:
        guarda = registrador[fpu_x]
    elif numero == var_fpu_y:
        guarda = registrador[fpu_y]
    elif numero == var_fpu_z:
        guarda = registrador[fpu_z]
    elif numero == var_fpu_op:
        guarda = registrador[fpu_control]
    elif var_fpu_4 == numero:
        guarda = registrador[fpu_control]
    
    registradores_32[Rz] = guarda
    
    
    
    switch = {
        "l8"  : hex8(int(guarda, 2)),
        "l16" : hex16(int(guarda, 2)),
        "l32" : hex32(int(guarda, 2))
    }

    hex_person = switch[comando]
    coluna2 = f"{comando} {nomeRgsmin(registrador, Rz)},[{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}]".ljust(ajuste)
    coluna3 = f"{nomeRgsMai(registrador, Rz)}=MEM[{hex32(mem)}]={hex_person}\n"
    arquivo_saida.write(f"{hex32(int(registradores_32[pc], 2))}:\t{coluna2}{coluna3}")
        

# funcao de leitura e escrita de bits na memoria
def leitura_escritaDaMemoria(registrador, memoria, instrucao, comando):
    Rz = int(zRead(instrucao), 2)
    Rx = chamaIndiciesDeR(registrador, instrucao, "x")
    Rl = lReadF(instrucao)[0] * 16 + lReadF(instrucao)
    mem = int(Rx, 2) + int(Rl, 2)
    global watch_dog_var
    # ler (l)

    if comando == "l8":
        mem = mem
        if mem == endereco_watch_dog:
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
        
        elif mem in lista_fpu:
            ler_l(comando, instrucao, registradores_hwe, mem, mem, Rz, Rx, Rl)
        else:
            operacao = procuraIndiceMemoria(memoria, mem , mem + 1)
            registrador[Rz] = operacao
            main_cash(cash_dado, bin(mem)[2:].zfill(32), "D")
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            
    elif comando == "l16":
        mem = mem << 1
        if mem == endereco_watch_dog:
            
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
       
        elif mem in lista_fpu:
            ler_l(comando, instrucao, registradores_hwe, mem, mem, Rz, Rx, Rl)
            

        else:
            main_cash(cash_dado, bin(mem)[2:].zfill(32), "D")
            registrador[Rz] = procuraIndiceMemoria(memoria, mem, mem + 2)

            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            
        
    elif comando == "l32":
        mem = mem << 2
        if mem == endereco_watch_dog:
            
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
        
        elif mem in lista_fpu:
            ler_l("l32", instrucao, registradores_hwe, mem, mem, Rz, Rx, Rl)
            

        else:
            registrador[Rz] = procuraIndiceMemoria(memoria, mem, mem + 4) # fazer a escrita
            main_cash(cash_dado, bin(mem)[2:].zfill(32), "D")
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            
        
    # escreve (s)
    elif comando == "s8":
        if mem == endereco_watch_dog:
            
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
        
        elif (var_fpu_4 == mem) or (var_fpu_op == mem) or (var_fpu_x == mem) or (var_fpu_y == mem) or (var_fpu_z == mem):
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            function_FPU(mem, registrador[Rz], "s8")
        
        elif mem == var_terminal:
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            terminal(mem, registrador[Rz])
        
        else:
            substitui_write(cash_dado, bin(mem)[2:].zfill(32), "D")
            memoria = funcaoEscrevenaRgistradorMemoria(registrador[Rz], memoria, mem, 8)
            registrador[Rz] = procuraIndiceMemoria(memoria, mem , mem)
            coluna2 = f"s8 [{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}],{nomeRgsmin(registrador, Rz)}".ljust(ajuste)
            coluna3 = f"MEM[{hex32(mem)}]={nomeRgsMai(registrador, Rz)}={hex8(int(memoria[mem], 2))}\n"
            arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}")

    elif comando == "s16":
        mem = mem << 1
        if mem == endereco_watch_dog:
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
        
        elif (var_fpu_4 == mem) or (var_fpu_op == mem) or (var_fpu_x == mem) or (var_fpu_y == mem) or (var_fpu_z == mem):
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            function_FPU(mem, registrador[Rz], comando)
        
        else:
            substitui_write(cash_dado, bin(mem)[2:].zfill(32), "D")
            memoria = funcaoEscrevenaRgistradorMemoria(registrador[Rz], memoria, mem, 16)
            coluna2 = f"s16 [{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}],{nomeRgsmin(registrador, Rz)}".ljust(ajuste)
            coluna3 = f"MEM[{hex32(mem)}]={nomeRgsMai(registrador, Rz)}={hex16(int(converteListastr(memoria[mem : mem + 2]), 2))}\n"
            arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}")
            
       
    elif comando == "s32":
        mem = mem << 2
        if mem == endereco_watch_dog:
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            obj_interrupt_hwe.set_watch_dog(registrador[Rz], True)
            watch_dog_var = int(registrador[Rz][1:], 2)
        
        elif mem in lista_fpu:
            escreve_arq_lS(comando, registrador, Rz, Rx, Rl, instrucao, mem)
            function_FPU(mem, registrador[Rz], comando)
            
        else:
            substitui_write(cash_dado, bin(mem)[2:].zfill(32), "D")
            memoria = funcaoEscrevenaRgistradorMemoria(registrador[Rz], memoria, mem, 32)
            coluna2 = f"s32 [{nomeRgsmin(registrador,int(xRead(instrucao), 2))}+{int(Rl, 2)}],{nomeRgsmin(registrador, Rz)}".ljust(ajuste)
            coluna3 = f"MEM[{hex32(mem)}]={nomeRgsMai(registrador, Rz)}={hex32(int(converteListastr(memoria[mem : mem + 4]), 2))}\n"
            arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}")
            
    # atribuicao global


# operacao de leitura de 8 bits da memoria
def l8 (registrador, memoria, instrucao):
    leitura_escritaDaMemoria(registrador, memoria, instrucao, "l8")

#operacao de leitura de 16 bits
def l16(registrador, memoria, instrucao):
     leitura_escritaDaMemoria(registrador, memoria, instrucao, "l16")

#operacao de leitura de 32 bits
def l32(registrador, memoria, instrucao):
    leitura_escritaDaMemoria(registrador, memoria, instrucao, "l32")

# operacao de escrita de 8 bits
def s8(registrador, memoria, instrucao):
    leitura_escritaDaMemoria(registrador, memoria, instrucao, "s8")

# operacao de escrita de 16 bits
def s16(registrador, memoria, instrucao):
    leitura_escritaDaMemoria(registrador, memoria, instrucao, "s16")

# operacao de escrita de 32 bits
def s32(registrador, memoria, instrucao):
    leitura_escritaDaMemoria(registrador, memoria, instrucao, "s32")

# seta a condicao e os nomes das funcoes
def setacondicao(instrucao, registradores):
    c  = opRead(instrucao)
    ZN = registradores[sr][zn]
    ZD = registradores[sr][zd]
    SN = registradores[sr][sn]
    OV = registradores[sr][ov]
    IV = registradores[sr][iv]
    CY = registradores[sr][cy]
    condicao = False
    if c == "101010":
        condicao = CY == "0"
        nome = "bae"
    if c == "101011":
        condicao = (ZN == "0" and CY == "0")
        nome = "bat"
    if c == "101100":
        condicao = (ZN == "1" or CY == "1")
        nome = "bbe"
    if c == "101101":
        condicao = CY == "1"
        nome = "bbt"
    if c == "101110":
        condicao = ZN == "1"
        nome = "beq"
    if c == "101111":
        condicao = SN == OV
        nome = "bge"
    if c == "110000":
        condicao = (ZN == '0' and SN == OV)
        nome = "bgt"
    if c == "110001":
        condicao = IV == "1"
        nome = "biv"
    if c == "110010":
        condicao = (ZN == '1' or SN != OV)
        nome = "ble"
    if c == "110011":
        condicao =  (SN != OV)
        nome = "blt"
    if c == "110100":
        condicao = ZN == "0"
        nome = "bne"
    if c == "110101":
        condicao = IV == "0"
        nome = "bni"
    if c == "110110":
        condicao = ZD == "0"
        nome = "bnz"
    if c == "111000":
        condicao = ZD == "1"
        nome = "bzd"
    if c == "110111":
        condicao = True
        nome = "bun"

    return (condicao, nome)


# escreve no arquivo as condicionais


# executa os desvios condicionais 
def condicionais(instrucao, registradores):
    global cpu_pc, var_checa_desvios, var_desvioativo, watch_dog_var, checa_dog
    
    soma = 4 + (c_int32(int(lReadS(instrucao)[0]*6 + lReadS(instrucao), 2)).value << 2)
    numero = c_int32(int(lReadS(instrucao)[0]*6 + lReadS(instrucao), 2)).value
    p = cpu_pc

    desviosCond = setacondicao(instrucao, registradores)
    condicao, nome = desviosCond[0], desviosCond[1]
   
    if condicao:
        cpu_pc += soma
        
    else:
        cpu_pc += 4 
    
    cpu_pc -= 4
    if opRead(instrucao) == "111111": #olhar o que é o CR
        if int(lReadS((objregistradores.get32Registradores(ir))), 2) == 0: # INTERRUPCAO POR SOFTWARE
            cpu_pc  = 0
            objregistradores.setRegistradorPC(cpu_pc)
            assem = str(f"{nome} {numero}".ljust(ajuste))
            arquivo_saida.write(f"{hex32(p-4)}:\t{assem}CR={hex32(0)},PC={hex32(cpu_pc)}\n")
        else:
            inT(registradores, instrucao)
    else:
        objregistradores.setRegistradorPC(cpu_pc)
        if var_checa_desvios:
            var_desvioativo = True
        elif watch_dog_var == 0 and obj_interrupt_hwe.get_watch_dog()[0] == "1" and registradores_32[sr][ie] == "1":
            checa_dog = True
        assem = str(f"{nome} {numero}".ljust(ajuste))
        arquivo_saida.write(f"{hex32(p-4)}:\t{assem}PC={hex32(int(registradores[pc], 2))}\n")


def call_F(instrucao, memoria, registrador):
    global cpu_pc
    p = int(registrador[pc], 2)
    SPv = int(registrador[sp], 2)
    
    objmemoria.setRegistradorMemoria(SPv, pc, 4)
    registrador[sp] = bin(SPv - 4)[2:].zfill(32)
    Rl = int(lReadF(instrucao)[0] * 16 + lReadF(instrucao), 2)
    Rx = int(registrador[int(xRead(instrucao), 2)], 2)
    
    cpu_pc = c_int32(Rx + Rl).value << 2
    
    coluna2 = f"call [{nomeRgsmin(registrador, int(xRead(instrucao), 2))}+{Rl}]".ljust(ajuste)
    coluna3 = f"PC={hex32(cpu_pc)},MEM[{hex32(SPv)}]={hex32(int(converteListastr(memoria[SPv:SPv + 4]), 2))}"
    arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}\n")

    
def call_S(instrucao, memoria, registrador):
    global cpu_pc
    SPv = int(registrador[sp], 2)
    objmemoria.setRegistradorMemoria(int(registrador[sp], 2), pc, 4)

    operacao = bin(int(registrador[sp], 2) - 4 )[2:]
    if operacao[0] == "b":
        operacao = operacao[1:].zfill(32)
    registrador[sp] = operacao

    p = int(registrador[pc], 2)
    Ri = lReadS(instrucao)[0] * 6 + lReadS(instrucao)
    rls = c_int32(int(Ri, 2)).value
    cpu_pc = p + 4 + (c_int32(int(Ri, 2) << 2).value)
    objregistradores.setRegistradorPC(cpu_pc - 4)
    
    coluna2 = f"call {rls}".ljust(ajuste)
    coluna3 = f"PC={hex32(cpu_pc)},MEM[{hex32(SPv)}]={hex32(p + 4)}"
    arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}\n")


def ret (instrucao, memoria, registrador):
    global cpu_pc
    p = int(registrador[pc], 2)
    SP = int(registrador[sp], 2) + 4
    
    objregistradores.setRegistradorSP(SP)
    rsp = int(registrador[sp], 2)

    cpu_pc = int(converteListastr(memoria[rsp: rsp + 4]), 2)
    
    objregistradores.setRegistradorPC(cpu_pc)
    coluna2 = f"ret".ljust(ajuste)
    coluna3 = f"PC=MEM[{hex32(SP)}]={hex32(cpu_pc)}"
    arquivo_saida.write(f"{hex32(p)}:\t{coluna2}{coluna3}\n")


def push (instrucao, memoria, registrador):
    SPv = int(registrador[sp], 2)
    SPv1 = int(registrador[sp], 2)
    v = lRead(instrucao)[:5]
    w = lRead(instrucao)[6:]
    x = xRead(instrucao)
    y = yRead(instrucao)
    z = zRead(instrucao)
    i = v + w + x + y + z
    lista = [v,w,x,y,z]
    coleta_indice = []
    coletahex = []
    for j in lista:
        if int(j, 2) != 0:
            coletahex.append(hex32(c_uint32(int(registrador[int(j,2)], 2)).value))
            coleta_indice.append(int(j,2))
            objmemoria.setRegistradorMemoria2(SPv, int(j,2))
            SPv -= 4
        else:
            break

    objregistradores.setRegistradorSP(SPv)
    
    # prepara indices dos registradores
    minusculos = ""
    maiusculos = ""
    for i in coleta_indice:
        minusculos += nomeRgsmin(registrador, i) + ","
        maiusculos += nomeRgsMai(registrador, i) + ","
    minusculos = minusculos.rstrip(",").ljust(ajuste - 5)
    maiusculos = "{" + maiusculos.rstrip(",") + "}"

    # pega os registradores
    lista_hexas = ""
    for i in coletahex:
        lista_hexas += i + ","
    lista_hexas = "{" + lista_hexas.rstrip(",") + "}"
    if len(coleta_indice) == 0:
        coluna2 = f"push -".ljust(ajuste)
        coluna3 = f"MEM[{hex32(SPv1)}]{lista_hexas}={maiusculos}"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}\n")

    else:
        coluna2 = f"push {minusculos}"
        coluna3 = f"MEM[{hex32(SPv1)}]{lista_hexas}={maiusculos}"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}\n")
        

def poP(instrucao, memoria, registrador):
    SPv = int(registrador[sp], 2)
    SPv1 = int(registrador[sp], 2)
    v = lRead(instrucao)[:5]
    w = lRead(instrucao)[6:]
    x = xRead(instrucao)
    y = yRead(instrucao)
    z = zRead(instrucao)
    
    lista = [v,w,x,y,z]
    coleta_indice = []
    coletahex = []
    
    for j in lista:
        if int(j, 2) != 0:
            SPv += 4
            registrador[int(j,2)] = pegaIstrucaoMemoria(memoria, SPv, SPv + 4)
            coletahex.append(hex32(c_uint32(int(registrador[int(j,2)], 2)).value))
            coleta_indice.append(int(j,2))
            
        else:
            break

    objregistradores.setRegistradorSP(SPv)

    # prepara indices dos registradores
    minusculos = ""
    maiusculos = ""
    for i in coleta_indice:
        minusculos += nomeRgsmin(registrador, i) + ","
        maiusculos += nomeRgsMai(registrador, i) + ","
    minusculos = minusculos.rstrip(",").ljust(ajuste - 4)
    maiusculos = "{" + maiusculos.rstrip(",") + "}"

    # pega os registradores
    lista_hexas = ""
    for i in coletahex:
        lista_hexas += i + ","
    lista_hexas = "{" + lista_hexas.rstrip(",") + "}"
    if len(coleta_indice) == 0:
        coluna2 = f"pop -".ljust(ajuste)
        coluna3 = f"{maiusculos}=MEM[{hex32(SPv1)}]{lista_hexas}"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}\n")

    else:
        coluna2 = f"pop {minusculos}"
        coluna3 = f"{maiusculos}=MEM[{hex32(SPv1)}]{lista_hexas}"
        arquivo_saida.write(f"{hex32(int(registrador[pc], 2))}:\t{coluna2}{coluna3}\n")


def opMls(registradores, instrucao):
    comando = lRead(instrucao)[0:3]
    switcher = {
        "000" : mul,
        "001" : sll,
        "010" : muls,
        "011" : sla,
        "100" : div,
        "101" : srl,
        "110" : divs,
        "111" : sra,
    }
    switcher[comando](registradores, instrucao)


def movNop(registrador, instrucao):
    if int(instrucao, 2) != 0:
        mov(registrador, instrucao)


def testesInstrucoes(registradores, instrucao, memoria):
    instR = opRead(instrucao)
    r, i, m = registradores, instrucao, memoria
    if instR == "000000":
        movNop(r, i)
    elif instR == "000001":
        movS(r, i)
    elif instR == "000010":
        add(r, i)
    elif instR == "000011":
        sub(r,i)
    elif instR == "000100":
        opMls(r, i)
    elif instR == "000101":
        cmP(r, i)
    elif instR == "000110":
        anD(r, i)
    elif instR == "000111":
        oR(r, i)
    elif instR == "001000":
        noT(r, i)
    elif instR == "001001":
        xor(r, i)
    elif instR == "010010":
        addi(r, i)
    elif instR == "010011":
        subi(r, i)
    elif instR == "010100":
        muli(r, i)
    elif instR == "010101":
        divi(r, i)
    elif instR == "010110":
        modi(r, i)
    elif instR == "010111":
        cmpi(r, i)
    elif instR == "011000":
        l8(r, m, i)
    elif instR == "011001":
        l16(r ,m, i)
    elif instR == "011010":
        l32(r, m, i)
    elif instR == "011011":
        s8(r, m , i)
    elif instR == "011100":
        s16(r, m, i)
    elif instR == "011101":
        s32(r, m, i)
    # desvios condicionais
    elif instR == "101010":
        condicionais(i, r)
    elif instR == "101011":
        condicionais(i, r)
    elif instR == "101100":
        condicionais(i, r)
    elif instR == "101101":
        condicionais(i, r)
    elif instR == "101110":
        condicionais(i, r)
    elif instR == "101111":
        condicionais(i, r)
    elif instR == "110000":
        condicionais(i, r)
    elif instR == "110001":
        condicionais(i, r)
    elif instR == "110010":
        condicionais(i, r)
    elif instR ==  "110011":
        condicionais(i, r)
    elif instR == "110100":
        condicionais(i, r)
    elif instR == "110101":
        condicionais(i, r)
    elif instR == "110110":
        condicionais(i, r)
    elif instR == "110111":
        condicionais(i, r)
    elif instR == "111000":
        condicionais(i, r)
    elif instR == "111111":
        inT(r, i)
    # pilha
    elif instR == "011110":
        call_F(i, m, r)
    elif instR == "111001":
        call_S(i, m, r)
    elif instR == "011111":
        ret(i, m, r)
    elif instR == "001010":
        push(i, m, r)
    elif instR == "001011":
        poP(i, m, r)
    elif instR == "100000":
        reti(registradores)
    elif instR == "100001":
        op_ajuste_limpeza(instrucao)
    else:
        instrucao_invalida(r, i, m)

cont_linha = 0
def main():
    arquivo_saida.write("[START OF SIMULATION]\n")
    global cpu_pc, cont_linha
    while True:
        instrucaoAtual = pegaIstrucaoMemoria(memoria_32kbys, cpu_pc, cpu_pc + 4)
        objregistradores.setRegistradorIR(instrucaoAtual)
        objregistradores.setRegistradorPC(cpu_pc)
        cpu_pc = int(registradores_32[pc], 2) + 4
        main_cash(cash_instrucao, registradores_32[pc], "I")
        incrementa_Idade(cash_instrucao, registradores_32)
        if opRead(instrucaoAtual) == "111111" and int(lReadS(instrucaoAtual)[0]*6 + lReadS(instrucaoAtual), 2) == 0:
            inT(registradores_32, instrucaoAtual)
            print_terminal()
            break
        
        else:
            testesInstrucoes(registradores_32, instrucaoAtual, memoria_32kbys)
            if obj_interrupt_hwe.get_watch_dog()[0] == "1":
                fuction_watch_dog()
    percent_hit()
    arquivo_saida.write("[END OF SIMULATION]\n")
    arquivo_saida.close()
    arquivo_entrada1.close()


main()
