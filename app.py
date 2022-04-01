from flask import Flask, redirect, render_template, request, session
from funciones import compara_distancia, crea_diccionario, crea_superdiccionario, graba_diccionario, lee_diccionario_csv, lee_diccionario_peliculas, crea_diccionario_peliculas, crea_diccionario_generos, crea_diccionario_x_anio
from passlib.hash import sha256_crypt
import os

app = Flask(__name__)

@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)