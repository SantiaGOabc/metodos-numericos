def sor(A, b, w, tol, max_iter, criterio, decimales):
    import numpy as np

    n = len(A)  # Número de variables
    x_prev = np.zeros(n)  # Vector inicializado en ceros (valores iniciales)
    iteraciones = []  # Para almacenar los resultados de cada iteración

    for k in range(max_iter):
        x_new = np.zeros(n)  # Vector para almacenar los nuevos valores
        iteracion_actual = {"normal": list(np.round(x_prev, decimales)), "suavizado": [], "errores": []}

        for i in range(n):
            # Calcular el nuevo valor de x_i usando SIEMPRE los valores de la iteración anterior
            suma1 = sum(A[i][j] * x_prev[j] for j in range(i))  # Términos anteriores para las primeras variables
            suma2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))  # Términos posteriores para las últimas variables
            x_i_new = (b[i] - suma1 - suma2) / A[i][i]

            # Suavizar el nuevo valor de x_i
            x_new[i] = (1 - w) * x_prev[i] + w * x_i_new

        # Guardar los valores suavizados para esta iteración
        iteracion_actual["suavizado"] = list(np.round(x_new, decimales))

        # Calcular errores relativos para cada variable
        for i in range(n):
            if abs(x_new[i]) > 1e-10:  # Evitar divisiones por cero
                error = abs((x_new[i] - x_prev[i]) / x_new[i]) * 100
            else:
                error = float('inf')  # Si el denominador es muy pequeño
            iteracion_actual["errores"].append(round(error, decimales))

        iteraciones.append(iteracion_actual)

        # Verificar criterio de parada
        max_error = max(iteracion_actual["errores"])
        if criterio == "tolerancia" and max_error < tol:
            break

        # Actualizar x_prev al final de la iteración
        x_prev = np.copy(x_new)

    return iteraciones, k + 1
