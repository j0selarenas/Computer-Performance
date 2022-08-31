from numpy import eye
import numpy as np
from time import perf_counter
import scipy.sparse as sparse

def laplacianaLlena(N, t):
    e = eye(N) - eye(N,N,1)
    return(t(e+e.T))

def laplacianaDispersa(N, t):
    e = sparse.eye(N, dtype = t) - sparse.eye(N, N, 1, dtype = t)
    return(e+e.T)

def matmul(A, B, caso):
    matMul = 0
    if caso == 'llena':
        matMul = A@B
    elif caso == 'dispersa':
        Acsr = sparse.csr_matrix(A)
        Bcsr = sparse.csr_matrix(B)
        matMul = Acsr@Bcsr
    return(matMul)

def exportar(datos_N, dt_ensamblaje, dt_matmul):
    with open("rendimiento_matmul_dispersa.txt", 'w') as f:
        for i in range(len(dt_ensamblaje)):
            for j in range(len(dt_ensamblaje[i])):
                f.write(f"{datos_N[i][j]} {dt_ensamblaje[i][j]} {dt_matmul[i][j]}\n")
            f.write("\n")
    f.close()
    
def repeticionN(valores_N, dtype):
    lista_dt_ensamblaje, lista_dt_matmul = [], []
    temporizador1 = perf_counter()
    for i in range(len(valores_N)):
        t1 = perf_counter()
        matrizDispersaA = laplacianaDispersa(valores_N[i], dtype)
        matrizDispersaB = laplacianaDispersa(valores_N[i], dtype)
        t2 = perf_counter()
        matrizDispersaC = matmul(matrizDispersaA, matrizDispersaB, 'dispersa')
        t3 = perf_counter()
        dt_ensamblaje = t2 - t1
        dt_matmul = t3 - t2
        lista_dt_ensamblaje.append(dt_ensamblaje)
        lista_dt_matmul.append(dt_matmul)
        
        temporizador2 = perf_counter()
        if temporizador2-temporizador1 >= 120:
            break
    return(lista_dt_ensamblaje, lista_dt_matmul)
    
def corridas(valores_N, dtype):
    datos_N, datos_dt_ensamblaje, datos_dt_matmul= [], [], []
    for _ in range(10):
        datos_N.append(valores_N)
        dt_ensamblaje, dt_matmul = repeticionN(valores_N, dtype)[0], repeticionN(valores_N, dtype)[1]
        datos_dt_ensamblaje.append(dt_ensamblaje)
        datos_dt_matmul.append(dt_matmul)
    return(datos_N, datos_dt_ensamblaje, datos_dt_matmul)

def main():
    valores_N = [2,5,10,12,16,20,30,40,45,50,55,60,80,100,130,160,200,250,350,500,600,800,1000,2000,5000,10000,20000,30000,40000,50000,100000,250000,500000,1000000,2500000,5000000,10000000,25000000]
    dtype = np.double
    datos_N = corridas(valores_N, dtype)[0]
    dt_ensamblaje = corridas(valores_N, dtype)[1]
    dt_matmul = corridas(valores_N, dtype)[2]
    exportar(datos_N, dt_ensamblaje, dt_matmul)

if __name__ == '__main__':
    main()