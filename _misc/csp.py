
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



###

# Example of kNN implemented from Scratch in Python

import csv
import random
import math
import operator


def loadDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def main():
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset('iris.data', split, trainingSet, testSet)
    print
    'Train set: ' + repr(len(trainingSet))
    print
    'Test set: ' + repr(len(testSet))
    # generate predictions
    predictions = []
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')


main()


def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors





class ArbolSanidad(models.Model):
    especie = models.ForeignKey(EspecieArbol, on_delete=models.PROTECT, null=True, blank=True)
    esalud = models.CharField(max_length=10, choices=(('', 'Sin Especificar'), ('malo', 'Malo'), ('regular', 'Regular'), ('bueno', 'Bueno')), null=True, blank=True)
    forma_vida = models.CharField(max_length=10, choices=(('', 'Sin Especificar'), ('B', 'Árbol'), ('A', 'Arbusto'), ('M', 'Mixto')), null=True, blank=True)
    forma_copa = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('conica', 'Cónica'), ('columnar', 'Columnar'), ('esferica', 'Esférica'), ('fusiforme', 'Fusiforme'), ('irregular', 'Irregular'), ('paliforme', 'Paliforme'), ('parasol', 'Parasol'), ('piramidal', 'Piramidal'), ('poda', 'Podado')), null=True, blank=True)
    angulo_fuste = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('recto', 'Recto (76º-90º)'), ('inclinado', 'Inclinado (66º-75º)'), ('muy_inclinado', 'Muy inclinado (0º-65º)')), null=True, blank=True)
    tipo_fuste = models.CharField(max_length=10, choices=(('', 'Sin Especificar'), ('M', 'Monopódico (cuando poseen un tallo)'), ('S', 'Simpódico (De más de un tallo)')), null=True, blank=True)
    conflicto_redes_aereas = models.CharField(max_length=20, null=True, blank=True, db_column='conredae')
    conflicto_redes_superficiales = models.CharField(max_length=30, null=True, blank=True, db_column='conredsup')
    condicion_cepa = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('adecuada', 'Cepa Adecuada (> 50% de la copa)'), ('reducida', 'Cepa Reducida (< 50% de la copa)')), null=True, blank=True)
    infiltracion_cepa = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('adecuado', 'Espacio Adecuado de Infiltración (cepa > 50% de la copa)'), ('poca', 'Poca Infiltración (cepa <49% copa)'), ('sin', 'Sin Infiltración (Cepa cubierta con mampostería)')), null=True, blank=True)
    radiacion = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('adecuada', 'Radiación Adecuada (sin interferencia importante de sombreado)'), ('intermedia', 'Radiación Intermedia'), ('poca_construcciones', 'Poca Radicación por Construcciones (sombreado de edificios)'), ('poca_plantas', 'Poca Radicación por Plantas (sombreado de otras plantas por sobrepoblación o cercanía)')), null=True, blank=True)
    manejo_copa = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('adecuado', 'Manejo de Podas Adecuadas'), ('severo', 'Poda Severa (>50% del follaje)'), ('letal', 'Poda Letal (>80%)')), null=True, blank=True)
    resultado_podas = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('ornamental', 'Poda Ornamental'), ('aclareo', 'Poda Aclareo Infraestructura'), ('desbalanceada', 'Poda Con Copa Desbalanceada')), null=True, blank=True)
    municipio = models.CharField(max_length=200, null=True, blank=True)
    c_esta_vivo = models.NullBooleanField(default=False)
    c_forma_vida = models.CharField(max_length=10, choices=(('', 'Sin Especificar'), ('B', 'Árbol'), ('A', 'Arbusto'), ('M', 'Mixto')), null=True, blank=True)
    c_angulo_fuste = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('recto', 'Recto (76º-90º)'), ('inclinado', 'Inclinado (66º-75º)'), ('muy_inclinado', 'Muy inclinado (0º-65º)')), null=True, blank=True)
    c_altura = models.IntegerField(null=True, blank=True)
    c_densidad_follaje = models.IntegerField(choices=(('', 'Sin Especificar'), (0, 'Nulo'), (1, 'Bajo'), (2, 'Medio'), (3, 'Denso')), null=True, blank=True)
    c_cobertura_follaje = models.IntegerField(null=True, blank=True)
    c_espesor_follaje = models.IntegerField(null=True, blank=True)
    c_diametro_basal = models.IntegerField(null=True, blank=True)
    c_diametro_altura_pecho = models.IntegerField(null=True, blank=True)
    c_tipo_fuste = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Monopódico'), (2, 'Simpódico')), null=True, blank=True)
    c_forma_copa = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('conica', 'Cónica'), ('columnar', 'Columnar'), ('esferica', 'Esférica'), ('fusiforme', 'Fusiforme'), ('irregular', 'Irregular'), ('palmiforme', 'Palmiforme'), ('parasol', 'Parasol'), ('piramidal', 'Piramidal'), ('poda', 'Podado')), null=True, blank=True)
    c_conflicto_redes_aereas = models.CharField(max_length=20, choices=(('', 'Sin Especificar'), ('no', 'No'), ('cableado', 'Cableado'), ('senaleticas', 'Señaleticas'), ('alumbrado', 'Alumbrado'), ('potencial', 'Conflicto Potencial')), null=True, blank=True)
    c_conflicto_redes_superficiales = models.CharField(max_length=30, choices=(('', 'Sin Especificar'), ('no', 'No'), ('banqueta', 'Banqueta'), ('cinta_asfaltica', 'Cinta Asfáltica'), ('visibilidad_peatonal', 'Visibilidad Peatonal'), ('visibilidad_automovilistas', 'Visibilidad Automovilistas'), ('cerca', 'Cerca'), ('muro', 'Muro de construcción'), ('potencial', 'Conflicto Potencial')), null=True, blank=True)
    c_cepa_borde = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Nada'), (2, 'Mampostería'), (3, 'Ladrillo'), (4, 'Otro')), null=True, blank=True)
    c_suelo_color = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Claro'), (2, 'Café'), (3, 'Negro')), null=True, blank=True)
    c_suelo_textura = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Arcilla'), (2, 'Limo'), (3, 'Arena')), null=True, blank=True)
    c_mh_radiacion = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Poca'), (2, 'Moderada'), (3, 'Optima')), null=True, blank=True)
    c_mh_riego = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Sin Riego'), (2, 'Eventual'), (3, 'Con riego y anegamiento'), (4, 'Otro')), null=True, blank=True)
    c_vigor = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Muerto'), (2, 'Muy Pobre'), (3, 'Pobre'), (4, 'Bueno'), (5, 'Máximo')), null=True, blank=True)
    c_riesgo = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Copa Desbalanceada'), (2, 'Interferencia Ramas Bajas'), (3, 'Ramas por desgajarse'), (4, 'Riesgo de desplome'), (5, 'Fuste con inclinación de 45°'), (6, 'Pudrición o daño en estructura')), null=True, blank=True)
    c_acciones_manejo = models.IntegerField(choices=(('', 'Sin Especificar'), (1, 'Poda'), (2, 'Aclareo'), (3, 'Derribo'), (4, 'Nada')), null=True, blank=True)

    muest_fita = models.IntegerField(null=True, blank=True)
    fit_enfermo = models.NullBooleanField(default=False)
    fit_plagado = models.NullBooleanField(default=False)
    fit_dano_mecanico = models.NullBooleanField(default=False)
    fit_quemado = models.NullBooleanField(default=False)
    fit_cinchado = models.NullBooleanField(default=False)
    geom = models.PointField(srid=32613)

    def __str__(self):
        if self.especie:
            return "{} : {}".format(str(self.id), self.especie)
        else:
            return str(self.id)

    def get_absolute_url(self):
        return reverse('arbol_sanidad_detalle', kwargs={'pk': self.pk})

    def natural_key(self):
        return self.nombre



