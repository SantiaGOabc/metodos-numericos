from flask import Flask, render_template, request, session, redirect, url_for
from gauss_seidel import gauss_seidel
from newton import newton_raphson
from no_lineal import resolver_sistemas_no_lineales
from jacobi import jacobi, extraer_coeficientes, es_diagonalmente_dominante, reorganizar_filas
from sor_jacobi import sor
from sor_gauss_seidel import sor_gauss_seidel
from biseccion import biseccion
import re



app = Flask(__name__)
app.secret_key = 'ñ' 

def procesar_funcion(funcion):
    """
    Corrige la entrada del usuario, permitiendo ^ como operador de potencia
    y agregando '*' entre números y variables si es necesario.
    """
    # Reemplaza ^ por ** para manejar potencias
    funcion = funcion.replace('^', '**')

    # Agrega '*' entre un número y una variable (ejemplo: 4x -> 4*x)
    funcion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion)

    # Agrega '*' entre una variable y un número (ejemplo: x2 -> x*2)
    funcion = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', funcion)

    return funcion


# Ruta para el método de bisección
@app.route('/biseccion', methods=['GET', 'POST'])
def biseccion_route():
    if request.method == 'POST':
        try:
            # Captura y procesa los datos del formulario
            funcion = request.form['funcion']
            funcion = procesar_funcion(funcion)

            a = float(request.form['a'])
            b = float(request.form['b'])
            criterio_detencion = request.form['criterio_detencion']
            decimales = int(request.form.get('decimales', 6))

            tolerancia = request.form.get('tolerancia', None)
            max_iter = request.form.get('max_iter', None)

            tolerancia = float(tolerancia) if tolerancia else None
            max_iter = int(max_iter) if max_iter else None

            # Ejecutar el método de bisección
            iteraciones, resultado, error = biseccion(funcion, a, b, tolerancia or 1e-6, max_iter or 100, criterio_detencion, decimales)

            return render_template('biseccion.html', iteraciones=iteraciones, resultado=resultado, error=error)

        except ValueError as e:
            return render_template('biseccion.html', error=str(e))
        except Exception as e:
            return render_template('biseccion.html', error="Error inesperado. Verifica los valores ingresados.")
    
    return render_template('biseccion.html')




#GAUSS SEIDEL
@app.route('/seleccionar_tamano_gauss_seidel', methods=['GET', 'POST'])
def seleccionar_tamano_gauss_seidel():
    if request.method == 'POST':
        tamano_matriz = int(request.form['tamano_matriz'])
        return render_template('gauss_seidel.html', matriz_generada=True, tamano_matriz=tamano_matriz)
    else:
        return render_template('gauss_seidel.html', matriz_generada=False)
    


@app.route('/resolver_gauss_seidel', methods=['POST'])
def resolver_gauss_seidel():
    tamano_matriz = int(request.form['tamano_matriz'])
    A = []
    b = []
    
    # Extraer valores de la matriz A
    for i in range(tamano_matriz):
        fila = []
        for j in range(tamano_matriz):
            fila.append(float(request.form[f'A_{i}_{j}']))
        A.append(fila)
    
    # Extraer valores del vector b
    for i in range(tamano_matriz):
        b.append(float(request.form[f'b_{i}']))

    criterio = request.form['criterio']
    
    if criterio == "tolerancia":
        tol = float(request.form['tolerancia'])
        max_iter = 100 
    else:
        tol = None
        max_iter = int(request.form['max_iter'])

    # los decimales que s etoma en cuenta
    decimales = int(request.form.get('decimales', 5))

    # Resolver Gauss-Seidel
    resultado, iteraciones, iteracion_final = gauss_seidel(A, b, tol, max_iter, criterio, decimales)

    if resultado is None:
        return render_template('gauss_seidel.html', matriz_generada=True, tamano_matriz=tamano_matriz, error=iteraciones)
    else:
        return render_template('gauss_seidel.html', matriz_generada=True, tamano_matriz=tamano_matriz, 
                               resultado=resultado, iteraciones=iteraciones, iteracion_final=iteracion_final)

# Ruta para el método de Jacobi
@app.route('/seleccionar_tamano_jacobi', methods=['GET', 'POST'])
def seleccionar_tamano_jacobi():
    if request.method == 'POST':
        tamano_matriz = int(request.form['tamano_matriz'])
        return render_template('jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz)
    else:
        return render_template('jacobi.html', matriz_generada=False)
@app.route('/resolver_jacobi', methods=['POST'])
def resolver_jacobi():
    tamano_matriz = int(request.form['tamano_matriz'])
    A = []
    b = []
    
    # Extraer valores de la matriz A
    for i in range(tamano_matriz):
        fila = []
        for j in range(tamano_matriz):
            fila.append(float(request.form[f'A_{i}_{j}']))
        A.append(fila)
    
    # Extraer valores del vector b
    for i in range(tamano_matriz):
        b.append(float(request.form[f'b_{i}']))

    criterio = request.form['criterio']
    
    if criterio == "tolerancia":
        tol = float(request.form['tolerancia'])
        max_iter = 100 
    else:
        tol = None
        max_iter = int(request.form['max_iter'])

    decimales = int(request.form.get('decimales', 6))

    if not es_diagonalmente_dominante(A):
        A, b = reorganizar_filas(A, b)
        if A is None:
            error_message = "La matriz no es diagonalmente dominante y no se puede reorganizar para cumplir con esta condición."
            return render_template('jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz, error=error_message)
        
    resultado, iteraciones, iteracion_final = jacobi(A, b, tol, max_iter, criterio, decimales)

    if resultado is None:
        # Mostrar mensaje de error si no se puede resolver por Jacobi
        return render_template('jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz, error="No se pudo calcular el resultado.")
    else:
        # Mostrar el resultado, la iteración final y los errores de cada iteración
        return render_template('jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz, 
                               resultado=resultado, iteraciones=iteraciones, iteracion_final=iteracion_final)


# Seleccionar tamaño para SOR
@app.route('/seleccionar_tamano_sor_jacobi', methods=['GET', 'POST'])
def seleccionar_tamano_sor_jacobi():
    if request.method == 'POST':
        tamano_matriz = int(request.form['tamano_matriz'])
        return render_template('sor_jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz)
    else:
        return render_template('sor_jacobi.html', matriz_generada=False)


# Resolver SOR
@app.route('/resolver_sor_jacobi', methods=['POST'])
def resolver_sor_jacobi():
    tamano_matriz = int(request.form['tamano_matriz'])
    A = []
    b = []
    
    # Extraer valores de la matriz A
    for i in range(tamano_matriz):
        fila = []
        for j in range(tamano_matriz):
            fila.append(float(request.form[f'A_{i}_{j}']))
        A.append(fila)
    
    # Extraer valores del vector b
    for i in range(tamano_matriz):
        b.append(float(request.form[f'b_{i}']))

    # Extraer criterio de detención y parámetros
    criterio = request.form['criterio']
    tol = float(request.form.get('tolerancia', 0.0001)) if criterio == "tolerancia" else None
    max_iter = int(request.form.get('max_iter', 100))
    decimales = int(request.form.get('decimales', 6))
    w = float(request.form.get('w', 1.0))  # Factor de relajación

    iteraciones, iteracion_final = sor(A, b, w, tol, max_iter, criterio, decimales)

    if not iteraciones:
        return render_template('sor_jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz, error="No se pudo calcular el resultado.")
    else:
        return render_template('sor_jacobi.html', matriz_generada=True, tamano_matriz=tamano_matriz, 
                               iteraciones=iteraciones, iteracion_final=iteracion_final)

# Ruta para seleccionar el tamaño de la matriz
@app.route('/seleccionar_tamano_sor_gauss_seidel', methods=['GET', 'POST'])
def seleccionar_tamano_sor_gauss_seidel():
    if request.method == 'POST':
        try:
            tamano_matriz = int(request.form['tamano_matriz'])
        except ValueError:
            return render_template('sor_gauss_seidel.html', matriz_generada=False, error="Debes ingresar un tamaño válido.")
        return render_template('sor_gauss_seidel.html', matriz_generada=True, tamano_matriz=tamano_matriz)
    else:
        return render_template('sor_gauss_seidel.html', matriz_generada=False)

# Ruta para resolver el método SOR basado en Gauss-Seidel
@app.route('/resolver_sor_gauss_seidel', methods=['POST'])
def resolver_sor_gauss_seidel():
    try:
        tamano_matriz = int(request.form['tamano_matriz'])
        A = []
        b = []

        # Extraer valores de la matriz A
        for i in range(tamano_matriz):
            fila = []
            for j in range(tamano_matriz):
                fila.append(float(request.form[f'A_{i}_{j}']))
            A.append(fila)

        # Extraer valores del vector b
        for i in range(tamano_matriz):
            b.append(float(request.form[f'b_{i}']))

        criterio = request.form.get('criterio', 'tolerancia')  
        tol = float(request.form.get('tolerancia', 0.0001)) if criterio == "tolerancia" else None
        max_iter = request.form.get('max_iter', '100')
        if max_iter.strip() == '':
            max_iter = 100 
        else:
            max_iter = int(max_iter)
        decimales = int(request.form.get('decimales', 6))
        w = float(request.form.get('w', 1.0))  # Factor de relajación

        iteraciones, iteracion_final = sor_gauss_seidel(A, b, w, tol, max_iter, criterio, decimales)

        return render_template('sor_gauss_seidel.html', matriz_generada=True, tamano_matriz=tamano_matriz,
                               iteraciones=iteraciones, iteracion_final=iteracion_final)
    except ValueError as e:
        return render_template('sor_gauss_seidel.html', matriz_generada=False, error=f"Error en los datos: {e}")
    except Exception as e:
        return render_template('sor_gauss_seidel.html', matriz_generada=False, error=f"Error inesperado: {e}")
    
#CALCULOS bases
def cambio_de_base(numero, base_origen, base_destino):
    try:
        numero_decimal = int(str(numero), base_origen)
        if base_destino == 10:
            return numero_decimal
        else:
            # Convertir a la base de destino utilizando las bases del 2 al 16
            caracteres = "0123456789ABCDEF"
            resultado = ''
            while numero_decimal > 0:
                resultado = caracteres[numero_decimal % base_destino] + resultado
                numero_decimal //= base_destino
            return resultado if resultado else '0' 
    except ValueError:
        raise ValueError('Número o base inválidos.')
    
    


@app.route('/')
def index():
    return render_template('index.html')

# Todo Newton desde aqui 
@app.route('/newton', methods=['GET'])
def newton():
    session.clear()
    return render_template('newton.html', resultado=None, iteraciones=None)

@app.route('/calcular', methods=['POST'])
def calcular():
    funcion = request.form.get('funcion')
    x0 = float(request.form.get('x0'))
    tolerancia = request.form.get('tolerancia')
    max_iter = request.form.get('max_iter')
    mostrar_paso_a_paso = 'mostrar_paso_a_paso' in request.form

    # Procesar la función ingresada
    funcion = procesar_funcion(funcion)

    tolerancia = float(tolerancia) if tolerancia else None
    max_iter = int(max_iter) if max_iter else None

    try:
        iteraciones, resultado_final = newton_raphson(funcion, x0, tolerancia, max_iter)
        return render_template('newton.html', 
                               resultado=resultado_final, 
                               iteraciones=iteraciones if mostrar_paso_a_paso else None,
                               funcion=funcion, 
                               x0=x0, 
                               tolerancia=tolerancia, 
                               max_iter=max_iter, 
                               mostrar_paso_a_paso=mostrar_paso_a_paso)
    except ValueError as e:
        return render_template('newton.html', error=str(e), iteraciones=None)


# Cambio de base
@app.route('/cambio_base', methods=['GET', 'POST'])
def cambio_base():
    if request.method == 'POST':
        numero = request.form.get('numero')
        base_origen = int(request.form.get('base_origen'))
        base_destino = int(request.form.get('base_destino'))

        try:
            resultado = cambio_de_base(numero, base_origen, base_destino)
            return render_template('cambio_base.html', resultado=resultado, numero=numero, base_origen=base_origen, base_destino=base_destino)
        except ValueError as e:
            return render_template('cambio_base.html', error=str(e))
    return render_template('cambio_base.html')



# Ruta para el formulario de sistemas no lineales
@app.route('/sistemas_no_lineales', methods=['GET', 'POST'])
def sistemas_no_lineales():
    if request.method == 'POST':
        # Obtener las ecuaciones y las variables del formulario
        ecuaciones = request.form.getlist('ecuaciones')
        variables = request.form.get('variables').split(',')

        # Resolver el sistema
        solucion = resolver_sistemas_no_lineales(ecuaciones, variables)

        # Mostrar el resultado
        return render_template('sistemas_no_lineales.html', solucion=solucion, ecuaciones=ecuaciones, variables=variables)

    # Enviar formulario vacío al cargar la página inicialmente
    return render_template('sistemas_no_lineales.html')


#Ruta para el boton de limpar
@app.route('/limpiar', methods=['POST'])
def limpiar():
    session.clear()
    return redirect(url_for('newton'))


if __name__ == '__main__':
    app.run(debug=True)
