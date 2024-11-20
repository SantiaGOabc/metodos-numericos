import sympy as sp
from sympy import symbols, solve, latex
def resolver_sistemas_no_lineales(ecuaciones_str, variables_str):
    try:
        ecuaciones = [sp.sympify(ec.strip()) for ec in ecuaciones_str]
        variables = [sp.symbols(var.strip()) for var in variables_str]

        # Resolver el sistema de ecuaciones
        solucion = sp.solve(ecuaciones, variables)

        # Convertir la solución a formato LaTeX
        solucion_latex = latex(solucion)
        return solucion_latex
    except Exception as e:
        return f"Error al resolver el sistema: {e}"
