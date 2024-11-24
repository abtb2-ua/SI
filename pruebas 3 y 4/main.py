import sys, pygame, heapq
from casilla import *
from mapa import *
from estado import *
from pygame.locals import *


MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(250, 180, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(120, 60, 50) 

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una CASILLA del mapa se puede seleccionar como destino o como origen
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res
    
# Devuelve si una POSICIÓN de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapi, posicion):
    res=-1
    
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2

    
    return res
   
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

# Calcule el coste del movimiento
def calcularCoste(casO, casD):
    if (
            (abs(casD.getFila() - casO.getFila()) == 1 and abs(casD.getCol() - casO.getCol() == 0)) or
            (abs(casD.getCol() - casO.getCol()) == 1 and abs(casD.getFila() - casO.getFila() == 0))
    ):
        return 1
    else:
        return 1.5    

# Devuelve las casillas adyacentes accesibles
def obtenerAdyacentesAccesibles(mapi, estado):
    adyacentes = []
    movimientos = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    
    for movimiento in movimientos:
        casilla = estado.getCasilla()
        nuevaCol = casilla.getCol() + movimiento[0]
        nuevaFila = casilla.getFila() + movimiento[1]
        #nueva_pos = (nueva_col, nueva_fila)
        nuevaCasilla = Casilla(nuevaFila, nuevaCol)
        
        #if esMapa(mapi, nueva_pos):
        if bueno(mapi, nuevaCasilla):
            adyacentes.append(nuevaCasilla)
    
    return adyacentes

def dentro_mapa(mapi, casilla):
    return casilla.getFila() >= 0 and casilla.getCol() >= 0 and \
           casilla.getFila() < mapi.alto and casilla.getCol() < mapi.ancho

def heuristica(actual, destino):
    # Primera heurística: h = 0 (algoritmo Dijkstra)
    return 0

def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.casilla)
        nodo = nodo.antecesor
    camino.reverse()
    return camino

def eliminar_estado(listaFrontera, estado_a_eliminar):
    # Creamos una nueva lista excluyendo el estado que queremos eliminar
    nueva_lista = [estado for estado in listaFrontera if estado != estado_a_eliminar]
    
    # Volvemos a transformar la lista en un heap
    heapq.heapify(nueva_lista)
    return nueva_lista

def A_estrella(mapi, inicio, destino):
    # Inicializar las listas
    listaInterior = []   # Evaluados
    listaFrontera = []   # Por evaluar

    # Crear el estado inicial
    estado_inicial = Estado(inicio)
    heapq.heappush(listaFrontera, estado_inicial)

    # Movimientos posibles: [(movimiento columna, movimiento fila, coste)]
    movimientos = [
        (0, 1, 1),   # Abajo
        (1, 0, 1),   # Derecha
        (0, -1, 1),  # Arriba
        (-1, 0, 1),  # Izquierda
        (-1, 1, 1.5),  # Diagonal Abajo-Izquierda
        (1, 1, 1.5),   # Diagonal Abajo-Derecha
        (1, -1, 1.5),  # Diagonal Arriba-Derecha
        (-1, -1, 1.5)  # Diagonal Arriba-Izquierda
    ]

    while listaFrontera:
        # Obtener el nodo con el menor valor de f (n)
        estado_actual = heapq.heappop(listaFrontera)

        # Verificar si hemos llegado al destino
        if estado_actual.casilla == destino:
            return reconstruir_camino(estado_actual), estado_actual.g

        # Agregar el nodo actual a la lista interior
        listaInterior.append(estado_actual)

        # Generar hijos (vecinos del nodo actual)
        for movimiento in movimientos:
            nueva_fila = estado_actual.casilla.getFila() + movimiento[1]
            nueva_col = estado_actual.casilla.getCol() + movimiento[0]
            nuevo_coste = movimiento[2]  # Coste del movimiento (1 o 1.5)
            nueva_casilla = Casilla(nueva_fila, nueva_col)

            # Verificar que la nueva casilla está dentro del mapa y es transitable
            if dentro_mapa(mapi, nueva_casilla) and bueno(mapi, nueva_casilla):
                g_prima = estado_actual.g + nuevo_coste  # Se ajusta el coste del movimiento
                nuevo_estado = Estado(nueva_casilla, estado_actual, g_prima, heuristica(nueva_casilla, destino))

                # Si el nuevo estado ya está en listaInterior, lo ignoramos
                if nuevo_estado in listaInterior:
                    continue

                # Verificar si ya está en la frontera con un mayor coste
                #encontrado = False
                for estado in listaFrontera:
                    if estado == nuevo_estado and estado.g > nuevo_estado.g:
                        #encontrado = True
                        listaFrontera = eliminar_estado(listaFrontera, estado)
                        break

                #if encontrado:
                heapq.heappush(listaFrontera, nuevo_estado)

    # Si llegamos aquí, no se encontró una solución
    return -1, -1

# función principal
def main():
    pygame.init()    
    
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa2.txt'
    else:
        file=sys.argv[-1]
         
    mapi=Mapa(file)     
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()      
                if pulsaBoton(mapi, pos)==1 or pulsaBoton(mapi, pos)==2:
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        print('Error: No hay origen o destino')
                    else:
                        camino=inic(mapi)
                        if pulsaBoton(mapi, pos)==1:
                            ###########################                                                 
                            #coste, cal=llamar a A estrella             
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                        else:
                            ###########################                                                   
                            #coste, cal=llamar a A estrella subepsilon                       
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            
                elif esMapa(mapi,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)
                        
                        if bueno(mapi, casO):
                            origen = casO
                            # Obtener y mostrar posiciones adyacentes accesibles
                            #adyacentes = obtener_adyacentes_accesibles(mapi, origen)
                            #frontera = obtener_lista_frontera(mapi, origen)
                            #print(f"Posiciones adyacentes accesibles desde ({origen.getCol()}, {origen.getFila()}): {adyacentes}")
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapi, casD):
                            destino=casD
                            caminoSol = A_estrella(mapi, origen, destino)
                            print(caminoSol)
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):                
                if camino[fil][col]!='.':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 25)
            textoCoste=fuente.render("Coste: "+str(coste), True, AMARILLO)            
            screen.blit(textoCoste, [anchoVentana-90, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render("Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
