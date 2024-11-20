def sor_gauss_seidel(A, b, w, tol, max_iter, criterio, decimales):
    import numpy as np

    n = len(A)  # Número de variables
    x = np.zeros(n)  # Vector inicializado en ceros
    iteraciones = []  # Para almacenar los resultados de cada iteración

    for k in range(max_iter):
        iteracion_actual = {"normal": list(np.round(x, decimales)), "suavizado": [], "errores": []}
        x_prev = np.copy(x)  # Copia del vector antes de actualizar

        for i in range(n):
            # Calcular el nuevo valor de x_i utilizando los valores más recientes
            suma1 = sum(A[i][j] * x[j] for j in range(i))  # Valores ya actualizados
            suma2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))  # Valores antiguos
            x_i_new = (b[i] - suma1 - suma2) / A[i][i]

            # Aplicar suavización con el factor w
            x[i] = (1 - w) * x[i] + w * x_i_new

        # Guardar los valores suavizados para esta iteración
        iteracion_actual["suavizado"] = list(np.round(x, decimales))

        # Calcular errores relativos para cada variable
        for i in range(n):
            if abs(x[i]) > 1e-10:  # Evitar divisiones por cero
                error = abs((x[i] - x_prev[i]) / x[i]) * 100
            else:
                error = float('inf')  # Si el denominador es muy pequeño
            iteracion_actual["errores"].append(round(error, decimales))

        iteraciones.append(iteracion_actual)

        # Verificar criterio de parada
        max_error = max(iteracion_actual["errores"])
        if criterio == "tolerancia" and max_error < tol:
            break

    return iteraciones, k + 1
