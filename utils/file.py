"""
UNIVERSIDAD DEL VALLE
SISTEMAS OPERATIVOS
ESTUDIANTE:
LISETH DAYANA CASTILLO QUIÑONES, CÓD. 1843187
"""
import sys


def read_file():
    ruta_archivo = sys.argv[1]
    f = open (ruta_archivo,'r')
    lineas = f.readlines()
    datos = [0 for x in range(int(sys.argv[2]))]
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
    f.close()
    # print(f'Se lee archivo')
    return datos

