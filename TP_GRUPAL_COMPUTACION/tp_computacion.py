#IMPORTACIONES:
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#CONSTANTES:

OPCION_VER_DENUNCIAS = 1
OPCION_EMITIR_ALERTA = 2
OPCION_VER_FOTOGRAFIA = 3
OPCION_VER_GRAFICO = 4
OPCION_SALIR = 5

INDICE_TIMESTAMP = 0
INDICE_PATENTE = 1
INDICE_TEL = 2
INDICE_DIRECCION = 3
INDICE_NRO = 4
INDICE_BARRIO = 5
INDICE_RUTA_FOTO = 6
INDICE_DESCRIPCION = 7

INDICE_MES = 1

NOMBRE_ARCHIVO_CSV = "C:/Users/User/Desktop/Python/TP_GRUPAL_COMPUTACION/reclamos.csv"
NOMBRE_ARCHIVO_TXT = "c:/Users/User/Desktop/TP_GRUPAL_COMPUTACION/robados.txt"

#FUNCIONES:
def borrar():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")

def pedir_opcion(menu):
  print(menu)
  opciones_validas = ["1","2","3","4","5"]
  opcion = input("Ingrese una opción del menú: ")
  while not opcion in opciones_validas:
    borrar()
    print(menu)
    opcion = input("Ingrese una opción válida: ")
  borrar()

  return int(opcion)


def leer_csv():
  try: 
    with open(NOMBRE_ARCHIVO_CSV, newline = '') as mi_archivo_csv:
        informacion = csv.reader(mi_archivo_csv, delimiter = ',') 
        datos_salida = list()    
        next(informacion) #Evitamos leer el header
        for fila in informacion:
          datos_salida.append(fila)
        if len(datos_salida[0]) == 1: #Si no se delimita por comas toda la linea se pasa como un solo elemento.
          raise IndexError 
        
    return datos_salida
  
  #Si no existe el archivo tomamos el error y damos aviso.
  except FileNotFoundError:
    print("No se pudo abrir el archivo, pruebe con otro nombre")
    print("Pulse 5")

  #Corroboramos que el archivo.csv venga delimitado por comas.
  except IndexError:
    print("El archivo no esta delimitado por comas")
    print("Pulse 5")
        
  

def leer_txt():
  
  try:
    with open (NOMBRE_ARCHIVO_TXT,'r') as mi_archivo_txt:
      informacion = mi_archivo_txt.readlines()
      informacion_limpia = list()
      for linea in informacion:
        informacion_limpia.append(linea.rstrip('\n')) #Sacamos los \n al final de cada linea.

    
    
  #Si no existe el archivo tomamos el error y damos aviso.
  except FileNotFoundError:
    print("No se pudo abrir el archivo, pruebe con otro nombre")
  
  return informacion_limpia


def listar_denuncias(lectura):
  lista_denuncias = list()

  calle = input("Ingrese la calle donde ocurieron las denuncias: ") 
  
  direccion_referencia = lectura[0][INDICE_DIRECCION]
  
  #Hacemos que el string de entrada tenga la misma estructura de mayusculas que el csv.
  if direccion_referencia.islower() == True:
    calle = calle.lower()
  elif direccion_referencia.isupper() == True:
    calle = calle.upper()
  elif direccion_referencia.isupper() == False and direccion_referencia.islower() == False:
    calle = calle.title()

  tramo_valido = False
  
  while tramo_valido == False:
    try:

      tramo = input("Ingrese el tramo separado por '-': ")
      tramo = tramo.split("-")
      tramo = [int(tramo[0]), int(tramo[1])]
      tramo_valido = True
    
    except IndexError:
      print("Tramo vacío")
      
    except ValueError:
      print("Tramo inválido. Falta un valor")
      
  #Esto es para validar que se pongan en orden ascendente las alturas.
  while tramo[0] > tramo[1]:
    print("Tramo inválido. Recuerde ingresar el tramo en orden ascendente")
    tramo = input("Ingrese el tramo separado por '-': ")
    tramo = tramo.split("-")
    tramo = [int(tramo[0]), int(tramo[1])]

  #Comparamos si las denuncias registradas cumplen las condiciones pedidas.
  for denuncia in lectura:
    if calle in denuncia[INDICE_DIRECCION] and int(denuncia[INDICE_NRO]) >= tramo[0] and int(denuncia[INDICE_NRO])<= tramo[1]:
        lista_denuncias.append(denuncia)
  
  print("LAS DENUNCIAS RECIBIDAS EN DICHO TRAMO SON: ")
  if len(lista_denuncias) != 0:
    for denuncia in lista_denuncias:
      print(f"""· PATENTE: {denuncia[INDICE_PATENTE]}
                · TIMESTAMP: {denuncia[INDICE_TIMESTAMP]}
                · TELEFONO: {denuncia[INDICE_TEL]}
                · DIRECCION: {denuncia[INDICE_DIRECCION]} {denuncia[INDICE_NRO]}, {denuncia[INDICE_BARRIO]}
                · DESCRIPCION : {denuncia[INDICE_DESCRIPCION]}
            """)

  else:
    print("No se han registrado denuncias en la dirección indicada")

def emitir_alerta(lectura_csv,lectura_robados):
  lista_coincidencias = list()
  for denuncia in lectura_csv:
    if denuncia[INDICE_PATENTE] in lectura_robados:
      lista_coincidencias.append(denuncia[INDICE_PATENTE])
  
  if len(lista_coincidencias) == 0:
    print("No se han registrado autos sospechosos")

  else:
    if len(lista_coincidencias) > 1:
      print(""" 
    ALERTA!!!
    Se han registrado autos sospechosos!
    """)
    
    elif len(lista_coincidencias) == 1:
      print(f"""
    ALERTA!!!
    Se ha registrado un auto sospechoso """)
    
    for patente in lista_coincidencias:
      indice_patente = lista_coincidencias.index(patente)
      print(f""" 
      Patente: {patente}
      Ubicación: {lectura_csv[indice_patente][INDICE_DIRECCION]} {lectura_csv[indice_patente][INDICE_NRO]}, {lectura_csv[indice_patente][INDICE_BARRIO]}
      Fecha: {lectura_csv[indice_patente][INDICE_TIMESTAMP]}
      Infracción: {lectura_csv[indice_patente][INDICE_DESCRIPCION]}
      ------------
      """)  


def ver_fotografia(lectura):
  patente_ingresada = input("Por favor ingrese una patente: ")
  lista_patentes = list()
  for denuncia in lectura:
    lista_patentes.append(denuncia[INDICE_PATENTE])
  if patente_ingresada in lista_patentes:
    indice_patente = lista_patentes.index(patente_ingresada)
    print("Buscando fotografía...")
    try:
      titulo = lectura[indice_patente][INDICE_DIRECCION] + " " + lectura[indice_patente][INDICE_NRO] + ", " + lectura[indice_patente][INDICE_BARRIO] 
      print(f"""
{titulo.upper()}
-------------------------
      """)
      foto = mpimg.imread(lectura[indice_patente][INDICE_RUTA_FOTO])
      fotoplot = plt.imshow(foto)
      plt.show()
      print(f"Descripcion: {lectura[indice_patente][INDICE_DESCRIPCION]}")

    except IOError:
      print("No se encontraron fotografías para la patente ingresada")

  else:
    print("La patente ingresada no tiene denuncias registradas")

def sumar_a_mes(lectura,meses):
  lista_timestamps = list()
  lista_separada = list()
  puntos_y = {"01":0,"02":0,"03":0,"04":0,"05":0,"06":0,"07":0,"08":0,"09":0,"10":0,"11":0,"12":0}
  for denuncia in lectura:
    lista_timestamps.append(denuncia[INDICE_TIMESTAMP])
  for timestamp in lista_timestamps:
    lista_separada.append(timestamp.split("/"))
  
  for mes in meses:
    for denuncia in lista_separada:
      if denuncia[INDICE_MES] == mes:
        puntos_y[mes]+=1
  
  return puntos_y

def ver_grafico(lectura,meses):
  lista_puntos_y = list()
  # Crear la figura y los ejes
  fig, ax = plt.subplots()
  #Para dibujar los puntos
  puntos_x = meses
  puntos_y = sumar_a_mes(lectura,meses) #Esto es un diccionario
  for mes in puntos_y:
    lista_puntos_y = puntos_y.values()
  lista_puntos_y = list(lista_puntos_y)
  # Dibujar puntos
  ax.plot(puntos_x, lista_puntos_y)

  # Guardar el gráfico en formato png
  plt.savefig('Grafico_denuncias_por_mes.png')
  # Mostrar el gráfico
  print("""
  Gráfico: DENUNCIAS POR MES
  ----------------------------
  """)
  plt.show()
                
# MAIN :

def main():
      
  borrar()
  
  print("Bienvenido al programa de denuncias de la Ciudad de Buenos Aires")
  
  meses = ["01","02","03","04","05","06","07","08","09","10","11","12"]
  
  menu = """ 
Elija una opción del menú:
1. Ver denuncias recibidas en un rango de dirección
2. Emitir alerta de auto sospechoso
3. Ver fotografía según patente
4. Ver gráfico mensual de denuncias
5. Salir
"""
  
  lectura_csv = leer_csv()

  
  entrada = pedir_opcion(menu) 

  while entrada != OPCION_SALIR:
      
    if entrada == OPCION_VER_DENUNCIAS:
        listar_denuncias(lectura_csv)
        
    elif entrada == OPCION_EMITIR_ALERTA:
        emitir_alerta(lectura_csv,leer_txt())
    
    elif entrada == OPCION_VER_FOTOGRAFIA:
      ver_fotografia(lectura_csv)
      #A veces se traba si la imagen es muy pesada

    elif entrada == OPCION_VER_GRAFICO:
      ver_grafico(lectura_csv,meses)
    
    entrada = pedir_opcion(menu)

  
  print("Programa finalizado. Gracias por utilizar la aplicación.")


if __name__ == "__main__":
  main()