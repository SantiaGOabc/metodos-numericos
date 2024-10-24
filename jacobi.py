import re

def extraer_coeficientes(ecuacion, tamano):
    # Extrae los coeficientes y el término independiente de una ecuación en formato texto
    coeficientes = [0] * tamano
    ecuacion = ecuacion.replace(' ', '')  # Eliminamos espacios
    pattern = re.compile(r'([+-]?\d*\.?\d*)X(\d+)')
    matches = pattern.findall(ecuacion)
    for match in matches:
        coef = float(match[0]) if match[0] != '' and match[0] != '+' and match[0] != '-' else (1.0 if match[0] != '-' else -1.0)
        var_index = int(match[1]) - 1  # Convertir X1 a índice 0
        coeficientes[var_index] = coef
    
    # Obtener el término independiente
    independiente = float(ecuacion.split('=')[-1])
    
    return coeficientes, independiente
def es_diagonalmente_dominante(A):
    """
    Verifica si una matriz es diagonalmente dominante.
    """
    n = len(A)
    for i in range(n):
        suma_fila = sum(abs(A[i][j]) for j in range(n) if j != i)  # Suma de todos los elementos de la fila excepto el de la diagonal
        if abs(A[i][i]) < suma_fila:
            return False
    return True

def reorganizar_filas(A, b):
    """
    Intenta reorganizar las filas de la matriz A para que sea diagonalmente dominante.
    Si no es posible, devuelve False.
    """
    from itertools import permutations
    n = len(A)
    for perm in permutations(range(n)):  # Permutamos las filas
        A_permutado = [A[i] for i in perm]
        b_permutado = [b[i] for i in perm]
        if es_diagonalmente_dominante(A_permutado):
            return A_permutado, b_permutado
    return None, None

def jacobi(A, b, tol, max_iter, criterio, decimales=5):
    """
    Método de Jacobi con cálculo de margen de error y redondeo de resultados a una cantidad específica de decimales.
    """
    # Verificar si la matriz es diagonalmente dominante
    if not es_diagonalmente_dominante(A):
        # Intentar reorganizar las filas
        A, b = reorganizar_filas(A, b)
        if A is None:
            return None, "No se puede resolver por Jacobi: la matriz no es diagonalmente dominante."

    n = len(A)
    x_old = [0] * n  # Vector inicial en ceros
    iteraciones = []

    for k in range(max_iter):
        x_new = x_old[:]  # Empezamos con los valores anteriores
        errores = []  # Almacenamos los errores de cada variable en la iteración actual
        for i in range(n):
            sum1 = sum(A[i][j] * x_old[j] for j in range(n) if j != i)  # Suma de los términos excepto el actual
            x_new[i] = (b[i] - sum1) / A[i][i]

            # Calcular el error usando la fórmula 1 - (x_anterior / x_actual)
            if x_new[i] != 0:
                error = 1 - (x_old[i] / x_new[i])
            else:
                error = float('inf')  # Evitar división por 0
            errores.append(abs(error))

        # El margen de error es el máximo error entre las variables
        residuo = max(errores)
        iteraciones.append({
            'iteracion': k + 1, 
            'x_actual': [round(x, decimales) for x in x_new],  # Redondeamos los valores
            'residuo': round(residuo, decimales),
            'errores': [round(e, decimales) for e in errores]
        })

        # Detener según el criterio elegido
        if criterio == "tolerancia" and residuo < tol:
            return x_new, iteraciones, k + 1  # Devuelve el resultado, las iteraciones y la iteración en la que se alcanzó el resultado
        elif criterio == "iteraciones" and k + 1 == max_iter:
            break

        # Actualizar para la próxima iteración
        x_old = x_new[:]

    return [round(x, decimales) for x in x_new], iteraciones, max_iter


