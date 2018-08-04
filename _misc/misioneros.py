lado_izquierdo = 0
lado_derecho = 1
balsa = 2
misioneros = 0
canibales = 1

# todos a la izquierda, y la posición de la balsa
estado_inicial = [[3, 3], [0, 0], lado_izquierdo]
# todos a la derecha, y la posición de la balsa
estado_final = [[0, 0], [3, 3], lado_derecho]

# viajes posibles (misionero, caníbal)
opciones_viajes = [[1, 0], [0, 1], [1, 1], [2, 0], [0, 2]]

viajes = []
camino = []
estado = estado_inicial
posibles = opciones_viajes.copy()


# devuelve si un estado es válido o no
def es_estado_valido(estado):
    # que no hayan de más o de menos
    if estado[lado_izquierdo][misioneros] > 3 or estado[lado_izquierdo][misioneros] < 0 or estado[lado_derecho][misioneros] > 3 or estado[lado_derecho][misioneros] < 0 or estado[lado_izquierdo][canibales] > 3 or estado[lado_izquierdo][canibales] < 0 or estado[lado_derecho][canibales] > 3 or estado[lado_derecho][canibales] < 0:
        return False
    # que no haya mas canibales que misioneros del lado izquierdo
    elif estado[lado_izquierdo][misioneros] != 0 and estado[lado_izquierdo][misioneros] < estado[lado_izquierdo][canibales]:
        return False
        # que no haya mas canibales que misioneros del lado derecho
    elif estado[lado_derecho][misioneros] != 0 and estado[lado_derecho][misioneros] < estado[lado_derecho][canibales]:
        return False
    return True


# cambia el estado (la posición) de la balsa según el viaje
def estado_balsa(estado, viaje):
    estado[estado[balsa]][misioneros] -= viaje[misioneros]
    estado[estado[balsa]][canibales] -= viaje[canibales]

    if estado[balsa] == lado_izquierdo:
        estado[balsa] = lado_derecho
    else:
        estado[balsa] = lado_izquierdo

    estado[estado[balsa]][misioneros] += viaje[misioneros]
    estado[estado[balsa]][canibales] += viaje[canibales]


def mostrar_estado(estado):
    b = ''
    if estado[balsa] == 0:
        b = "--w__--"
    elif estado[balsa] == 1:
        b = "--__w--"
    else:
        b = "--_e_--"  # este no deberia pasar nunca, pero por si si, la e es de error xD
    print(estado[lado_izquierdo][misioneros], estado[lado_izquierdo][canibales], b, estado[lado_derecho][misioneros], estado[lado_derecho][canibales])


# mientras el estado actual no sea igual al estado final (o sea, que no se haya llegado al estado objetivo)
while estado != estado_final:
    if len(posibles) == 0:
        exit(1)

    # probamos viajes hasta que se nos acaben los viajes posibles o uno sea válido
    while posibles:
        viaje = posibles.pop(0)

        posible_estado = [estado[lado_izquierdo].copy(), estado[lado_derecho].copy(), estado[balsa]]
        estado_balsa(posible_estado, viaje)

        # salimos del bucle si el estado es válido y no existe ya en el camino
        if es_estado_valido(posible_estado) and posible_estado not in camino:
            break

        # si todo lo anterior falla, entonces el estado no era bueno
        posible_estado = None


    if posible_estado:
        # registramos del estado actual
        camino.append(estado)
        viajes.append(posibles)

        # el viaje parece bueno
        estado = posible_estado
        posibles = opciones_viajes.copy()
    else:
        # el viaje no dio resultado satisfactorio, recuperamos el estado anterior, quitando del camino el ultimo estado,
        # que no funcionó
        estado = camino.pop()
        posibles = viajes.pop()
        posible_estado = None



print(camino)

while True:
    try:
        res = camino.pop(0)
    except:
        break
    mostrar_estado(res)
mostrar_estado(estado)





