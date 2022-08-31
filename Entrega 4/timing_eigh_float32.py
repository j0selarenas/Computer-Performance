from scipy.linalg import solve, eigh
from numpy import eye, float32, ones
import numpy as np
import scipy as sp
from time import perf_counter

def laplaciana(N, dtype):
    e = eye(N) - eye(N,N,1)
    return dtype(e+e.T)

def solveSciPy(caso, N, matrizNxN):
    b = ones(N)
    t1 = perf_counter()
    if caso == 1:
        x = np.linalg.inv(matrizNxN)*b
    elif caso == 2:
        x = solve(matrizNxN, b)
    elif caso == 3:
        x = solve(matrizNxN, b, assume_a = 'pos')
    elif caso == 4:
        x = solve(matrizNxN, b, assume_a = 'sym')
    elif caso == 5:
        x = solve(matrizNxN, b, overwrite_a = True)
    elif caso == 6:
        x = solve(matrizNxN, b, overwrite_b = True)
    else:
        x = solve(matrizNxN, b, overwrite_a = True, overwrite_b = True)
    t2 = perf_counter()
    dt = t2 - t1
    return(dt)

def eigenValues(caso, matrizNxN):
    t1 = perf_counter()
    if caso == 1:
        w, h = sp.linalg.eigh(matrizNxN)
    elif caso == 2:
        w, h = sp.linalg.eigh(matrizNxN, overwrite_a = False, turbo = "ev")
    elif caso == 3:
        w, h = sp.linalg.eigh(matrizNxN, overwrite_a = False, turbo = 'evd')
    elif caso == 4:
        w, h = sp.linalg.eigh(matrizNxN, overwrite_a = False, turbo = 'evr')
    else:
        w, h = sp.linalg.eigh(matrizNxN, overwrite_a = False, turbo = 'evx')
    t2 = perf_counter()
    dt = t2 - t1
    return(dt)

def promedio(lista_datos):
    lista_datos = np.array(lista_datos)
    lista_promedio = []
    for i in range(len(lista_datos[0])):
        lista_promedio.append(np.average(lista_datos[:,i]))
    return(lista_promedio)

def exportar(caso, datos_N, datos_dt, dtype):
    nombre_archivo = "rendimiento_eigh_caso_" + str(caso) + "_False_float32.txt"
    if dtype == np.double:
        with open(nombre_archivo, 'w') as f:
            for i in range(len(datos_dt)):
                f.write(f"{datos_N[i]} {datos_dt[i]}\n")
            f.write("\n")
        f.close()
    else:
        with open(nombre_archivo, 'w') as f:
            for i in range(len(datos_dt)):
                f.write(f"{datos_N[i]} {datos_dt[i]}\n")
            f.write("\n")
        f.close()
    
def repeticionN(caso, valores_N, dtype):
    lista_dt = []
    temporizador1 = perf_counter()
    for i in range(len(valores_N)):
        matrizNxN = laplaciana(int(valores_N[i]),dtype)
        lista_dt.append(eigenValues(caso, matrizNxN))
        temporizador2 = perf_counter()
        if temporizador2-temporizador1 >= 120:
            break
    return(lista_dt)
    
def corridas(caso, valores_N, dtype):
    corrida = 1
    datos_corrida = []
    while corrida <= 10:
        datos_corrida.append(repeticionN(caso, valores_N, dtype))
        corrida += 1
    return(datos_corrida)
    
def main():
    valores_N = [2,5,10,12,16,20,30,40,45,50,55,60,80,100,130,160,200,250,350,500,600,800,1000,2000,5000,7500]
    dtype = float32
    casos = [1,2,3,4,5]    
    
    caso_1 = promedio(corridas(casos[0], valores_N, dtype))
    exportar(casos[0], valores_N, caso_1, dtype)
    
    caso_2 = promedio(corridas(casos[1], valores_N, dtype))
    exportar(casos[1], valores_N, caso_2, dtype)
    
    caso_3 = promedio(corridas(casos[2], valores_N, dtype))
    exportar(casos[2], valores_N, caso_3, dtype)
    
    caso_4 = promedio(corridas(casos[3], valores_N, dtype))
    exportar(casos[3], valores_N, caso_4, dtype)
    
    caso_5 = promedio(corridas(casos[4], valores_N, dtype))
    exportar(casos[4], valores_N, caso_5, dtype)

if __name__ == '__main__':
    main()