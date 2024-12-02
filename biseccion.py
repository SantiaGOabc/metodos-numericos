import sympy as sp
def biseccion(funcion, a, b, tolerancia, max_iter, criterio_detencion, decimales=6):
    x = sp.symbols('x')
    e = sp.exp(1)
    f = sp.sympify(funcion, locals={"e": e})

    if f.subs(x, a) * f.subs(x, b) >= 0:
        raise ValueError("La función debe tener un cambio de signo entre a y b.")

    iteraciones = []
    resultado = None

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f.subs(x, c)
        error = abs(b - a) / 2

        iteraciones.append({
            'iteracion': i + 1,
            'a': round(float(a), decimales),
            'b': round(float(b), decimales),
            'c': round(float(c), decimales),
            'fc': round(float(fc), decimales),
            'error': round(error * 100, decimales)  # Error en porcentaje
        })

        if criterio_detencion == 'tolerancia' and (abs(fc) < tolerancia or error < tolerancia):
            resultado = c
            break
        elif criterio_detencion == 'max_iter' and i >= max_iter - 1:
            resultado = c
            break

        if f.subs(x, a) * fc < 0:
            b = c
        else:
            a = c

    if resultado is None:
        resultado = c

    return iteraciones, round(float(resultado), decimales), round(error * 100, decimales)  # Error en porcentaje
