

def es_valido(grafo):
    for nodo, adiacentes in grafo.items():
        assert(nodo not in adiacentes)
        for siguiente in adiacentes:
            assert(siguiente in grafo and nodo in grafo[siguiente])

def revisar_solucion(grafo, solution):
    if solution is not None:
        for node,nexts in grafo.items():
            assert(node in solution)
            color = solution[node]
            for next in nexts:
                assert(next in solution and solution[next] != color)

def mejor_candidato(grafo, heuristicas):
    if True:
        candidatos_info = [
            (
                -len({heuristicas[vecino] for vecino in grafo[n] if vecino in heuristicas}),
            -len({vecino for vecino in grafo[n] if vecino not in heuristicas}),
            n
            ) for n in grafo if n not in heuristicas]
        # print(candidatos_info)
        candidatos_info.sort()
        candidatos = [n for _, _, n in candidatos_info]
    else:
        candidatos = [n for n in grafo if n not in heuristicas]
        candidatos.sort()
    if candidatos:
        candidato = candidatos[0]
        assert(candidato not in heuristicas)
        return candidato
    assert(set(grafo.keys()) == set(heuristicas.keys()))
    return None

contador = 0

def resolver(grafo, colores, heuristicas, profundidad):
    global contador
    contador += 1
    n = mejor_candidato(grafo, heuristicas)
    if n is None:
        return heuristicas

    for c in colores - {heuristicas[vecino] for vecino in grafo[n] if vecino in heuristicas}:
        assert(n not in heuristicas)
        assert(all((vecino not in heuristicas or heuristicas[vecino] != c) for vecino in grafo[n]))
        heuristicas[n] = c
        indentacion = '  ' * profundidad
        # print("{}Intentado color {} para {}".format(indentacion, c, n))
        if resolver(grafo, colores, heuristicas, profundidad+1):
            # print("{}Dado el color {} a {}".format(indentacion, c, n))
            return heuristicas
        else:
            del heuristicas[n]
            # print("{}No se pudo asignar el color {} a {}".format(indentacion,c,n))
    return None


def resolver_problema(grafo, colores):
    es_valido(grafo)
    solucion = resolver(grafo, colores, {}, 0)
    print(solucion)
    revisar_solucion(grafo, solucion)


WA  = 'Western Australia'
NT  = 'Northwest Territories'
SA  = 'Southern Australia'
Q   = 'Queensland'
NSW = 'New South Wales'
V   = 'Victoria'
T   = 'Tasmania'

australia = { T:   {V                },
              WA:  {NT, SA           },
              NT:  {WA, Q, SA        },
              SA:  {WA, NT, Q, NSW, V},
              Q:   {NT, SA, NSW      },
              NSW: {Q, SA, V         },
              V:   {SA, NSW, T       }
            }

colors  = {'Rojo', 'Verde', 'Azul', 'Naranja'}

resolver_problema(australia, colors)
print("\npasos para encontrar la solución:", contador)