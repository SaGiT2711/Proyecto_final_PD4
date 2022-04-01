import csv
from passlib.hash import sha256_crypt
from Levenshtein import distance

class Pelicula():
    def __init__(self,id,titulo,link_foto,fecha_estreno,descripcion):
        self.id = id
        self.titulo = titulo
        self.link_foto = link_foto
        self.fecha_estreno = fecha_estreno
        self.descripcion   = descripcion
    def __str__(self):
        return f'{self.titulo} - {self.fecha_estreno}'

def lee_archivo_csv(archivo:str)->list:
    '''Lee un archivo CSV y regresa una lista de registros
    '''
    lista = []
    try:
        with open(archivo,'r',encoding='utf-8') as fh:
            csv_reader = csv.reader(fh)
            for renglon in csv_reader:
                lista.append(renglon)
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return lista

def lee_diccionario_csv(archivo:str)->list:
    '''Lee un archivo CSV y regresa un diccionario de diccionarios
    '''
    diccionario = {}
    try:
        with open(archivo,'r',encoding='utf-8') as fh:
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon['usuario']
                diccionario[llave]=renglon
    except IOError:
        print(f"No se pudo leer el archivo {archivo}")
    return diccionario

def crea_diccionario_peliculas(lista:list) -> dict:
    ''' Cicla la lista de peliculas para crear objetos Pelicula y agregarlos
        al diccionario de peliculas. Regresa un diccionario de películas
    '''
    diccionario_peliculas = {}
    for pelicula in lista:
        id = pelicula[0]
        titulo = pelicula[1]
        link = pelicula[2]
        fecha = pelicula[3]
        trama = pelicula[4]
        movie = Pelicula(id,titulo,link,fecha,trama)
        if id not in diccionario_peliculas:
            diccionario_peliculas[id] = movie
    return diccionario_peliculas

def lee_diccionario_peliculas(archivo_csv:str)->dict:
    ''' Lee un archivo CSV y regresa un diccionario de peliculas
    '''
    diccionario = {}
    try:
        with open(archivo_csv,"r",encoding="utf-8") as fh:
            csvreader = csv.DictReader(fh)
            for renglon in csvreader:
                llave = renglon['id']
                diccionario[llave] = renglon
    except IOError:
        print("Error al leer archivo")
        print(IOError.filename)
    return diccionario

def crea_diccionario_generos(diccionario_peliculas:dict)->dict:
    diccionario_genero = {}
    for id,pelicula in diccionario_peliculas.items():
        genero = pelicula['genero']
        if genero not in diccionario_genero:
            diccionario_genero[genero] = [pelicula]
        else:
            diccionario_genero[genero].append(pelicula)
    return diccionario_genero

def crea_diccionario_usuarios(diccionario_peliculas:dict)->dict:
    diccionario_usuario = {}
    for id,pelicula in diccionario_peliculas.items():
        usuario = pelicula['usuario']
        if genero not in diccionario_usuario:
            diccionario_usuario[usuario] = [pelicula]
        else:
            diccionario_usuario[usuario].append(pelicula)
    return diccionario_usuario

def crea_diccionario(diccionario_peliculas:dict,llave_ext:str)->dict:
    diccionario = {}
    for id,pelicula in diccionario_peliculas.items():
        llave = pelicula[llave_ext]
        if llave not in diccionario:
            diccionario[llave] = [pelicula]
        else:
            diccionario[llave].append(pelicula)
    return diccionario


def crea_diccionario_x_anio(diccionario_peliculas:dict)->dict:
    diccionario_anio = {}
    for id, pelicula in diccionario_peliculas.items():
        fecha = pelicula['fecha_estreno'].split("/") # 5/5/2022 -> 0/1/2
        anio  = fecha[2]
        if anio not in diccionario_anio:
            diccionario_anio[anio] = [pelicula]
        else:
            diccionario_anio[anio].append(pelicula)
    return diccionario_anio

def graba_diccionario(diccionario:dict,llave_dict:str,archivo:str):
    with open(archivo,'w') as fh: #fh = file handle
        lista_campos = obten_campos(diccionario, llave_dict)
        dw = csv.DictWriter(fh,lista_campos)
        dw.writeheader()
        renglones = []
        for llave, valor_d in diccionario.items():
            d = { 'usuario':llave}
            for key, value  in valor_d.items():
                d[key] = value
            renglones.append(d)
        dw.writerows(renglones)

def obten_campos(diccionario:dict,llave_d:str)->list:
    lista = [llave_d]
    llaves = list(diccionario.keys())
    k = llaves[0]
    nuevo_diccionario = diccionario[k]
    lista_campos = list(nuevo_diccionario.keys())
    lista.extend(lista_campos)
    return lista

def limpia_texto(texto:str)->str:
    lista_simbolos = [',',';','.','-','_',':','¿','?','¡','!']
    for simbolo in lista_simbolos:
        texto = texto.replace(simbolo,'')
    return texto
        
def agrega_palabras(diccionario:dict, cadena:str, diccionario_pelicula):
    minusculas = cadena.lower()
    cadena_limpia = limpia_texto(minusculas)
    palabras = cadena_limpia.split(" ")
    for palabra in palabras:
        if palabra not in diccionario:
            diccionario[palabra] = [ diccionario_pelicula ]
        else:
            diccionario[palabra].append(diccionario_pelicula)


def crea_superdiccionario(diccionario_peliculas:dict)->dict:
    diccionario_palabras = {}
    for id,pelicula in diccionario_peliculas.items():
        titulo = pelicula['titulo']
        sinopsis=pelicula['sinopsis']
        agrega_palabras(diccionario_palabras,titulo,pelicula)
        agrega_palabras(diccionario_palabras,sinopsis,pelicula)
    return diccionario_palabras

def compara_distancia(diccionario:dict,frase:str)->dict:
    diccionario_resultados = {}
    lista_tuplas = []
    for llave, lista in diccionario.items():
        L = distance(frase, llave) 
        tupla = (llave, L)
        lista_tuplas.append(tupla)
    #ordenar lista
    sorted_t = sorted(lista_tuplas, key=lambda tup:tup[1])
    # [ ("memory",15),("memory",2),("memory",3)]
    for t in sorted_t[0:6]:
        llave = t[0]
        distancia = t[1]
        peliculas = diccionario[llave] #lista peliculas asociadas con la llave
        for pelicula in peliculas: #extraemos peliculas de la lista
            id = pelicula['id']
            pelicula['distancia'] = distancia #agregamos distancia de la frase original
            pelicula['frase'] = llave #agregamos la frase con la que la encontramos
            diccionario_resultados[id] = pelicula
    return diccionario_resultados


if __name__ == "__main__":
    #listado = lee_archivo_csv("lista_estrenos.csv")
    #for pelicula in listado:
    #    print(pelicula[1])
    #diccionario = crea_diccionario_peliculas(listado)
    diccionario = lee_diccionario_peliculas("cartelera_estrenos.csv")
    generos = crea_diccionario_generos(diccionario)
    diccionario_anio = crea_diccionario_x_anio(diccionario)
    for genero,pelis in generos.items():
        print(genero)

    #print(diccionario['Taken']['sinopsis'])

    #print(diccionario_anio['2001'])
    #diccionario_usuarios = {'bob': { 'nombre':'Bob Esponja',
    #                             'edad'  : '20',
    #                             'genero': 'Comedia'
    #                            }
    #                    }
    #lista = obten_campos(diccionario_usuarios,'usuario')
    #print(lista)
    #graba_diccionario(diccionario_usuarios,'usuario','usuarios.csv')
    texto_plano= 'Batman'
    texto_cript= sha256_crypt.hash(texto_plano)
    print(f'{texto_plano} es {texto_cript}')
    
