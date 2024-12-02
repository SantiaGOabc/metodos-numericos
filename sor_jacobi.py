def sor(A, b, w, tol, max_iter, criterio, decimales):
    import numpy as np

    n = len(A)  
    x_prev = np.zeros(n) 
    iteraciones = []  

    for k in range(max_iter):
        x_new = np.zeros(n)  
        iteracion_actual = {"normal": list(np.round(x_prev, decimales)), "suavizado": [], "errores": []}

        for i in range(n):
            suma1 = sum(A[i][j] * x_prev[j] for j in range(i))  
            suma2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))  
            x_i_new = (b[i] - suma1 - suma2) / A[i][i]

            x_new[i] = (1 - w) * x_prev[i] + w * x_i_new

        iteracion_actual["suavizado"] = list(np.round(x_new, decimales))

        for i in range(n):
            if abs(x_new[i]) > 1e-10:  
                error = abs((x_new[i] - x_prev[i]) / x_new[i]) * 100
            else:
                error = float('inf')
            iteracion_actual["errores"].append(round(error, decimales))

        iteraciones.append(iteracion_actual)

        max_error = max(iteracion_actual["errores"])
        if criterio == "tolerancia" and max_error < tol:
            break

        x_prev = np.copy(x_new)

    return iteraciones, k + 1
