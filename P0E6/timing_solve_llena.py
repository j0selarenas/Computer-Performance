from numpy import eye, ones
from scipy.linalg import solve
import numpy as np
from time import perf_counter
import scipy.sparse as sparse
import scipy.sparse.linalg as lin

def laplacianaLlena(N, t):
    e = eye(N) - eye(N,N,1)
    return(t(e+e.T))

def laplacianaDispersa(N, t):
    e = sparse.eye(N, dtype = t) - sparse.eye(N, N, 1, dtype = t)
    return(e+e.T)

def solveSciPy(matrizNxN, b, caso):
    t1 = perf_counter()
    if caso == 'llena':
        x = solve(matrizNxN, b, assume_a = 'pos')
    elif caso == 'dispersa':
        x = lin.spsolve(matrizNxN, b)
    t2 = perf_counter()
    dt = t2 - t1
    return(dt)

def exportar(datos_N, dt_ensamblaje, dt_solucion, caso):
    with open("rendimiento_solve_"+caso+".txt", 'w') as f:
        for i in range(len(dt_ensamblaje)):
            for j in range(len(dt_ensamblaje[i])):
                f.write(f"{datos_N[i][j]} {dt_ensamblaje[i][j]} {dt_solucion[i][j]}\n")
            f.write("\n")
    f.close()
        
def repeticionN(valores_N, dtype, caso):
    lista_dt_ensamblaje, lista_dt_solucion = [], []
    temporizador1 = perf_counter()
    for i in range(len(valores_N)):
        t1 = perf_counter()
        if caso == 'llena':
            matrizNxN = laplacianaLlena(valores_N[i], dtype)
        elif caso == 'dispersa':
            matriz = laplacianaDispersa(valores_N[i], dtype)
            matrizNxN = sparse.csr_matrix(matriz)
        b = ones(valores_N[i])
        t2 = perf_counter()
        matrizSolve = solveSciPy(matrizNxN, b, caso)
        t3 = perf_counter()
        dt_ensamblaje = t2 - t1
        dt_solucion = t3 - t2
        lista_dt_ensamblaje.append(dt_ensamblaje)
        lista_dt_solucion.append(dt_solucion)
        temporizador2 = perf_counter()
        if temporizador2-temporizador1 >= 120:
            break
    resultados = [lista_dt_ensamblaje, lista_dt_solucion]
    return(resultados)
    
def corridas(valores_N, dtype, caso):
    datos_N, datos_dt_ensamblaje, datos_dt_solucion= [], [], []
    for _ in range(10):
        datos_N.append(valores_N)
        RESULTADO = repeticionN(valores_N, dtype, caso)
        dt_ensamblaje, dt_solucion = RESULTADO[0], RESULTADO[1]
        datos_dt_ensamblaje.append(dt_ensamblaje)
        datos_dt_solucion.append(dt_solucion)
    resultados = [datos_N, datos_dt_ensamblaje, datos_dt_solucion]
    return(resultados)

def main():
    valores_N = [2,5,10,12,16,20,30,40,45,50,55,60,80,100,130,160,200,250,350,500,600,800,1000,2000,5000,10000,15000]
    dtype = np.double
    casos = ['llena', 'dispersa']
    caso = casos[0]
    RESULTADOS = corridas(valores_N, dtype, caso)
    datos_N = RESULTADOS[0]
    dt_ensamblaje = RESULTADOS[1]
    dt_solucion = RESULTADOS[2]
    exportar(datos_N, dt_ensamblaje, dt_solucion, caso)

if __name__ == '__main__':
    main()