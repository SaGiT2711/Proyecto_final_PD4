from flask import Flask, redirect, render_template, request, session
from funciones import compara_distancia, crea_diccionario, crea_superdiccionario, graba_diccionario, lee_diccionario_csv, lee_diccionario_peliculas, crea_diccionario_peliculas, crea_diccionario_generos, crea_diccionario_x_anio
from passlib.hash import sha256_crypt
import os

login = Flask(__name__)
usuarios= "archivo_usuarios.csv"
diccionario_usuarios = lee_diccionario_csv(usuarios)

@login.route('/login', methods=['GET','POST'])
@login.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        msg = ''
        return render_template('login.html',mensaje=msg)
    else:
        if request.method == 'POST':
            #print(request.form.keys())
            usuario = request.form['usuario']
            if usuario in diccionario_usuarios:
                password_db = diccionario_usuarios[usuario]['password'] # password guardado
                password_forma = request.form['password'] #password presentado
                verificado = sha256_crypt.verify(password_forma,password_db)
                if (verificado == True):
                    session['usuario'] = usuario
                    session['logged_in'] = True
                    if 'ruta' in session:
                        ruta = session['ruta']
                        session['ruta'] = None
                        return redirect(ruta)
                    else:
                        return redirect("/")
                else:
                    msg = f'El password de {usuario} no corresponde'
                    return render_template('login.html',mensaje=msg)
            else:
                msg = f'usuario {usuario} no existe'
                return render_template('login.html',mensaje=msg)