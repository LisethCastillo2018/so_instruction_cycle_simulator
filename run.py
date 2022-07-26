"""
UNIVERSIDAD DEL VALLE
SISTEMAS OPERATIVOS
ESTUDIANTE:
LISETH DAYANA CASTILLO QUIÑONES, CÓD. 1843187
"""
import sys
from utils.utils import read_file, read_input


def get_memory_data():
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


def set_mar(var):
    global mar
    mar = int(var.replace("D",""))


def set_acumulador(val):
    global acumulador
    acumulador = int(val)


def execute_icr(instruccion):
    global icr, pc
    icr = instruccion
    pc += 1


def execute_mdr():
    global mdr
    mdr = get_memory_data()
    # print('**** instruccion: ', instruccion)
    if mdr is not None:
        if type(mdr) is dict and mdr['word'] in palabras_instruciones:
            execute_icr(mdr)        
                

def execute_load(var='var1'):
    set_mar(icr[var])
    valor = get_memory_data()
    set_acumulador(valor)
    return valor


def excute_store(var='var1'):
    set_mar(icr[var])
    data[mar] = acumulador


def execute_set():
    position = int(icr['var1'].replace("D",""))
    data[position] = int(icr['var2'])


def execute_add():
    # print('*** acumulador: ', acumulador)
    if icr['var2'] != 'NULL' and icr['var3'] != 'NULL':

        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 + var2)
        excute_store('var3')

    elif icr['var2'] != 'NULL':
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 + var2)

    else:
        valor_acumulador_inicial = acumulador
        var1 = execute_load()
        set_acumulador(valor_acumulador_inicial + var1)


def execute_sub():
    # print('*** acumulador: ', acumulador)
    if icr['var2'] != 'NULL' and icr['var3'] != 'NULL':

        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 - var2)
        excute_store('var3')

    elif icr['var2'] != 'NULL':
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 - var2)

    else:
        valor_acumulador_inicial = acumulador
        var1 = execute_load()
        set_acumulador(valor_acumulador_inicial - var1)


def execute_mul(var='var1'):

    if icr['var2'] != 'NULL' and icr['var3'] != 'NULL':

        execute_load('var2')
        icr['var2'] = 'NULL'
        execute_mul()
        excute_store('var3')

    elif icr['var2'] != 'NULL' :

        execute_load('var2')
        icr['var2'] = 'NULL'
        execute_mul()

    else:

        valor_acumulador_inicial = acumulador
        # print('*** valor_acumulador_inicial: ', valor_acumulador_inicial)
        for i in range(valor_acumulador_inicial-1):
            if i == 0:
                execute_load(var)
            execute_add()


def execute_div(var='var1'):
    
    if icr['var2'] != 'NULL' and icr['var3'] != 'NULL':

        var1 = icr['var1']
        var2 = icr['var2']

        icr['var2'] = var1
        icr['var1'] = var2

        execute_load('var2')
        icr['var2'] = 'NULL'
        execute_div()
        excute_store('var3')

    elif icr['var2'] != 'NULL' :

        var1 = icr['var1']
        var2 = icr['var2']

        icr['var2'] = var1
        icr['var1'] = var2

        execute_load('var2')
        icr['var2'] = 'NULL'
        execute_div()

    else:

        valor_acumulador_inicial = acumulador
        # print('*** valor_acumulador_inicial: ', valor_acumulador_inicial)
        for i in range(valor_acumulador_inicial-1):
            if acumulador > 0:
                execute_sub()
            else:
                set_acumulador(i)
                break


def execute_control_unit():
    if icr['word'] in palabras_instruciones:
        if icr['word'] == INSTRUCTION_ADD:

            execute_add()

        elif icr['word'] == INSTRUCTION_SUB:

            execute_sub()

        elif icr['word'] == INSTRUCTION_MUL:

            execute_mul()

        elif icr['word'] == INSTRUCTION_DIV:
    
            execute_div()

        elif icr['word'] == INSTRUCTION_SET:

            execute_set()

        elif icr['word'] == INSTRUCTION_LOAD:
            
            execute_load()

        elif icr['word'] == INSTRUCTION_STORE:

            excute_store()

        elif icr['word'] == INSTRUCTION_SHOW:
            
            dict_show = {
                'ACC': acumulador,
                'ICR': icr,
                'MAR': mar,
                'MDR': mdr
            }
            value_show = dict_show.get(icr['var1'], None)

            if value_show is not None:
                return value_show
            elif 'D' in icr['var1'] and icr['var1'] not in ['UC']:
                position = int(icr['var1'].replace("D",""))
                return data[position]


"""************ INICIO DEL PROGRAMA ************"""

if __name__ == '__main__':
    # Constantes
    INSTRUCTION_LOAD = 'LDR'
    INSTRUCTION_ADD = 'ADD'
    INSTRUCTION_SUB = 'SUB'
    INSTRUCTION_MUL = 'MUL'
    INSTRUCTION_DIV = 'DIV'
    INSTRUCTION_STORE = 'STR'
    INSTRUCTION_SET = 'SET'
    INSTRUCTION_SHOW = 'SHW'

    INICIO_INSTRUCCIONES = 1000

    # Leer el archivo con las instruciones
    if len(sys.argv) > 1:
        data = read_file(INICIO_INSTRUCCIONES)
    else:
        data = read_input(INICIO_INSTRUCCIONES)

    palabras_instruciones = [
        INSTRUCTION_LOAD, 
        INSTRUCTION_ADD, 
        INSTRUCTION_SUB,
        INSTRUCTION_MUL,
        INSTRUCTION_DIV,
        INSTRUCTION_STORE,
        INSTRUCTION_SET,
        INSTRUCTION_SHOW
    ]

    pc = INICIO_INSTRUCCIONES
    icr = None
    mdr = None
    mar = pc
    acumulador = 0
    alu = []
    resultado = None

    for i in range(len(get_instruciones_memoria())):
        execute_mdr()
        resultado = execute_control_unit()
        mar = pc

    print(resultado)
