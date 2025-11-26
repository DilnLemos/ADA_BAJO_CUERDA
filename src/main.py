import sys 
import os 
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import filechooser as fc

modified_route = None

def leer_finca(route):
    ruta = route
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]
    n = int(lineas[0])
    finca = [tuple(map(int, l.split(','))) for l in lineas[1:n+1]]
    
    return finca
def exit():
    print("Adios")
    return False

def main(r='finca.txt', n=None):
    global modified_route
    route = modified_route if (modified_route != None) else r
    route = os.path.abspath(modified_route) if modified_route != None else os.path.abspath(r)
    if n == None:
        print("          Riego Optimo")
        text = ["Soluciones implementada con programacion lineal utilizando el solver minizinc", "1 - Ejecutar Solucion", " 2 - Especificar archivo (si no se hace toma uno por defecto)", "SALIR : digite SALIR"]
        for t in text:
            print(f"\n{t}")
        opt = " "
        while type(opt) != int or opt == 0 or opt > 2 :
            
            try: 
                opt = input("\nDigite el numero de su eleccion  y presione ENTER:")
                if opt == "SALIR":
                    return False
                opt = int(opt)

            except ValueError:
                print("Eleccion no disponible 🙄")
            
            except TypeError:
                print("Eleccion no disponible 🙄")
            
            if type(opt) != int:
                print("Eleccion no disponible 🙄")
            
            elif opt == 2:
                modified_route = fc.select_file()
                print(f"source : {modified_route}")
            elif opt > 2:
                print("No tenemos tantas opciones")
                opt = 0
        
    else: 
        opt = n
        
    if opt == 1:
        print(f" === RESOLVIENDO {os.path.basename(route)} ===")
        finca = leer_finca(route)
        print(f"source : {route}")
        tiempo_i = time.time()
        mejor_permutacion, mejor_costo = "esta vaina no esta lista", "esto tampoco"
        tiempo_f = time.time()

        print("=======================================================================")
        print("RESULTADO ÓPTIMO")
        print("=======================================================================")
        print("Tiempo de ejecución:", tiempo_f - tiempo_i)
        
        print(mejor_costo)
        '''
        for idx in mejor_permutacion:
            print(idx)
            '''
        input("Enter para continuar")


if __name__ == "__main__":
    
    while True:
        running = main()
        if running == False:
            break
    
