from jacobi import es_diagonalmente_dominante, reorganizar_filas
def gauss_seidel(A, b, tol, max_iter, criterio, decimales=6):
    # Verificar si la matriz es diagonalmente dominante
    if not es_diagonalmente_dominante(A):
        # Intentar reorganizar las filas
        A, b = reorganizar_filas(A, b)
        if A is None:
            return None, "No se puede resolver por Gauss-Seidel: la matriz no es diagonalmente dominante."

    n = len(A)
    x = [0] * n  # Vector inicial en ceros
    iteraciones = []

    for k in range(max_iter):
        x_old = x[:]  
        errores = [] 
        
        for i in range(n):
            sum1 = sum(A[i][j] * x[j] for j in range(n) if j != i) 
            x[i] = (b[i] - sum1) / A[i][i]

            # Calcular el error
            if x[i] != 0:
                error = 1 - (x_old[i] / x[i])
            else:
                error = float('inf')  # Evitar división por 0
            errores.append(abs(error))

        # El margen de error es el máximo error entre las variables
        residuo = max(errores)
        iteraciones.append({
            'iteracion': k + 1, 
            'x_actual': [round(val, decimales) for val in x],  # Redondeamos los valores
            'residuo': round(residuo, decimales),
            'errores': [round(e, decimales) for e in errores]
        })

        # Detener según el criterio elegido
        if criterio == "tolerancia" and residuo < tol:
            return x, iteraciones, k + 1  # Devuelve resultado
        elif criterio == "iteraciones" and k + 1 == max_iter:
            break

    return [round(val, decimales) for val in x], iteraciones, max_iter
