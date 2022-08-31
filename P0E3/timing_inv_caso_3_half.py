from scipy import linalg
from numpy import zeros
import numpy as np
import scipy as sp
from time import perf_counter
from psutil import virtual_memory

def laplaciana(N, dtype):
    matriz = zeros((N,N), dtype=dtype)
    for i in range(N):
        matriz[i,i] = 2
        for j in range(max(0, i-2), i):
            if abs(i - j) == 1:
                matriz[i, j] = -1
                matriz[j, i] = -1
    return matriz

def inverseSciPy(matriz):
    t1 = perf_counter()
    matrizINV = sp.linalg.inv(matriz, overwrite_a=True)
    t2 = perf_counter()
    dt_inversion = t2 - t1
    uso_memoria = matrizINV.nbytes
    datos_SciPy = [matrizINV, dt_inversion, uso_memoria]
    return(datos_SciPy)

def exportar(datos_N, datos_dt, datos_memoria):
    with open('rendimiento_caso_3_half.txt', 'w') as f:
        for i in range(len(datos_N)):
            for j in range(len(datos_N[i])):
                f.write(f"{datos_N[i][j]} {datos_dt[i][j]} {datos_memoria[i][j]}\n")
            f.write("\n")
    f.close()

def main():
    datos_N, datos_dt, datos_memoria = [], [], []
    valores_N = [3,5,10,12,16,20,30,40,45,50,55,60,80,100,130,160,200,250,350,500,600,800,1000,2000,5000,10000]
    capacidadRAM = virtual_memory().available
    repeticiones = 1
    while repeticiones <= 10:
        lista_dt = []
        lista_memoria = []
        temporizador1 = perf_counter()
        for i in range(len(valores_N)):
            dtype = np.half
            matrizNxN = laplaciana(int(valores_N[i]),dtype)
            memoria_inv = inverseSciPy(matrizNxN)[2]
            memoria_total = matrizNxN.nbytes + memoria_inv
            dt_inv = inverseSciPy(matrizNxN)[1]
            temporizador2 = perf_counter()
            if temporizador2-temporizador1 >= 120:
                break
            if memoria_total >= capacidadRAM:
                break
            lista_dt.append(dt_inv)
            lista_memoria.append(memoria_total)
        datos_N.append(valores_N)
        datos_dt.append(lista_dt)
        datos_memoria.append(lista_memoria)      
        repeticiones += 1
    exportar(datos_N, datos_dt, datos_memoria)

if __name__ == '__main__':
    main()