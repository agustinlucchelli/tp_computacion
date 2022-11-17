import os
import csv
import matplotlib.pyplot as plt

def leer_csv():
    
    nombre_archivo = input("ingrese el nombre del archivo csv: ")
    nombre_archivo += ".csv"
    lista = os.listdir("TP_GRUPAL_COMPUTACION")
    os.system("cls")
    
    while nombre_archivo not in lista and nombre_archivo == "tp.py.csv" :
               
        print("archivo csv inexistente, pruebe con otro nombre")
        nombre_archivo = input("ingrese el nombre del archivo csv: ")
        os.system("cls")
        
    with open(f"TP_GRUPAL_COMPUTACION/{nombre_archivo}", newline = '') as csvfile:
        
        informacion = csv.reader(csvfile, delimiter = ',', quotechar = '|') 
        
        salida = list() 
                    
        for row in informacion:
            salida.append(row)
            
        return salida
    

def listar_denuncias(lectura):
    
    calle = input("ingrese la calle donde ocurieron las denuncias: ")
    tramo = input("ingrese el tramo separado por '-': ")
    tramo = tramo.split("-")
    tramo = [int(tramo[0]), int(tramo[1])]
    lista = list()
    lista1 = list()
    
    try:
            posiciones = [lectura[i].index("Direccion"), lectura[i].index("Nro")]
    except ValueError:   
            posiciones = [lectura.index("direccion"), lectura.index("nro")]
    
    for i in range(len(lectura)):
        
        lista1.append(lectura[i][posiciones[0]])
            
        if lectura[i][posiciones[0]] == calle and int(lectura[i][posiciones[1]]) >= tramo[0] and int(lectura[i][posiciones[1]]) <= tramo[1]:
            lista.append(lectura[i])
        
    if calle not in lista1:
        os.system("cls")
        print("no hay registros con esa direccion.")
        listar_denuncias()
    else:
        os.system("cls")
        if len(lista) != 0:
            print(lectura[0])
            for i in lista:
                print(i)
        else:
            os.system("cls")
            print("no se registraron denuncias en el tramo indicado")
        
        
                
                
                
def main():
    
    os.system("cls")

    TEXTO_MENU = """
    
        para listar las denuncias recibidas en un tramo de una calle ingrese 1
        para ver la fotografia de la patente ingrese 2
        para cerrar el  programa ingrese 0
    
    """    
    
    lectura = leer_csv()
    
    print(TEXTO_MENU)
    entrada = input("ingrese una opcion: ")
    os.system("cls")

    while entrada != "0":
        
        if entrada == "1":
            listar_denuncias(lectura)
            
        elif entrada == "2":
            pass
        
        print(TEXTO_MENU)
        entrada = input("ingrese una opcion")
    
    os.system("cls")
    print("Programa finalizado")
        
        

if __name__ == '__main__':
    main()
