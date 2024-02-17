from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import re


#instala flask y panda

app = Flask(__name__)

app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

datos = pd.read_excel("Datos.xlsx")
#usuarios accedidos en login
usuarios = {
    'yahir': 'yahir',
    'Pedro': 'pedro',
    'Luis Alfaro': 'Sof'
}
#filtrar los datos de excel
def search_nombre(patron):
    datos[['Nombre', 'Correo']] = datos[['Nombre', 'Correo']].fillna('')
    coincidence = datos[datos['Nombre'].str.contains(patron, flags=re.IGNORECASE, regex=True)]
    return coincidence[['Nombre' , 'Correo']]

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
    result = search_nombre(searchnombres)
    if not result.empty:
        resultados = result.to_dict(orient='records')
        return render_template('resultado.html', resultados=resultados)
    else:
        return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)


                
   