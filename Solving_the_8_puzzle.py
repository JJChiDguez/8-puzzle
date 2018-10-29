###########################################################################
#                       Jesus Javier Chi Dominguez.                       #
#                          Cinvestav- Zacatenco.                          # 
#                       Inteligencia Computacional.                       #
#                                Tarea 0                                  #
###########################################################################

###########################################################################
######### inversions calcula el nu'mero de inversiones de un estado #######
###########################################################################
def inversions(estado):
    inv = []
    for i in range(9):
        if estado[i] != " ":
            inv.append(int(estado[i]))
    counting = 0
    for i in range(7):
        for j in range(i+1,8):
            # contamos el numero de inversiones #
            if inv[i] > inv[j]:
                counting += 1
    return counting

###########################################################################
###### manhattan(s) calcula la distancia manhattan de s a '12345678 '######
########### Esta distancia ser'a nuestra heuri'stica requerida ############
###########################################################################
def manhattan(s,goal):
    suma = 0
    #goal = '12345678 '
    for i in goal:
        suma += abs ( (s.index(i)/3) - (goal.index(i)/3) ) + abs( (s.index(i) % 3) - (goal.index(i) % 3) )
    return suma

###########################################################################
### Adju(u) determina el conjunto de los nodos que esta'n conectado a u ###
####################### (El conjunto Adjacente de u) ######################
###########################################################################
def Adju(u):
    for i in range(9):
        if u[i] == " ":
            j = i
    # Determinamos las posiciones donde se puede mover el elemento espacio #
    options = { 0 : [1,3],
                1 : [0,2,4],
                2 : [1,5],
                3 : [0,4,6],
                4 : [1,5,3,7],
                5 : [2,4,8],
                6 : [3,7],
                7 : [4,6,8],
                8 : [5,7],
               }
    ad = options[j]
    adju = []
# Comenzamos con crear los estados adyacentes como una cadena de caracteres #
    for i in ad:
        z = list(u)
        z[j] = z[i]
        z[i] = ' '
        adju.append("".join(z))

    return adju

###########################################################################
############# show(A,k) imprime el estado A con sangri'a k ################
###########################################################################
def show(A,k):
    slash = k*" "
    print slash, "*", "-" ,"*", "-", "*", "-", "*"
    for i in range(3):
        print slash, "|", A[3*i], "|", A[3*i+1], "|", A[3*i+2], "|"
        print slash, "*", "-", "*", "-", "*", "-", "*"

###########################################################################
######################## Algoritmo de A* (star) ###########################
###########################################################################
def A_Star(V, s, t):
    from copy import copy

    esperando =["\(n_n)/","(/n_n)/","(-n_n)-","-(n_n-)","\(n_n\)"]
    ##################  Verificamos los nodos entradas ####################
    if s == t:
        return "El nodo inicial y final son el mismo. Por lo que la distancia mi'nima es 0."
    if s in V == False:
        return "El nodo inicial " + str(s) + " no pertenece al grafo."
    if t in V == False:
        return "El nodo final " + str(t) + " no pertenece al grafo."

    #  #
    grafo = {}
    # Creamos un diccionario d, para las distancias "mi'nimas" 
    d = {}
    # Creamos un diccionario pi
    pi = {}
    count = 0
    # Inicializamos las distancias
    for i in V:
        k = i
        if i == s:
            d[i] = 0 # la distancia ma's corta de s a s es 0
        else:
            d[i] = float('inf') # las dema's distancias son infinitas
    
    #Q = copy(d) # 
    grafo[s] = {u:1 for u in Adju(s)}
    Q = []
    h = {}
    #Q[s] = d[s]
    h[s] = manhattan(s,t)
    Q.append((d[s]+h[s],s))
    #######################################################################
    #################### Comenzamos con el algoritmo ######################
    #######################################################################
    from heapq import heappop,heapify, heappush
    # Hacemos Q como una cola de priodidad #
    heapify(Q)
    auxiliar = 0
    w = []
    print ""
    while len(Q) > 0:
        # Hallamos la llave con la mi'nima d
        # dq es el con la mi'nima d
        dq = heappop(Q)[1]
        w.append(dq)
        # Actualizamos segu'n los nodos que se encuentran conectado con dq
        for i in grafo[dq]:
            if d[i] > (d[dq] + grafo[dq][i]):
                d[i] = d[dq] + grafo[dq][i]
                pi[i] = dq
                h[i] = manhattan(i,t)
                heappush(Q,(d[i]+h[i],i))
                grafo[i] = {u:1 for u in Adju(i)}
            if i == t:
                auxiliar = 1
                break
        if auxiliar == 1:
            break
        #del Q[dq] # Una vez que un nodo es visitado, lo debemos excluir de Q
        count += 1
        if (count % 3000) == 0:
            print " recorriendo estados..... ", esperando[ (count/3000 - 1) % 5]
    print ""
    ########################################################################
    ######################## Termina el algoritmo ##########################
    ########################################################################

    ###### Ahora se procede a imprimir el caminos ma's corto de s a t ######

    temp = copy(t)
    rpath = []
    path = []

    while 1:
        rpath.append(temp)
        # Preguntamos si existe un camino entre s y t #
        # si t no esta' en los indices de pi, entonces no existe ningu'n camino #
        if pi.has_key(temp):
            temp = pi[temp]
        else:
            print " Nu'mero de estados recorridos: " + str(len(w)) + "."
            return " No existe camino de " + str(s) + " a " + str(t) + "."
        if temp == s:
            rpath.append(temp)
            break
    # Ordenamos los estados ya que en lo anterior obtenemos los estados #
    # (movimientos) desde t hasta s #
    for j in range(len(rpath)-1,-1,-1):
        path.append(rpath[j])

    print " El camino ma's corto entre estos dos estados es: "
    for i in range(len(path)):
        show(path[i],30)
        print " "

    print " Nu'mero mi'nimo de movimientos: " + str(d[t]) + "."
    return " Nu'mero de estados recorridos: " + str(len(w)) + "."

###########################################################################
############## Comenzamos con la resoluci'on del 8-puzzle #################
###########################################################################

from itertools import permutations
import random
import time

# La siguiente secuencia de prints explican como ejecutar el archivo #
print ""
print "*************************************************************************"
print " Primeramente, a la siguiente pregunta se debe de responder: si o no, si "
print " no se teclea  exactamente igual,  el programa seguira'preguntando hasta "
print " que se teclee  correctamente.  Si selecciona no,  se debera' teclear el "
print " tado como una cadena, por ejemplo supongamos que deseamos teclear el si-"
print " guiente estado: "
print "                * - * - * - *"
print "                | 8 | 6 | 7 |"
print "                * - * - * - *"
print "                | 2 | 5 | 4 |"
print "                * - * - * - *"
print "                | 3 |   | 1 |"
print "                * - * - * - *"
print " Entonces seri'a : 8672543 1"                
print "**********************************************************************"

print ""

# Un posible estado objetivo usual#
u = '12345678 ' 
# Generamos el conjunto de todas las permutaciones #
auxV = list(permutations(u))
#  En esta parte transformamos cada entrada de nuestra lista a una cadena  #
V = []
for i in range(len(auxV)):
    V.append(''.join(auxV[i]))
# Selecionamos un nu'mero aleatorio entre 0 y 9!, esto nos servira' para #
# obtener un estado aleatorio #
x = random.randint(0,len(V))

goal = u

print " El estado objetivo es: "
show(goal,10)

# Ahora preguntamos si se quiere seleccionar aleatoriamente el estado inicial #
decision = str( raw_input(' Seleccionar aleatoriamente un estado inicial?: (si/no) '))
# Se realiza un while hasta que seleccione Si o' No #
while (decision != 'si' and decision != 'no'):
    print " Respuesta inva'lida, asegu'rese de teclear si o' no"
    decision = str( raw_input(' Seleccionar aleatoriamente un estado inicial?: (si/no) '))

if decision == 'si':
    print " Se selecionara' aleatoriamente el estado inicial"
    print " El estado incial seleccionado aleatoriamente es: "
    show(V[x],10)
    # Verificamos si se satisface la condicio'n de paridad #
    # Si no, entonces no se puede resolver el 8-puzzle#
    if (inversions(V[x]) % 2) == 1:
        print " Error de Paridad, nu'mero de inversiones impar."
        print " No existe camino entre el estado inicial y el objetivo."
    else:
        start_time = time.time()
        print A_Star(V, V[x], goal)
        print " Tiempo de ejecuci'on: ", time.time() - start_time, "segundos."

else:
    initial = str( raw_input('Teclea el estado inicial: '))
    print " El estado incial tecleado es: "
    show(initial,10)
    # Nuevamente checamos la condicio'n de paridad #
    if (inversions(initial) % 2) == 1:
        print " Error de Paridad, nu'mero de inversiones impar."
        print " No existe camino entre el estado inicial y el objetivo."
    else:
        start_time = time.time()
        print A_Star(V, initial, goal)
        print " Tiempo de ejecucio'n: ", time.time() - start_time, "segundos."
