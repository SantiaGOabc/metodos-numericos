import sympy as sp 

def verificar_variable(funcion_str):
    variables = sp.sympify(funcion_str).free_symbols
    if variables != {sp.Symbol('x')}:
        raise ValueError('La única variable permitida es "x".')

def newton_raphson(funcion_str, x0, tolerancia=None, max_iter=None):
    verificar_variable(funcion_str)
    
    x = sp.symbols('x')
    funcion = sp.sympify(funcion_str)
    derivada = sp.diff(funcion, x)
    f = sp.lambdify(x, funcion)
    f_deriv = sp.lambdify(x, derivada)

    tol = tolerancia if tolerancia is not None else 1e-6
    max_iter = max_iter if max_iter is not None else 100

    iteraciones = []
    x_actual = x0

    for i in range(1, max_iter + 1):
        fx = f(x_actual)
        fdx = f_deriv(x_actual)

        if fdx == 0:
            iteraciones.append({'iteracion': i, 'x_actual': x_actual, 'fx': fx, 'error': 'Derivada cero'})
            break

        x_nuevo = x_actual - fx / fdx

        iteraciones.append({'iteracion': i, 'x_actual': x_nuevo, 'fx': fx})

        if abs(x_nuevo - x_actual) < tol:
            break

        x_actual = x_nuevo

    return iteraciones, x_actual

    