from numpy import zeros, float32
from time import perf_counter
import numpy as np
from psutil import virtual_memory
#Creando listas para usar más adelante
datos_N, datos_dt, datos_memoria, datos_capacidadRAM = [], [], [], []
#Valores eje X para el gráfico
rango_N = [1,10,20,50,100,200,500,1000,2000,5000,10000,20000]
#Lista con los tamaños de matrices utilizados
valores_N = [2,5,10,12,16,20,30,40,45,50,55,60,80,100,130,160,200,250,350,500,600,800,1000,2000,5000,10000]
#Capacidad disponible RAM de mi laptop
capacidadRAM = virtual_memory().available
#Variable para hacer las 10 repeticiones
repeticiones = 1
#while para hacer las 10 corridas del código
while repeticiones <= 10:
    #Listas para acumular datos de cada corrida, más adelante se almacenarán estos datos en otras listas
    lista_dt = []
    lista_memoria = []
    #Tiempo inicial de cada corrida, para ver que no se demore más de 2 min cada corrida
    temporizador1 = perf_counter()
    #for para hacer las operaciones solicitadas
    for i in range(len(valores_N)):
        #Tamaño de las matrices
        N = valores_N[i]
        #Matrices A y B
        A = zeros((N,N), dtype=float32) + 1
        B = zeros((N,N), dtype=float32) + 2
        #t1 y t2 para ver cuanto se demora en hacer el matmul
        t1 = perf_counter() 
        C = A@B
        t2 = perf_counter()
        dt = t2 - t1
        #Calculo de la memoria utilizada para determinar matmul
        uso_memoria = A.nbytes + B.nbytes + C.nbytes
        #Tiempo que va cambiando dentro de la corrida para ver si luego se pasan los 2 min
        temporizador2 = perf_counter()
        #if que para la corrida si se pasan los 2 min
        if temporizador2-temporizador1 >= 120:
            break
        #if que para la corrida si se sobrepasa la capacidadRAM del laptop
        if uso_memoria >= capacidadRAM:
            break
        #Se agregan los datos solicitados a listas
        lista_dt.append(dt)
        lista_memoria.append(uso_memoria)
        #print(f"N = {N} dt = {dt} s  mem = {uso_memoria} bytes  flops = {N**3/dt} flops/s")
    #Se guardan las listas de datos en otras listas para almacenar información de todas las corridas
    datos_N.append(valores_N)
    datos_dt.append(lista_dt)
    datos_memoria.append(lista_memoria)
    #Se suma 1 a la variable para que el while termine después de 10 corridas        
    repeticiones += 1
#Se crea un archivo txt para almacenar todos los datos obtenidos
with open('rendimiento.txt', 'w') as f:
    for i in range(len(datos_N)):
        for j in range(len(datos_N[i])):
            f.write(f"{datos_N[i][j]} {datos_dt[i][j]} {datos_memoria[i][j]}\n")
        f.write("\n")
f.close()