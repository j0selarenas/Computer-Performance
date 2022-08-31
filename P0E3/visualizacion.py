import matplotlib.pylab as plt
from psutil import virtual_memory

datos_N, datos_dt, datos_memoria, datos_capacidadRAM = [], [], [], []
tamano_matriz, lista_dt, lista_memoria = [], [], []
rango_N = [1,10,20,50,100,200,500,1000,2000,5000,10000,20000]
capacidadRAM = virtual_memory().available
dt_min = 10
mem_min = 100

#El archivo .txt puede incluir el ".txt" o no, el código se ajusta a cualquier caso.
input_usuario = str(input("Ingresar el nombre del archivo .txt \n(Ej: rendimiento_caso_2_double) = "))

if input_usuario.endswith(".txt") == True:
    usuario = ""
    for i in input_usuario:
        if i == ".":
            break
        else:
            usuario += i
else:
    usuario = input_usuario

archivo_txt = usuario + ".txt"
name = ""

a = usuario.find("caso_") + 5

while a < len(usuario):
    name += usuario[a]
    a += 1

graph_name = "graficos_caso_" + name + ".png"

b = usuario.replace("_", " ")

rend_name = ""

for i in range(len(b)):
    if b[i-1] == " " or i == 0:
        rend_name += b[i].upper()
    else:
        rend_name += b[i]

for i in range(len(rango_N)):
    datos_capacidadRAM.append(capacidadRAM)
    
with open(archivo_txt, 'r') as f:
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

plt.figure(1)
plt.subplot(2,1,1)

for i in range(len(datos_N)):
    plt.loglog(datos_N[i], datos_dt[i], '-o')
    
plt.ylim(dt_min/2, 60*10)
plt.yticks([0.1/1000,1/1000,10/1000,1/10,1,10,60,60*10],["0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"])

plt.xlim(1,20000)
plt.xticks(rango_N,[""])

plt.grid()
plt.title(rend_name)
plt.ylabel('Tiempo transcurrido')

plt.subplot(2,1,2)
plt.loglog(datos_N[0], datos_memoria[0], '-bo')
plt.loglog(rango_N, datos_capacidadRAM, '--k')

plt.ylim(mem_min/2, 10**11)
plt.yticks([10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10], ["1 KB", "10 KB", "100 KB", "1 MB", "10 MB", "100 MB", "1 GB", "10 GB"])
plt.xlim(1,20000)
plt.xticks(rango_N,["","10", "20", "50", "100", "200", "500", "1000", "2000", "5000", "10000", "20000"],rotation=45)

plt.grid()
plt.ylabel('Uso memoria')
plt.xlabel('Tamaño matriz N')
plt.savefig(graph_name,bbox_inches='tight')
plt.show()