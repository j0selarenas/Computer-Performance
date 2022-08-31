import matplotlib.pylab as plt
from psutil import virtual_memory

rango_N = [1,10,20,50,100,200,500,1000,2000,5000,10000,20000]

#El archivo .txt puede incluir el ".txt" o no, el código se ajusta a cualquier caso.
input_usuario1 = str(input("Ingresar el nombre del archivo .txt \n(Ej: rendimiento_solve_caso_1_double.txt) = "))
input_usuario2 = str(input("Ingresar el nombre del archivo .txt \n(Ej: rendimiento_solve_caso_2_double.txt) = "))

def arreglarArchivo(input_usuario):
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
    a = usuario.find("rendimiento_") + 12
    
    while a < len(usuario):
        name += usuario[a]
        a += 1
    return(archivo_txt, name)

def openArchivo(archivo):
    lista_N, lista_dt, dt_min = [], [], 10
    with open(archivo, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            sl = line.split()
            N = int(sl[0])
            dt = float(sl[1])
            if dt < dt_min:
                dt_min = dt
            lista_N.append(N)
            lista_dt.append(dt)
    f.close()
    return(lista_N, lista_dt, dt_min)

datos_N1 = openArchivo(arreglarArchivo(input_usuario1)[0])[0]
datos_dt1 = openArchivo(arreglarArchivo(input_usuario1)[0])[1]
dt_min1 = openArchivo(arreglarArchivo(input_usuario1)[0])[2]

datos_N2 = openArchivo(arreglarArchivo(input_usuario2)[0])[0]
datos_dt2 = openArchivo(arreglarArchivo(input_usuario2)[0])[1]
dt_min2 = openArchivo(arreglarArchivo(input_usuario2)[0])[2]

dt_min = min(dt_min1, dt_min2)

names = [arreglarArchivo(input_usuario1)[1], arreglarArchivo(input_usuario2)[1]]

graph_name = names[0] + "_vs_" + names[1] + ".png"

plt.figure(1)
plt.subplot(2,1,1)

plt.loglog(datos_N1, datos_dt1, '-o', label=names[0])
plt.loglog(datos_N2, datos_dt2, '-o', label=names[1])
plt.legend()

plt.ylim(dt_min/2, 60*10)
plt.yticks([0.1/1000,1/1000,10/1000,1/10,1,10,60,60*10],["0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"])

plt.xlim(1,20000)
plt.xticks(rango_N,[""])

plt.grid()
plt.ylabel('Tiempo transcurrido')

plt.xlabel('Tamaño matriz N')
plt.savefig(graph_name,bbox_inches='tight')
plt.show()