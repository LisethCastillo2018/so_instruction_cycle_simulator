"""
UNIVERSIDAD DEL VALLE
SISTEMAS OPERATIVOS
ESTUDIANTE:
LISETH DAYANA CASTILLO QUIÑONES, CÓD. 1843187
"""
import sys


def read_file(inicio_instrucciones):
    ruta_archivo = sys.argv[1]
    f = open(ruta_archivo,'r')
    datos = procesar_lineas(f.readlines(), inicio_instrucciones)
    f.close()
    return datos


def read_input(inicio_instrucciones):
    instruccion = ""
    lineas = []
    while instruccion != "END":
        entrada = input("Ingrese instruccion: ")
        instruccion = str(entrada.split()[0]).upper()
        lineas.append(entrada)
    datos = procesar_lineas(lineas, inicio_instrucciones)
    return datos


def procesar_lineas(lineas, inicio_instrucciones):
    datos = [0 for x in range(inicio_instrucciones)]
    for i in range(0, len(lineas)):
        linea = lineas[i].replace('\n','').split(sep=' ')
        var4 = 'NULL'
        if len(linea) >= 5:
            var4 = linea[4]
        datos.append({
            'word': linea[0],
            'var1': linea[1],
            'var2': linea[2],
            'var3': linea[3],
            'var4': var4,
        })
    return datos
