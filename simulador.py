"""
UNIVERSIDAD DEL VALLE
SISTEMAS OPERATIVOS
ESTUDIANTE:
LISETH DAYANA CASTILLO QUIÑONES, CÓD. 1843187
"""
import sys
from utils.file import read_file


def get_instrucion():
    if mar > len(data):
        return None
    else:
        return data[mar]


def get_instruciones_memoria():
    instrucciones = []
    # print(data)
    for val in data:
        if type(val) is dict and val['word'] in palabras_instruciones:
            instrucciones.append(val['word'])
    return instrucciones


def set_mar():
    global mar
    mar = int(icr['var1'].replace("D",""))
    execute_mdr()


def add_alu(val):
    global alu
    alu.append(int(val))


def execute_alu(word):
    if word == INSTRUCTION_ADD:
        return sum(alu)
    return None


def clear_alu():
    global alu
    alu = []


def set_acumulador(val):
    global acumulador
    acumulador = int(val)


def execute_icr(instruccion):
    global icr, pc
    icr = instruccion
    pc += 1


def execute_mdr():
    instruccion = get_instrucion()
    # print('**** instruccion: ', instruccion)
    if instruccion is not None:
        if type(instruccion) is dict and instruccion['word'] in palabras_instruciones:
            execute_icr(instruccion)        
        else: 
            if icr is not None and icr['word'] == INSTRUCTION_STORE:
                data[mar] = acumulador
            elif type(data[mar]) is int:
                set_acumulador(data[mar])

def execute_control_unit():
    if icr['word'] in palabras_instruciones:
        if icr['word'] == INSTRUCTION_ADD:
            add_alu(acumulador)
            set_mar()
            add_alu(acumulador)
            value = execute_alu(icr['word'])
            if value is not None:
                set_acumulador(value)
            clear_alu()
        elif icr['word'] == INSTRUCTION_SET:
            position = int(icr['var1'].replace("D",""))
            data[position] = int(icr['var2'])
        elif icr['word'] in [INSTRUCTION_LOAD, INSTRUCTION_STORE]:
            set_mar()
        elif icr['word'] == INSTRUCTION_SHOW:
            if icr['var1']  == 'ACC':
                print('ACUMULADOR: ', acumulador)
            elif icr['var1'] == 'ICR':
                print('ICR: ', icr)
            elif icr['var1'] == 'MAR':
                print('MAR: ', mar)
            elif 'D' in icr['var1'] and icr['var1'] not in ['MDR', 'UC']:
                position = int(icr['var1'].replace("D",""))
                print(f'D{position}:', data[position])


if __name__ == '__main__':
    # Constantes
    INSTRUCTION_LOAD = 'LDR'
    INSTRUCTION_ADD = 'ADD'
    INSTRUCTION_STORE = 'STR'
    INSTRUCTION_SET = 'SET'
    INSTRUCTION_SHOW = 'SHW'

    # Leer el archivo con las instruciones
    data = read_file()

    palabras_instruciones = [
        INSTRUCTION_LOAD, 
        INSTRUCTION_ADD, 
        INSTRUCTION_STORE,
        INSTRUCTION_SET,
        INSTRUCTION_SHOW
    ]

    pc = int(sys.argv[2])
    icr = None
    mar = pc
    acumulador = 0
    alu = []

    for i in range(len(get_instruciones_memoria())):
        execute_mdr()
        execute_control_unit()
        mar = pc

    # print('\n')
    # print('ESTADO FINAL DE LA MEMORIA RAM: ')
    # print(data)