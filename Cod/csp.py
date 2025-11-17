from variable import Variable
from typing import List, Tuple, Dict, Optional
import time

# Variable global para habilitar/deshabilitar prints de debug
DEBUG = False

# Índices para los contadores
REC = 0  # Recursiones
ASI = 1  # Asignaciones


#########################################################################
#                    FUNCIONES AUXILIARES                               #
#########################################################################

def vecinos_de(f: int, c: int) -> List[Tuple[int, int]]:
    """
    Devuelve las posiciones (fila, col) que son vecinas de (f, c) en Sudoku.
    Incluye: misma fila, misma columna y misma caja 3x3.
    """
    vecinos = set()

    # Misma fila
    for j in range(9):
        if j != c:
            vecinos.add((f, j))

    # Misma columna
    for i in range(9):
        if i != f:
            vecinos.add((i, c))

    # Misma caja 3x3
    f0, c0 = (f // 3) * 3, (c // 3) * 3
    for i in range(f0, f0 + 3):
        for j in range(c0, c0 + 3):
            if (i, j) != (f, c):
                vecinos.add((i, j))

    return list(vecinos)


def calcular_dominio_inicial(variables: List[Variable], f: int, c: int) -> List[int]:
    """
    Calcula el dominio inicial de una celda (f, c) eliminando valores
    que aparecen en sus vecinos ya asignados.
    Usa las variables en lugar del tablero.
    """
    usados = set()
    vecinos = vecinos_de(f, c)
    
    # Buscar valores usados en vecinos
    for var in variables:
        if (var.fila, var.col) in vecinos and var.valor is not None:
            usados.add(var.valor)
    
    return [v for v in range(1, 10) if v not in usados]


def crear_variables(copTab, recortar_dominios=True) -> List[Variable]:
    """
    Crea las variables del CSP a partir del tablero inicial.
    
    Parámetros:
    - copTab: copia del tablero inicial (para identificar celdas fijas)
    - recortar_dominios: si True, calcula dominios iniciales reducidos; 
                         si False, usa dominios completos [1..9]
    
    Retorna lista de variables ordenadas por posición (fila, columna).
    """
    variables = []
    
    # Primera pasada: crear variables con valores fijos
    for f in range(9):
        for c in range(9):
            ch_inicial = copTab.getCelda(f, c)

            if ch_inicial != '0':
                # Celda fija
                v = int(ch_inicial)
                var = Variable(fila=f, col=c, valor=v, fija=True, dominio=[v])
            else:
                # Celda no fija (dominio se calculará después)
                var = Variable(fila=f, col=c, valor=None, fija=False, dominio=list(range(1, 10)))
            
            variables.append(var)
    
    # Segunda pasada: calcular dominios reducidos si es necesario
    if recortar_dominios:
        for var in variables:
            if not var.fija:
                var.dominio = calcular_dominio_inicial(variables, var.fila, var.col)
    
    return variables


def escribir_solucion(variables: List[Variable], tablero) -> None:
    """
    Escribe la solución (valores de variables) en el tablero.
    """
    for var in variables:
        f, c = var.fila, var.col
        if var.valor is not None:
            tablero.setCelda(f, c, str(var.valor))
        else:
            tablero.setCelda(f, c, '0')


def es_valido(variables: List[Variable], idx: int) -> bool:
    """
    Comprueba si la asignación de variables[idx] es válida.
    Verifica que no haya conflictos con vecinos ya asignados.
    """
    var = variables[idx]
    if var.valor is None:
        return False
    
    vecinos = vecinos_de(var.fila, var.col)
    
    for v in variables:
        if (v.fila, v.col) in vecinos:
            if v.valor is not None and v.valor == var.valor:
                return False
    
    return True


def seleccionar_variable(variables: List[Variable]) -> Optional[int]:
    """
    Selecciona la siguiente variable a asignar (orden fijo).
    Retorna el índice de la variable, o None si todas están asignadas.
    """
    for i, var in enumerate(variables):
        if not var.fija and var.valor is None:
            return i
    return None


#########################################################################
#                    ALGORITMO BACKTRACKING (BT)                        #
#########################################################################

def BT(variables: List[Variable], counters: List[int]) -> bool:
    """
    Algoritmo de Backtracking para resolver el Sudoku.
    
    - Itera sobre el dominio de cada variable
    - Comprueba restricciones antes de asignar
    - Cuenta recursiones y asignaciones

    - Hace recursión cuando encuentra un valor válido -> Por eso no aumenta el contador de recursiones
    - Disminuye cantidad de asignaciones porque no intenta valores que es_valido() rechazaría
    """
    counters[REC] += 1
    
    # Seleccionar siguiente variable (orden fijo)
    idx = seleccionar_variable(variables)
    
    if idx is None:
        # Todas las variables asignadas: solución encontrada
        return True

    var = variables[idx]
    
    # Probar cada valor del dominio
    for valor in var.dominio:
        var.valor = valor
        counters[ASI] += 1
        
        # Comprobar si es válido
        if es_valido(variables, idx):
            # Recursión
            if BT(variables, counters):
                return True

        # Deshacer asignación
        var.valor = None

    return False


def resolver_BT(copTab, recortar_dominios=True) -> Tuple[bool, List[Variable], List[int]]:
    """
    Resuelve el Sudoku usando Backtracking.
    
    Parámetros:
    - copTab: tablero inicial
    - recortar_dominios: si True, usa dominios iniciales reducidos
    
    Retorna: (exito, variables, counters)
    """
    # Inicializar contadores
    counters = [0, 0]  # [recursiones, asignaciones]
    
    # Crear variables
    variables = crear_variables(copTab, recortar_dominios)
    
    # Ejecutar algoritmo
    t_inicio = time.time()
    exito = BT(variables, counters)
    t_fin = time.time()
    
    # Mostrar resultados
    print(f"--- BACKTRACKING ---")
    print(f"Recorte de dominios: {recortar_dominios}")
    print(f"Recursiones: {counters[REC]}")
    print(f"Asignaciones: {counters[ASI]}")
    print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    
    return exito, variables, counters


#########################################################################
#                  ALGORITMO FORWARD CHECKING (FC)                      #
#########################################################################

def forward_checking(variables: List[Variable], idx: int, valor: int) -> Tuple[bool, Dict[int, List[Tuple[int, int]]]]:
    """
    Realiza forward checking: poda el valor asignado de los dominios
    de las variables NO asignadas relacionadas.

    Retorna:
    - consistente: True si ningún dominio quedó vacío
    - podas: diccionario {idx_var: [(valor, posicion), ...]} para restaurar
    """
    var = variables[idx]
    vecinos = vecinos_de(var.fila, var.col)
    podas = {}
    
    # Buscar TODAS las variables no asignadas que sean vecinas
    for i, vi in enumerate(variables):
        if i == idx:
            continue
            
        #if vi.fija or vi.valor is not None:
         #   continue

        # Comprobar si es vecina
        if (vi.fila, vi.col) in vecinos:
            # Intentar podar el valor del dominio
            if valor in vi.dominio:
                pos = vi.dominio.index(valor)
                vi.dominio.remove(valor)
                
                if i not in podas:
                    podas[i] = []
                podas[i].append((valor, pos))
                
                if DEBUG:
                    print(f"  Poda: quito {valor} de Var({vi.fila},{vi.col}), |dom|={len(vi.dominio)}")
                
                # Comprobar dominio vacío
                if len(vi.dominio) == 0:
                    if DEBUG:
                        print(f"  ✗ Dominio vacío en Var({vi.fila},{vi.col})")
                    return False, podas
    
    return True, podas


def restaurar_podas(variables: List[Variable], podas: Dict[int, List[Tuple[int, int]]]) -> None:
    """
    Restaura los valores podados en los dominios.
    """
    for idx, lista_podas in podas.items():
        var = variables[idx]
        for valor, pos in lista_podas:
            var.dominio.insert(pos, valor)
            if DEBUG:
                print(f"  Restaura: {valor} en Var({var.fila},{var.col}), |dom|={len(var.dominio)}")


def FC(variables: List[Variable], counters: List[int]) -> bool:
    """
    Algoritmo de Forward Checking para resolver el Sudoku.
    
    - NO comprueba restricciones (asume dominios bien inicializados)
    - Poda dominios de variables no asignadas vecinas
    - Usa orden de variables fijo
    """
    counters[REC] += 1
    
    # Seleccionar siguiente variable (orden fijo -> esquema de clase)
    var_idx = seleccionar_variable(variables)
    
    if var_idx is None:
        # Todas las variables asignadas: solución encontrada
        return True

    var = variables[var_idx]
    
    if DEBUG:
        print(f"[{counters[REC]}] Var({var.fila},{var.col}), dom={var.dominio}")
    
    # Probar cada valor del dominio
    for valor in list(var.dominio):  # Copiar dominio para iterar
        var.valor = valor
        counters[ASI] += 1
        
        if DEBUG:
            print(f"  Asigna Var({var.fila},{var.col}) = {valor}")
        
        # Forward checking: podar dominios
        consistente, podas = forward_checking(variables, var_idx, valor)

        if consistente:
            # Recursión
            if FC(variables, counters):
                return True

        # Restaurar podas
        restaurar_podas(variables, podas)

        # Deshacer asignación
        var.valor = None
        
        if DEBUG:
            print(f"  Backtrack de Var({var.fila},{var.col}) = {valor}")

    return False


def resolver_FC(copTab, recortar_dominios=True) -> Tuple[bool, List[Variable], List[int]]:
    """
    Resuelve el Sudoku usando Forward Checking.
    
    Parámetros:
    - copTab: tablero inicial
    - recortar_dominios: si True, usa dominios iniciales reducidos
    
    Retorna: (exito, variables, counters)
    """
    # Inicializar contadores
    counters = [0, 0]  # [recursiones, asignaciones]
    
    # Crear variables
    variables = crear_variables(copTab, recortar_dominios)
    
    # Ejecutar algoritmo
    t_inicio = time.time()
    exito = FC(variables, counters)
    t_fin = time.time()
    
    # Mostrar resultados
    print(f"--- FORWARD CHECKING ---")
    print(f"Recorte de dominios: {recortar_dominios}")
    print(f"Recursiones: {counters[REC]}")
    print(f"Asignaciones: {counters[ASI]}")
    print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    
    return exito, variables, counters


#########################################################################
#                        ALGORITMO AC-3                                  #
#########################################################################

def tiene_apoyo(valor: int, dominio_vecino: List[int]) -> bool:
    """
    Verifica si un valor tiene apoyo en el dominio de un vecino.
    En Sudoku: valor tiene apoyo si existe algún b en dominio_vecino donde b ≠ valor.
    Equivalente: valor NO tiene apoyo si dominio_vecino = {valor}.
    """
    for b in dominio_vecino:
        if b != valor:
            return True
    return False


def revisar(Xi: Variable, Xj: Variable) -> bool:
    """
    Revisa el arco <Xi, Xj> y elimina valores de Di que no tienen apoyo en Dj.
    
    Retorna True si se eliminó algún valor de Di, False en caso contrario.
    """
    eliminado = False
    valores_a_eliminar = []
    
    # Buscar valores sin apoyo
    for valor in Xi.dominio:
        if not tiene_apoyo(valor, Xj.dominio):
            valores_a_eliminar.append(valor)
            eliminado = True
    
    # Eliminar valores sin apoyo
    for valor in valores_a_eliminar:
        Xi.dominio.remove(valor)
        if DEBUG:
            print(f"  Elimina {valor} de Var({Xi.fila},{Xi.col}), |dom|={len(Xi.dominio)}")
    
    return eliminado


def AC3(variables: List[Variable]) -> bool:
    """
    Algoritmo AC-3 para garantizar consistencia de arco.
    
    Retorna:
    - True si el CSP es consistente (ningún dominio quedó vacío)
    - False si se detecta inconsistencia (algún dominio quedó vacío)
    """
    # 1. Crear cola con todos los arcos
    from collections import deque
    cola = deque()
    
    # Crear mapeo de posición a índice para acceso rápido
    pos_to_idx = {(v.fila, v.col): i for i, v in enumerate(variables)}
    
    # Añadir todos los arcos <Xi, Xj> donde Xi y Xj son vecinas
    for i, Xi in enumerate(variables):
        if Xi.fija:  # Las variables fijas no cambian su dominio
            continue
        
        vecinos_pos = vecinos_de(Xi.fila, Xi.col)
        for (vf, vc) in vecinos_pos:
            j = pos_to_idx.get((vf, vc))
            if j is not None:
                Xj = variables[j]
                cola.append((i, j))  # Añadir arco <Xi, Xj>
    
    if DEBUG:
        print(f"AC3: cola inicial con {len(cola)} arcos")
    
    arcos_procesados = 0
    
    # 2. Procesar arcos hasta que la cola esté vacía
    while cola:
        i, j = cola.popleft()
        Xi = variables[i]
        Xj = variables[j]
        
        arcos_procesados += 1
        
        if DEBUG:
            print(f"Procesando arco <Var({Xi.fila},{Xi.col}), Var({Xj.fila},{Xj.col})>")
        
        # 3. Revisar el arco
        if revisar(Xi, Xj):
            # 4. Comprobar dominio vacío
            if len(Xi.dominio) == 0:
                if DEBUG:
                    print(f"✗ Dominio vacío en Var({Xi.fila},{Xi.col}) → Inconsistente")
                return False
            
            # 5. Añadir arcos entrantes <Xk, Xi> a la cola
            vecinos_Xi = vecinos_de(Xi.fila, Xi.col)
            for (vf, vc) in vecinos_Xi:
                k = pos_to_idx.get((vf, vc))
                if k is not None and k != j:  # Todos los vecinos excepto Xj
                    Xk = variables[k]
                    if not Xk.fija:  # Solo si Xk no es fija
                        cola.append((k, i))
                        if DEBUG:
                            print(f"  Añade arco <Var({Xk.fila},{Xk.col}), Var({Xi.fila},{Xi.col})> a la cola")
    
    if DEBUG:
        print(f"✓ AC3 completado. Arcos procesados: {arcos_procesados}")
    
    return True


def mostrar_dominios(variables: List[Variable], titulo: str = "Dominios") -> None:
    """
    Muestra los dominios de todas las variables no fijas en orden de fila, columna.
    """
    print(f"\n{'='*70}")
    print(f"{titulo}")
    print('='*70)
    
    # Filtrar variables no fijas y ordenar por (fila, col)
    no_fijas = [v for v in variables if not v.fija]
    no_fijas_ordenadas = sorted(no_fijas, key=lambda v: (v.fila, v.col))
    
    print(f"Total variables no fijas: {len(no_fijas_ordenadas)}\n")
    
    # Mostrar dominios en orden
    for var in no_fijas_ordenadas:
        tam = len(var.dominio)
        print(f"Var({var.fila},{var.col}): {var.dominio}  (|D|={tam})")
    
    # Mostrar estadísticas al final
    print(f"\n{'-'*70}")
    print("Distribución por tamaño de dominio:")
    
    por_tamano = {}
    for var in no_fijas_ordenadas:
        tam = len(var.dominio)
        por_tamano[tam] = por_tamano.get(tam, 0) + 1
    
    for tam in sorted(por_tamano.keys()):
        print(f"  |D|={tam}: {por_tamano[tam]} variables")
    
    print('='*70)


def resolver_AC3(variables: List[Variable]) -> bool:
    """
    Ejecuta AC-3 sobre las variables y muestra dominios antes y después.
    
    Retorna True si es consistente, False si detecta inconsistencia.
    """
    print("\n" + "="*70)
    print("EJECUTANDO AC-3")
    print("="*70)
    
    # Mostrar dominios antes
    mostrar_dominios(variables, "DOMINIOS ANTES DE AC-3")
    
    # Ejecutar AC-3
    t_inicio = time.time()
    consistente = AC3(variables)
    t_fin = time.time()
    
    # Mostrar dominios después
    if consistente:
        mostrar_dominios(variables, "DOMINIOS DESPUÉS DE AC-3")
        print(f"\n✓ AC-3 completado exitosamente")
        print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    else:
        print(f"\n✗ AC-3 detectó INCONSISTENCIA (dominio vacío)")
        print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    
    print("="*70)
    
    return consistente


#########################################################################
#                    FUNCIONES DE RESOLUCIÓN PARA MAIN                  #
#########################################################################

def resolver_backtracking(tablero, copTab, recortar_dominios=True, variables=None) -> bool:
    """
    Wrapper para llamar desde main.py.
    
    Si se pasan variables (ej: después de AC3), hace una copia profunda para no modificarlas.
    Si no, crea nuevas variables con el recorte especificado.
    """
    if variables is None:
        exito, variables_bt, _ = resolver_BT(copTab, recortar_dominios)
    else:
        # Hacer copia profunda de variables para no modificar las originales
        import copy as copy_module
        variables_bt = copy_module.deepcopy(variables)
        
        # Resetear valores asignados pero mantener dominios reducidos
        for var in variables_bt:
            if not var.fija:
                var.valor = None
        
        counters = [0, 0]
        t_inicio = time.time()
        exito = BT(variables_bt, counters)
        t_fin = time.time()
        
        print(f"--- BACKTRACKING (con dominios reducidos por AC-3) ---")
        print(f"Recursiones: {counters[REC]}")
        print(f"Asignaciones: {counters[ASI]}")
        print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    
    if exito:
        escribir_solucion(variables_bt, tablero)
    
    return exito


def resolver_forward_checking(tablero, copTab, recortar_dominios=True, variables=None) -> bool:
    """
    Wrapper para llamar desde main.py.
    
    Si se pasan variables (ej: después de AC3), hace una copia profunda para no modificarlas.
    Si no, crea nuevas variables con el recorte especificado.
    
    IMPORTANTE: FC modifica dominios durante la búsqueda. Usar copia profunda garantiza
    que cada ejecución empiece con los mismos dominios.
    """
    if variables is None:
        exito, variables_fc, _ = resolver_FC(copTab, recortar_dominios)
    else:
        # Hacer copia profunda de variables para no modificar las originales
        # CRÍTICO para FC: FC modifica dominios y no los restaura completamente
        import copy as copy_module
        variables_fc = copy_module.deepcopy(variables)
        
        # Resetear valores asignados pero mantener dominios reducidos
        for var in variables_fc:
            if not var.fija:
                var.valor = None
        
        counters = [0, 0]
        t_inicio = time.time()
        exito = FC(variables_fc, counters)
        t_fin = time.time()
        
        print(f"--- FORWARD CHECKING (con dominios reducidos por AC-3) ---")
        print(f"Recursiones: {counters[REC]}")
        print(f"Asignaciones: {counters[ASI]}")
        print(f"Tiempo: {t_fin - t_inicio:.4f} segundos")
    
    if exito:
        escribir_solucion(variables_fc, tablero)
    
    return exito
