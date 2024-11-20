import re

def extraer_coeficientes(ecuacion, tamano):
    coeficientes = [0] * tamano
    ecuacion = ecuacion.replace(' ', '')  # quitar espacios
    pattern = re.compile(r'([+-]?\d*\.?\d*)X(\d+)')
    matches = pattern.findall(ecuacion)
    for match in matches:
        coef = float(match[0]) if match[0] != '' and match[0] != '+' and match[0] != '-' else (1.0 if match[0] != '-' else -1.0)
        var_index = int(match[1]) - 1  # Convertir X1 a índice al 0
        coeficientes[var_index] = coef
    independiente = float(ecuacion.split('=')[-1])
    
    return coeficientes, independiente

def es_diagonalmente_dominante(A):
    n = len(A)
    for i in range(n):
        suma_fila = sum(abs(A[i][j]) for j in range(n) if j != i)  
        if abs(A[i][i]) < suma_fila:
            return False
    return True

def reorganizar_filas(A, b):
    from itertools import permutations
    n = len(A)
    for perm in permutations(range(n)):  # Permutamos las filas
        A_permutado = [A[i] for i in perm]
        b_permutado = [b[i] for i in perm]
        if es_diagonalmente_dominante(A_permutado):
            return A_permutado, b_permutado
    return None, None

def jacobi(A, b, tol, max_iter, criterio, decimales=5):
    if not es_diagonalmente_dominante(A):
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
            sum1 = sum(A[i][j] * x_old[j] for j in range(n) if j != i) 
            x_new[i] = (b[i] - sum1) / A[i][i]

            # Calcular el error usando la fórmula de error
            if x_new[i] != 0:
                error = 1 - (x_old[i] / x_new[i])
            else:
                error = float('inf')  # Evitar división por 0
            errores.append(abs(error))

        residuo = max(errores)
        iteraciones.append({
            'iteracion': k + 1, 
            'x_actual': [round(x, decimales) for x in x_new],  # Redondeamos los valores
            'residuo': round(residuo, decimales),
            'errores': [round(e, decimales) for e in errores]
        })

        # Detener
        if criterio == "tolerancia" and residuo < tol:
            return x_new, iteraciones, k + 1  # Devuelve resulado
        elif criterio == "iteraciones" and k + 1 == max_iter:
            break

        x_old = x_new[:]

    return [round(x, decimales) for x in x_new], iteraciones, max_iter


