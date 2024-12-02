def sor_gauss_seidel(A, b, w, tol, max_iter, criterio, decimales):
    import numpy as np

    n = len(A)  
    x = np.zeros(n) 
    iteraciones = []  

    for k in range(max_iter):
        iteracion_actual = {"normal": list(np.round(x, decimales)), "suavizado": [], "errores": []}
        x_prev = np.copy(x)  

        for i in range(n):
            suma1 = sum(A[i][j] * x[j] for j in range(i))  # Valores ya actualizados
            suma2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))  # Valores antiguos
            x_i_new = (b[i] - suma1 - suma2) / A[i][i]

            x[i] = (1 - w) * x[i] + w * x_i_new

        iteracion_actual["suavizado"] = list(np.round(x, decimales))

        for i in range(n):
            if abs(x[i]) > 1e-10:  
                error = abs((x[i] - x_prev[i]) / x[i]) * 100
            else:
                error = float('inf')  
            iteracion_actual["errores"].append(round(error, decimales))

        iteraciones.append(iteracion_actual)

        max_error = max(iteracion_actual["errores"])
        if criterio == "tolerancia" and max_error < tol:
            break

    return iteraciones, k + 1
