import matplotlib.pylab as plt

rango_N = [1,10,20,50,100,200,500,1000,2000,5000,10000,20000]
rango_N_str = ["","10", "20", "50", "100", "200", "500", "1000", "2000", "5000", "10000", "20000"]
#El archivo .txt puede incluir el ".txt" o no, el código se ajusta a cualquier caso.
input_usuario = str(input("Ingresar el nombre del archivo .txt \n(Ej: rendimiento_solve_llena.txt) = "))

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
    a = usuario.find("rendimiento_") + 12
    name = ""  
    while a < len(usuario):
        name += usuario[a]
        a += 1
    nameArch = name.split('_')
    return(archivo_txt, nameArch)

def openArchivo(archivo):
    lista_N, lista_dt_ensamblaje, lista_dt_matmul, dt_min = [], [], [], 10
    datos_N, datos_dt_ensamblaje, datos_dt_matmul = [], [], []
    with open(archivo, 'r') as f:
        for line in f:
            if line == "\n":
                datos_N.append(lista_N)
                datos_dt_ensamblaje.append(lista_dt_ensamblaje)
                datos_dt_matmul.append(lista_dt_matmul)
                lista_N, lista_dt_ensamblaje, lista_dt_matmul= [], [], []
                continue
            sl = line.split()
            N = int(sl[0])
            dt_ensamblaje = float(sl[1])
            dt_matmul = float(sl[2])
            dt = min(dt_ensamblaje, dt_matmul)
            if dt < dt_min:
                dt_min = dt
            lista_N.append(N)
            lista_dt_ensamblaje.append(dt_ensamblaje)
            lista_dt_matmul.append(dt_matmul)
    f.close()
    return(datos_N, datos_dt_ensamblaje, datos_dt_matmul, dt_min)

nameArch = arreglarArchivo(input_usuario)[1]

xlim = 20_000

datos_N = openArchivo(arreglarArchivo(input_usuario)[0])[0]
dt_ensamblaje = openArchivo(arreglarArchivo(input_usuario)[0])[1]
dt_matmul = openArchivo(arreglarArchivo(input_usuario)[0])[2]
dt_min = openArchivo(arreglarArchivo(input_usuario)[0])[3]

Nmin, Nmax = min(datos_N[0]), max(datos_N[0])
dt_ens_max, dt_mat_max = 0, 0

for i in range(len(dt_ensamblaje)):
    for j in range(len(dt_ensamblaje[i])):
        if dt_ensamblaje[i][j] > dt_ens_max:
            dt_ens_max = dt_ensamblaje[i][j]
            
for i in range(len(dt_matmul)):
    for j in range(len(dt_matmul[i])):
        if dt_matmul[i][j] > dt_mat_max:
            dt_mat_max = dt_matmul[i][j]

plt.figure(1)
plt.subplot(2,1,1)

for i in range(len(datos_N)):
    plt.loglog(datos_N[i], dt_ensamblaje[i], '-o', color='black', alpha=0.2, markersize=2.5)

valN = [Nmin, Nmax]
plt.loglog(valN, [dt_ens_max, dt_ens_max] ,'--',color='blue')
valN = [Nmin, Nmax]
val_dt_ens = [0.01/10000, dt_ens_max]
plt.loglog(valN, val_dt_ens, '--', color='orange')
valN = [Nmin**2, Nmax]
val_dt_ens = [(0.01/10000)**2, dt_ens_max]
plt.loglog(valN, val_dt_ens, '--', color='green')
valN = [Nmin**3, Nmax]
val_dt_ens = [(0.01/10000)**3, dt_ens_max]
plt.loglog(valN, val_dt_ens, '--', color='red')
valN = [Nmin**4, Nmax]
val_dt_ens = [(0.01/10000)**4, dt_ens_max]
plt.loglog(valN, val_dt_ens, '--', color='purple')

plt.ylim(0.01/10000, 60*10)
plt.yticks([0.01/1000,0.1/1000,1/1000,10/1000,1/10,1,10,60,60*10],["0.01 ms", "0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"])

plt.xlim(1,xlim)
plt.xticks(rango_N,[""])

plt.title('Rendimiento Laplaciana '+nameArch[0].upper()+' '+nameArch[1])
plt.grid()
plt.ylabel('Tiempo de ensamblado')
plt.subplot(2,1,2)

for i in range(len(datos_N)):
    plt.loglog(datos_N[i], dt_matmul[i], '-o', color='black', alpha=0.2, markersize=3)
    
valN = [Nmin, Nmax]
plt.loglog(valN, [dt_mat_max, dt_mat_max] ,'--',color='blue', label='Constante')
valN = [Nmin, Nmax]
val_dt_mat = [0.01/10000, dt_mat_max]
plt.loglog(valN, val_dt_mat, '--', color='orange', label='O(N)')
valN = [Nmin**2, Nmax]
val_dt_mat = [(0.01/10000)**2, dt_mat_max]
plt.loglog(valN, val_dt_mat, '--', color='green', label='O(N²)')
valN = [Nmin**3, Nmax]
val_dt_mat = [(0.01/10000)**3, dt_mat_max]
plt.loglog(valN, val_dt_mat, '--', color='red', label='O(N³)')
valN = [Nmin**4, Nmax]
val_dt_mat = [(0.01/10000)**4, dt_mat_max]
plt.loglog(valN, val_dt_mat, '--', color='purple', label='O(N⁴)')    
plt.legend(loc=2)

plt.ylim(0.01/10000, 60*10)
plt.yticks([0.01/1000,0.1/1000,1/1000,10/1000,1/10,1,10,60,60*10],["0.01 ms", "0.1 ms", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "1 min", "10 min"])

plt.xlim(1,xlim)
plt.xticks(rango_N,rango_N_str,rotation=45)
plt.grid()
plt.ylabel('Tiempo de solucion')

graph_name = "grafico_" + nameArch[0] + "_" + nameArch[1] + ".png"

plt.xlabel('Tamaño matriz N')
plt.savefig(graph_name, bbox_inches='tight')
plt.show()