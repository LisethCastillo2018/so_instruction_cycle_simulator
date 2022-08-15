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

def set_control_unit(val):
    global cu
    cu = val

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


def execute_store(var='var1'):
    set_mar(icr[var])
    data[mar] = acumulador


def execute_set(value=None, var='var1'):
    set_mar(icr[var])
    if value is None:
        value = int(icr['var2'])
    data[mar] = value


def execute_add():
    # print('*** acumulador: ', acumulador)
    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 + var2)
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE:
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 + var2)

    else:
        valor_acumulador_inicial = acumulador
        var1 = execute_load()
        set_acumulador(valor_acumulador_inicial + var1)


def execute_sub():
    # print('*** acumulador: ', acumulador)
    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 - var2)
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE:
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_acumulador(var1 - var2)

    else:
        valor_acumulador_inicial = acumulador
        var1 = execute_load()
        set_acumulador(valor_acumulador_inicial - var1)


def execute_mul(var='var1'):

    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        execute_load('var2')
        icr['var2'] = NULL_VALUE
        execute_mul()
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE :

        execute_load('var2')
        icr['var2'] = NULL_VALUE
        execute_mul()

    else:

        valor_acumulador_inicial = acumulador
        # print('*** valor_acumulador_inicial: ', valor_acumulador_inicial)
        for i in range(valor_acumulador_inicial-1):
            if i == 0:
                execute_load(var)
            execute_add()


def execute_div(var='var1'):
    
    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        var1 = icr['var1']
        var2 = icr['var2']

        icr['var2'] = var1
        icr['var1'] = var2

        execute_load('var2')
        icr['var2'] = NULL_VALUE
        execute_div()
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE :

        var1 = icr['var1']
        var2 = icr['var2']

        icr['var2'] = var1
        icr['var1'] = var2

        execute_load('var2')
        icr['var2'] = NULL_VALUE
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


def execute_inc():
    execute_load('var1')
    set_acumulador(acumulador + 1)
    execute_store('var1')


def execute_dec():
    execute_load('var1')
    set_acumulador(acumulador - 1)
    execute_store('var1')


def execute_mov():
    execute_load('var1')
    execute_store('var2')
    execute_set(0, 'var1')


def execute_beq():
    initial_value_acumulator = acumulador
    variables = ['var1', 'var2', 'var3']
    for variable in variables:
        if icr[variable] != NULL_VALUE:
            value = execute_load(variable)
            diferencia = initial_value_acumulator - value
            if diferencia == 0:
                execute_set(0, variable)
    set_acumulador(initial_value_acumulator)


""" 
AND D2 D5 D6 - Carga los valores en las direcciones de memoria (los 3 obligatorios), si cada uno es mayor
al valor del acumulador, se actualiza el valor del acumulador con el mayor valor
"""
def execute_and():
    if icr['var1'] != NULL_VALUE and icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:
        variables = ['var1', 'var2', 'var3']
        initial_value_acumulator = acumulador
        bigger_num = acumulador
        validated = True

        for variable in variables:
            value = execute_load(variable)
            """ Verificar que todos los valores sean mayor al del acumulador """
            if initial_value_acumulator >= value:
                validated = False
                break
            """ Registrar el numero mayor """
            if value > bigger_num:
                bigger_num = value

        if validated is False:
            set_acumulador(initial_value_acumulator)
        else:
            set_acumulador(bigger_num)


""" 
AND D2 D5 D6 - Carga los valores en las direcciones de memoria, el valor del acumulador 
es actualizado con el primer valor que se encuentre que sea mayor a él
"""
def execute_or():
    variables = ['var1', 'var2', 'var3']
    initial_value_acumulator = acumulador
    bigger_num = acumulador
    validated = False

    for variable in variables:
        if icr[variable] != NULL_VALUE:
            value = execute_load(variable)
            """ Registrar el numero mayor """
            if value > initial_value_acumulator:
                bigger_num = value
                validated = True
                break

    if validated is False:
        set_acumulador(initial_value_acumulator)
    else:
        set_acumulador(bigger_num)


def execute_print():
    dict_show = {
        'ACC': acumulador,
        'ICR': icr,
        'MAR': mar,
        'MDR': mdr,
        'UC': cu
    }
    value_show = dict_show.get(icr['var1'], None)

    if value_show is not None:
        print(value_show)
    else:
        vars_print = ['var1', 'var2', 'var3']
        for var_print in vars_print:
            if 'D' in icr[var_print]:
                position = int(icr[var_print].replace("D",""))
                print(data[position])


def execute_control_unit():
    if icr['word'] in palabras_instruciones:
        cu_list = {
            INSTRUCTION_ADD: execute_add,
            INSTRUCTION_SUB: execute_sub,
            INSTRUCTION_MUL: execute_mul,
            INSTRUCTION_DIV: execute_div,
            INSTRUCTION_SET: execute_set,
            INSTRUCTION_LOAD: execute_load,
            INSTRUCTION_STORE: execute_store,
            INSTRUCTION_INC: execute_inc,
            INSTRUCTION_DEC: execute_dec,
            INSTRUCTION_MOV: execute_mov,
            INSTRUCTION_BEQ: execute_beq,
            INSTRUCTION_AND: execute_and,
            INSTRUCTION_OR: execute_or,
            INSTRUCTION_SHOW: execute_print,
        }
        function = cu_list.get(icr['word'], None)
        if function is not None:
            function()
            set_control_unit(function)


"""************ INICIO DEL PROGRAMA ************"""

if __name__ == '__main__':
    # Constantes
    NULL_VALUE = 'NULL'
    INSTRUCTION_LOAD = 'LDR'
    INSTRUCTION_ADD = 'ADD'
    INSTRUCTION_SUB = 'SUB'
    INSTRUCTION_MUL = 'MUL'
    INSTRUCTION_DIV = 'DIV'
    INSTRUCTION_STORE = 'STR'
    INSTRUCTION_SET = 'SET'
    INSTRUCTION_SHOW = 'SHW'
    INSTRUCTION_INC = 'INC'
    INSTRUCTION_DEC = 'DEC'
    INSTRUCTION_MOV = 'MOV'
    INSTRUCTION_BEQ = 'BEQ'
    INSTRUCTION_AND = 'AND'
    INSTRUCTION_OR = 'OR'

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
        INSTRUCTION_SHOW,
        INSTRUCTION_INC,
        INSTRUCTION_DEC,
        INSTRUCTION_MOV,
        INSTRUCTION_BEQ,
        INSTRUCTION_AND,
        INSTRUCTION_OR
    ]

    pc = INICIO_INSTRUCCIONES
    icr = None
    mdr = None
    cu = None
    mar = pc
    acumulador = 0
    alu = []

    for i in range(len(get_instruciones_memoria())):
        execute_mdr()
        execute_control_unit()
        mar = pc
