import matplotlib.pylab as plt
from psutil import virtual_memory
#Creando listas para usar más adelante
datos_N, datos_dt, datos_memoria, datos_capacidadRAM = [], [], [], []
tamano_matriz, lista_dt, lista_memoria = [], [], []
rango_N = [1,10,20,50,100,200,500,1000,2000,5000,10000,20000]
capacidadRAM = virtual_memory().available
#Variables para después buscar el valor min para establecer los límites del gráfico
dt_min = 10
mem_min = 100
#Añadiendo la capacidadRAM a su lista, para luego graficar el límite de memoria del código
for i in range(len(rango_N)):
    datos_capacidadRAM.append(capacidadRAM)
#Se lee el archivo txt y se añaden los datos a listas para luego graficar correctamente
with open('rendimiento.txt', 'r') as f:
    for line in f:
        if line == "\n":
            datos_N.append(tamano_matriz)
            datos_dt.append(lista_dt)
            datos_memoria.append(lista_memoria)
            tamano_matriz, lista_dt, lista_memoria = [], [], []
            continue
        sl = line.split()
        N = int(sl[0])
        dt = float(sl[1])
        mem = int(sl[2])
        if dt < dt_min:
            dt_min = dt
        if mem < mem_min:
            mem_min = mem
        tamano_matriz.append(N)
        lista_dt.append(dt)
        lista_memoria.append(mem)
f.close()
#Se generan los 2 gráficos solicitados:
plt.figure(1)
plt.subplot(2,1,1)
#Se grafican todas las curvas de Tiempo Transcurrido (ya que varían con cada corrida)
for i in range(len(datos_N)):
    plt.loglog(datos_N[i], datos_dt[i], '-o')
#Se establece el eje Y
plt.ylim(dt_min/2, 60*10)
plt.yticks([0.1/1000,1/1000,10/1000,1/10,1,10,60,60*10],["0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"])
#Se establece el eje X
plt.xlim(1,20000)
plt.xticks(rango_N,[""])
#Se agrega un fondo cuadriculado y se nombra el grafico
plt.grid()
plt.title('Rendimiento A@B')
plt.ylabel('Tiempo transcurrido')
#Segundo grafico
plt.subplot(2,1,2)
#Se grafica la curva de Uso de Memoria (siempre es la misma curva para cada corrida del código, por lo que no es necesario un for)
plt.loglog(datos_N[0], datos_memoria[0], '-bo')
#Se grafica una linea punteada paralela al eje X para mostrar la capacidad RAM de mi laptop
plt.loglog(rango_N, datos_capacidadRAM, '--k')
#Se establece el eje Y
plt.ylim(mem_min/2, 10**11)
plt.yticks([10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10], ["1 KB", "10 KB", "100 KB", "1 MB", "10 MB", "100 MB", "1 GB", "10 GB"])
#Se establece el eje X
plt.xlim(1,20000)
plt.xticks(rango_N,["","10", "20", "50", "100", "200", "500", "1000", "2000", "5000", "10000", "20000"],rotation=45)
#Se agrega un fondo cuadriculado y se nombra el grafico
plt.grid()
plt.ylabel('Uso memoria')
plt.xlabel('Tamaño matriz N')
plt.savefig('graficos.png',bbox_inches='tight')
plt.show()