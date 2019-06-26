import numpy as np
prestrunc = 10

casillas = {"0": "A", "1": "B", "2": "C", "3": "D", "4": "E", "5": "F"}
casflong = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}

A = np.matrix([[0.0, 1/2, 0.0, 0.0, 0.0, 1/2],
               [1/3, 0.0, 0.0, 1/3, 0.0, 1/3],
               [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
               [0.0, 1/3, 1/3, 0.0, 1/3, 0.0],
               [0.0, 0.0, 0.0, 1/2, 0.0, 1/2],
               [1/3, 1/3, 0.0, 0.0, 1/3, 0.0]])

M = np.matrix([[0 ,1, 0, 0, 0, 1],
               [1, 0, 0, 1, 0, 1],
               [0, 0, 0, 1, 0, 0],
               [0, 1, 1, 0, 1, 0],
               [0, 0, 0, 1, 0, 1],
               [1, 1, 0, 0, 1, 0],])

N = M


B = A

def mindistancia(M):
    coordenadasvalidas = [0, 1, 2, 3, 4, 5, "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"]

    origen = input("origen: ")
    destino = input("destino: ")
    if type(origen) == str:
        origen = casflong.get(origen.upper())
    if type(destino) == str:
        destino = casflong.get(destino.upper())

    if origen in coordenadasvalidas and destino in coordenadasvalidas:

        itera = 1
        while(True):
            if M[origen,destino] != 0:

                return itera, M[origen,destino]
            else:
                itera += 1
                M = M * N
        return itera, M[origen,destino]
    else:
        print("coordenadas invalidas")
        exit(-1)


def menu():
    # para SSH
    print("┌──────────────────────────┐")
    print("│                          │")
    print("│    A    │                │")
    print("│         │                │")
    print("├─────   ─┘       F        │")
    print("│                          │")
    print("│    B    │                │")
    print("│         └────────┬────   │")
    print("│                  │       │")
    print("├─────────┤                │")
    print("│             D        E   │")
    print("│    C    │        │       │")
    print("└─────────┴────────┴───────┘")
    print()


    """ # para windows (creo)
    print("┌───────────────┐")
    print("│                          │")
    print("│    A    │               │")
    print("│         │               │")
    print("├──   ─┘       F        │")
    print("│                          │")
    print("│    B    │               │")
    print("│         └────┬──   │")
    print("│                  │      │")
    print("├─────┤               │")
    print("│             D        E  │")
    print("│    C    │        │     │")
    print("└─────┴─────┴───┘")
    print() """



    print("\nSelecciona una de las opciones siguientes, digitando la letra del inciso \n")
    print("a) Cual es la probabilidad de que, dado que el raton esta en una habitacion, cambie a cada una de las otras?")
    print("b) Si empieza en la habitacion A, cual es la probabilidad de que este en cada uno de los otros cuartos en dos minutos?")
    print("c) Cual es el cuarto que el raton pasara menos tiempo?")
    print("d) Dados dos cuartos del laberinto, cual es la longitud del viaje mas corto entre ellos?")
    print("e) Dados dos cuartos del laberinto, cuantos caminos con longitud minima hay entre ellos?")
    print("x) salir")
    print()


menu()

op = str(input("   Digita la opcion deseada "))



if op.lower() == 'a':
    print()
    print(A)
elif op.lower() == 'b':
    print()
    A2 = A*A
    print("Pa =", A2[0, 0], "; Pb =", A2[0, 1], "; Pc =", A2[0, 2], "; Pd =", A2[0, 3], "; Pe =", A2[0, 4], "; Pf =", A2[0, 5])
elif op.lower() == 'c':
    print()
    l = []
    prestrunc = input("precisión decimal (digitos decimales, más de 14 itera infinitas veces, menos de 4 es impreciso):")
    try:
        prestrunc = int(prestrunc)
    except:
        print("Error, el valor no es numerico")
        exit(-1)
    if type(prestrunc) is not int or prestrunc > 15 or prestrunc < 4:
        print("valor no aceptado")
        exit(-1)
    iteraciones = 1
    contigualdad = len(casillas)
    while(contigualdad != 1):
        iteraciones += 1
        A = A * B
        C = A.transpose()
        for i in C:
            contigualdad = len(casillas)
            for j in range(len(casillas)-1):
                if np.round(i[0, j], prestrunc, None) == np.round(i[0, j+1], prestrunc, None):
                    contigualdad -= 1
            if contigualdad == 1:
                break

    sumcols = sum(A)

    for i in range(len(casillas)):
        l.append(sumcols[0, i])
        cas = min(l)

    print("\n\nLa matriz se estabiliza a partir del tiempo", iteraciones, "con una precisión de truncamiento de", prestrunc, "digitos decimales")
    print("El cuarto en el que el raton pasara menos tiempo es:", casillas[str(l.index(cas))], "\n")
    print(A.round(prestrunc))

elif op.lower() == 'd':
    dist = mindistancia(M)


    print("la longitud del viaje mas corto es de", dist[0], "pasos")

elif op.lower() == 'e':
    dist = mindistancia(M)
    print("la cantidad de caminos con longitud minima de ", dist[0], "pasos; y es de", dist[1], "caminos")

elif op.lower() == 'x':
    exit(0)

else:
    menu()
    op = str(input("   Digita la opcion deseada "))