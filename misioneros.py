lado_izquierdo = 0
lado_derecho = 1
balsa = 2
misioneros = 0
canibales = 1

# en el estado inicial todos están del lado izquierdo y nadie del lado derecho, y la canoa está del lado izquierdo
estado_inicial = [[3, 3], [0, 0], lado_izquierdo]

# en el estado objetivo todos están del lado derecho y nadie del lado izquierdo, y la canoa está del lado derecho
estado_objetivo = [[0, 0], [3, 3], lado_derecho]

# consideramos los viajes posibles en una lista de estados, donde cada estado es una lista y donde el orden importa,
# siendo cada sublista una posibilidad de la canoa, con el elemento [0] el misionero, y el elemento [1] el canibal
viajes = [[1, 0], [0, 1], [1, 1], [2, 0], [0, 2]]

def es_estado_valido(estado):
    # invalido si hay de más o de menos
    if estado[lado_izquierdo][misioneros] > 3 or estado[lado_izquierdo][misioneros] < 0 or estado[lado_derecho][misioneros] > 3 or estado[lado_derecho][misioneros] < 0 or estado[lado_izquierdo][canibales] > 3 or estado[lado_izquierdo][canibales] < 0 or estado[lado_derecho][canibales] > 3 or estado[lado_derecho][canibales] < 0:
        return False
    # Que no haya mas canibales que misioneros del lado izquierdo
    elif estado[lado_izquierdo][misioneros] != 0 and estado[lado_izquierdo][misioneros] < estado[lado_izquierdo][canibales]:
        return False
    # Que no haya mas canibales que misioneros del lado derecho
    elif estado[lado_derecho][misioneros] != 0 and estado[lado_derecho][misioneros] < estado[lado_derecho][canibales]:
        return False

    # si no se cumple ninguno de los anteriores, entonces el estado es valido
    else:
        return True


def canoa(estado, viaje):
    estado[estado[balsa]][misioneros] = estado[estado[balsa]][misioneros] - viaje[misioneros]
    estado[estado[balsa]][canibales] = estado[estado[balsa]][canibales] - viaje[canibales]

    if estado[balsa] == lado_izquierdo:
        estado[balsa] = lado_derecho
    else:
        estado[balsa] = lado_izquierdo

    estado[estado[balsa]][misioneros] = estado[estado[balsa]][misioneros] + viaje[misioneros]
    estado[estado[balsa]][canibales] = estado[estado[balsa]][canibales] + viaje[canibales]


def imprimir_estado(estado):
    espacio = "-----------"
    print("Misioneros:{}, Canibales:{} {} Misioneros:{}, Canibales:{}").format(estado[lado_izquierdo][misioneros], estado[lado_izquierdo][canibales], espacio, estado[lado_derecho][misioneros], estado[lado_derecho][canibales])


viajes = []
anterior = []


# empezar con estado inicial:
estado = estado_inicial.copy()
posibles = viajes.copy()


while estado != estado_objetivo:
    if posibles == nil:
		STDOUT.puts "NO he encontrado solucion!"
		exit
	end

	# probamos viajes hasta que se nos acaben o uno sea válido
	while ! posibles.empty?
		viaje = posibles.shift

		# duplicamos los vectores internos
		posibleEstado =  [ estado[Izq].dup, estado[Der].dup,
			estado[Canoa] ]
		canoa(posibleEstado, viaje)

		# salimos si es válido y no se ha repetido
		break if valido?(posibleEstado) &&
			anterior.index(posibleEstado) == nil

		# no es válido
		posibleEstado = nil
	end

	# tenemos uno válido?
	if posibleEstado != nil
		# nos acordamos del estado actual
		anterior.push estado
		viajes.push posibles

		# aceptamos el viaje como bueno (por ahora)
		estado = posibleEstado
		posibles = Viajes.dup
	else
		# el viaje no nos ha llevado a un resultado
		# asi que recuperamos el estado anterior
		estado = anterior.pop
		posibles = viajes.pop

		posibleEstado = nil
	end
end
