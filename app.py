from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import re


#instala flask y panda

app = Flask(__name__)

app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

datos = pd.read_excel("./Datos.xlsx")
#usuarios accedidos en login
usuarios = {
    'yahir': 'yahir',
    'Pedro': 'pedro',
    'Luis Alfaro': 'Sof',
    'Chano': 'Chano@05'
}

def find(name, email):
    if name and not email:
        datos[['Nombre']] = datos[['Nombre']].fillna('')
        coincidence = datos[datos['Nombre'].str.contains(name, flags=re.IGNORECASE, regex=True)]
        return coincidence[['Nombre','Correo']]
    
    if email and not name:
        # Asegura que no haya NaNs que puedan causar errores.
        datos['Correo'] = datos['Correo'].fillna('')
        # Filtra solo la columna especifica pero retorna todos los valores de la fila
        found = datos[datos['Correo'].str.contains(email, flags=re.IGNORECASE, regex=True, na=False)]
        return found[['Nombre','Correo']]
    
    if name and email:
        datos['Correo'] = datos['Correo'].fillna('')
        found = datos[
            (datos['Nombre'].str.contains(name, flags=re.IGNORECASE, regex=True)) & 
            (datos['Correo'].str.contains(email, flags=re.IGNORECASE, regex=True, na=False))
            ]
        return found[['Nombre','Correo']]
    
#redireccionar siempre al login como ruta raiz
@app.route("/")
def redireccionar():
        return redirect(url_for('login'))

#ruta para el login
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if user in usuarios and usuarios[user] == password:
            session['logged_in'] = True
            session['username'] = user
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
            return render_template('Login.html', error=error)
    else:
        return render_template('Login.html')

#ruta para el formulario
@app.route('/Formulario')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('Formulario.html')
    else:
        return redirect(url_for('login')) 
    
#Para obtener el resultado de la lista
@app.route('/Lista', methods=['POST'])
def lista():
    searchnombres = request.form['busqueda']
    email = request.form['email']

    result = find(searchnombres, email)

    if not result.empty:
        resultados = result.to_dict(orient='records')
        return render_template('Formulario.html', resultados=resultados)
    else:
        return render_template('resultado.html', no_results=True)
    

if __name__ == '__main__':
    app.run(debug=True)