

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







# De importan las bibliotecas shapefile y BeautifulSoup, para generar archivos shapefile
# y leer documentos SGML respectivamente.
import shapefile
from bs4 import BeautifulSoup


doc = open('doc.kml')  # leer el archivo .kml y guardar su contenido en la variable doc
soup = BeautifulSoup(doc, "html.parser")  # leer mediante BeautifulSoup el archivo contenido en doc, como html
places = soup.find_all('placemark')

w = shapefile.Writer(shapefile.POINT)
# w.autoBalance = 1
w.field('ident', 'C', 100)
w.field('dap', 'F', 10, 8)
w.field('dbas', 'F', 10, 8)
w.field('cob', 'F', 10, 8)
w.field('alt', 'F', 10, 8)
w.field('copa', 'N')
w.field('densidad', 'N')
w.field('ffuste', 'N')
w.field('ifuste', 'N')
w.field('esalud', 'N')
w.field('ired', 'N')
w.field('dinf', 'N')

for i in range(len(places)):
    try:
        ident = places[i].ident.get_text().replace('\n', '')
    except:
        ident = ''

    try:
        dap = float(places[i].dap.get_text().replace('\n', ''))
    except:
        dap = 0.0

    try:
        dbas = float(places[i].dbas.get_text().replace('\n', ''))
    except:
        dbas = 0.0

    try:
        cob = float(places[i].cob.get_text().replace('\n', ''))
    except:
        cob = 0.0

    try:
        alt = float(places[i].alt.get_text().replace('\n', ''))
    except:
        alt = 0.0

    try:
        copa = int(places[i].copa.get_text().replace('\n', ''))
    except:
        copa = 0

    try:
        densidad = int(places[i].densidad.get_text().replace('\n', ''))
    except:
        densidad = 0

    try:
        ffuste = int(places[i].ffuste.get_text().replace('\n', ''))
    except:
        ffuste = 0

    try:
        ifuste = int(places[i].ifuste.get_text().replace('\n', ''))
    except:
        ifuste = 0

    try:
        esalud = int(places[i].esalud.get_text().replace('\n', ''))
    except:
        esalud = 0

    try:
        ired = int(places[i].ired.get_text().replace('\n', ''))
    except:
        ired = 0

    try:
        dinf = int(places[i].dinf.get_text().replace('\n', ''))
    except:
        dinf = 0

    try:
        coord = places[i].coordinates.get_text().split(',')
        coord[0] = float(coord[0])
        coord[1] = float(coord[1])
    except:
        coord = [0, 0]

    print(coord[0], coord[1])
    w.point(coord[0], coord[1])
    print(ident, dap, dbas, cob, alt, copa, densidad, ffuste, ifuste, esalud, ired, dinf)
    w.record(ident, dap, dbas, cob, alt, copa, densidad, ffuste, ifuste, esalud, ired, dinf)

w.save("arboles.shp")

