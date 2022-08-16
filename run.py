"""
UNIVERSIDAD DEL VALLE
SISTEMAS OPERATIVOS
ESTUDIANTE:
LISETH DAYANA CASTILLO QUIÑONES, CÓD. 1843187
"""
import sys
from utils.utils import read_file, read_input


""" Obtener valor en memoria de MAR """
def get_memory_data():
    if mar > len(data):
        return None
    else:
        return data[mar]


""" Obtener todas las instrucciones a ejecutar """
def get_memory_instructions():
    instructions = []
    for val in data:
        if type(val) is dict and val['word'] in words_instructions:
            instructions.append(val['word'])
    return instructions


""" Asignar MAR, direccion del dato que se quiere leer """
def set_mar(var):
    global mar
    mar = int(var.replace("D",""))


""" Asignar Acumulador """
def set_accumulator(val):
    global accumulator
    accumulator = int(val)


""" Asignar ultima funcion ejecutada """
def set_control_unit(function):
    global cu
    cu = function


""" Almacenar la instrucción que se está ejecutando """
def execute_icr(instruction):
    global icr, pc
    icr = instruction
    pc += 1


""" Ejecutar MDR """
def execute_mdr():
    global mdr
    mdr = get_memory_data()
    if mdr is not None:
        if type(mdr) is dict and mdr['word'] in words_instructions:
            execute_icr(mdr)        
                

""" 
Load the value in 'var' memory address and puts in accumulator register
"""
def execute_load(var='var1'):
    set_mar(icr[var])
    valor = get_memory_data()
    set_accumulator(valor)
    return valor


"""
Read the value in accumulator register and puts in 'var' memory address
"""
def execute_store(var='var1'):
    set_mar(icr[var])
    data[mar] = accumulator


"""
Store 'value' in 'var' memory address. where 'value' is an immediate, direct or constant value.
"""
def execute_set(value=None, var='var1'):
    set_mar(icr[var])
    if value is None:
        value = int(icr['var2'])
    data[mar] = value


"""
ADDITION - There are three ways: ADD D1 NULL NULL, adds the value in D1 memory address to loaded 
value in accumulator register. ADD D1 D3 NULL Load the value in D1 memory address in the accumulator 
register and add to found value in D3 memory address. ADD D1 D3 D4 same that ADD D1 D3 but puts the result in D4
"""
def execute_add():
    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        var1 = execute_load()
        var2 = execute_load('var2')
        set_accumulator(var1 + var2)
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE:
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_accumulator(var1 + var2)

    else:
        initial_accumulator_value = accumulator
        var1 = execute_load()
        set_accumulator(initial_accumulator_value + var1)


"""
SUBTRACTION - There are three ways: SUB D1 NULL NULL, SUB D1 D2 NULL and SUB D3 D2 D1 similar to ADD but perform subtraction.
"""
def execute_sub():

    if icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:

        var1 = execute_load()
        var2 = execute_load('var2')
        set_accumulator(var1 - var2)
        execute_store('var3')

    elif icr['var2'] != NULL_VALUE:
    
        var1 = execute_load()
        var2 = execute_load('var2')
        set_accumulator(var1 - var2)

    else:
        initial_accumulator_value = accumulator
        var1 = execute_load()
        set_accumulator(initial_accumulator_value - var1)


"""
MULTIPLICATION - Using ADD perform multiplication operation. There are three ways: MUL D1 NULL NULL, MUL D1 D2 NULL, 
MUL D1 D2 D3 similar to ADD and SUB. Multiplication cannot be used with an immediate/direct/constant value.
"""
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
    
        initial_accumulator_value = accumulator
        for i in range(initial_accumulator_value-1):
            if i == 0:
                execute_load(var)
            execute_add()


"""
INTEGER DIVISION - Using SUB perform division operation.
"""
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
        initial_accumulator_value = accumulator
        for i in range(initial_accumulator_value-1):
            if accumulator > 0:
                execute_sub()
            else:
                set_accumulator(i)
                break


"""
NCREMENT - INC D3 NULL NULL Load the value in D3 memory address adds 1 and store in same address
"""
def execute_inc():
    execute_load('var1')
    set_accumulator(accumulator + 1)
    execute_store('var1')


"""
DECREMENT - DEC D3 NULL NULL Load the value in D3 memory address dec 1 and store in same address
"""
def execute_dec():
    execute_load('var1')
    set_accumulator(accumulator - 1)
    execute_store('var1')


"""
MOVE - MOV D2 D10 NULL Load the value in D2 memory address to D10 memory address and clear D2 address
"""
def execute_mov():
    execute_load('var1')
    execute_store('var2')
    execute_set(0, 'var1')


"""
BEQ D10 NULL NULL Load the value in D10 memory address if subtraction with accumulator register 
values is zero puts in D10 memory address. There are three ways: BEQ D10 NULL NULL, BEQ D1 D10 NULL, BEQ D1 D2 D3
"""
def execute_beq():
    initial_value_acumulator = accumulator
    variables = ['var1', 'var2', 'var3']
    for variable in variables:
        if icr[variable] != NULL_VALUE:
            value = execute_load(variable)
            difference = initial_value_acumulator - value
            if difference == 0:
                execute_set(0, variable)
    set_accumulator(initial_value_acumulator)


""" 
AND D2 D5 D6 - Carga los valores en las direcciones de memoria (los 3 obligatorios), si cada uno es mayor
al valor del accumulator, se actualiza el valor del accumulator con el mayor valor
"""
def execute_and():
    if icr['var1'] != NULL_VALUE and icr['var2'] != NULL_VALUE and icr['var3'] != NULL_VALUE:
        variables = ['var1', 'var2', 'var3']
        initial_value_acumulator = accumulator
        bigger_num = accumulator
        validated = True

        for variable in variables:
            value = execute_load(variable)
            """ Verificar que todos los valores sean mayor al del accumulator """
            if initial_value_acumulator >= value:
                validated = False
                break
            """ Registrar el numero mayor """
            if value > bigger_num:
                bigger_num = value

        if validated is False:
            set_accumulator(initial_value_acumulator)
        else:
            set_accumulator(bigger_num)


""" 
AND D2 D5 D6 - Carga los valores en las direcciones de memoria, el valor del accumulator 
es actualizado con el primer valor que se encuentre que sea mayor a él
"""
def execute_or():
    variables = ['var1', 'var2', 'var3']
    initial_value_acumulator = accumulator
    bigger_num = accumulator
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
        set_accumulator(initial_value_acumulator)
    else:
        set_accumulator(bigger_num)


"""
SHOW - SHW D2 NULL NULL show the value in D2 memory address, SHW ACC show the value in accumulator register, 
SHW ICR show the value in ICR register, SHW MAR show the value in MAR register, SHW MDR show the value in 
MDR register, SHW UC show the value in Control Unit.
"""
def execute_print():
    dict_show = {
        'ACC': accumulator,
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


""" Ejecutar unidad de control """
def execute_control_unit():
    if icr['word'] in words_instructions:
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

    """ Constantes """
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

    INICIO_INSTRUCCIONES = 1000  # De esta posición en adelante de registran las instrucciones

    """ Instrucciones habilitadas para ser leidas """
    words_instructions = [
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

    """ Cargar instrucciones en memoria """
    if len(sys.argv) > 1:  # Leer instruciones desde archivo de texto
        data = read_file(INICIO_INSTRUCCIONES)
    else:
        data = read_input(INICIO_INSTRUCCIONES)  # Leer instrucciones por linea de comandos
    
    """ Variables globales """
    pc = INICIO_INSTRUCCIONES
    icr = None
    mdr = None
    cu = None
    mar = pc
    accumulator = 0
    alu = []

    """ Ejecutar instrucciones en memoria """
    for i in range(len(get_memory_instructions())):
        execute_mdr()
        execute_control_unit()
        mar = pc
