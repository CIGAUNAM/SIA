
especies = EspecieArbol.objects.all().annotate(num=Count('arbol'))
esp_altura = 50

for i in especies:
    esp_altura = 50
    arboles = Arbol.objects.filter(especie__id=i.id, altura__gte=0)
    min_altura = None
    max_altura = None

    if arboles.count() > 0:
        min_altura = int(arboles.order_by('altura')[0].altura)
        max_altura = int(arboles.order_by('-altura')[0].altura)

    alturas = {}
    if (min_altura and max_altura):
        if min_altura == max_altura:
            max_altura += 1
        for j in range(min_altura - min_altura%esp_altura + 1 - esp_altura, max_altura, esp_altura):
            # print(j, j+esp_altura)
            q = Arbol.objects.filter(especie__id=i.id).filter(Q(altura__gte=j) & Q(altura__lte=j + esp_altura - 1))
            alturas[j+esp_altura - 1] = q.count()

    esp_dap = 5
    daps = {}
    arboles = Arbol.objects.filter(especie__id=i.id, diametro_altura_pecho__gte=0)
    min_dap = None
    max_dap = None

    if arboles.count() > 0:
        min_dap = int(arboles.order_by('diametro_altura_pecho')[0].diametro_altura_pecho)
        max_dap = int(arboles.order_by('-diametro_altura_pecho')[0].diametro_altura_pecho)

    if (min_dap and max_dap):
        if min_dap == max_dap:
            max_dap += 1
        for j in range(min_dap - min_dap%esp_dap + 1 - esp_dap, max_dap + esp_dap, esp_dap):

            q = Arbol.objects.filter(especie__id=i.id).filter(Q(diametro_altura_pecho__gte=j) & Q(diametro_altura_pecho__lte=j + esp_dap - 1))
            daps[j+esp_dap - 1] = q.count()

    esp_db = 5
    dbs = {}
    arboles = Arbol.objects.filter(especie__id=i.id, diametro_basal__gte=0)
    min_db = None
    max_db = None

    if arboles.count() > 0:
        min_db = int(arboles.order_by('diametro_basal')[0].diametro_basal)
        max_db = int(arboles.order_by('-diametro_basal')[0].diametro_basal)

    if (min_db and max_db):
        if min_db == max_db:
            max_dap += 1
        for j in range(min_db - min_db % esp_db + 1 - esp_db, max_db + esp_db, esp_db):
            q = Arbol.objects.filter(especie__id=i.id).filter(
                Q(diametro_altura_pecho__gte=j) & Q(diametro_altura_pecho__lte=j + esp_db - 1))
            dbs[j + esp_db - 1] = q.count()


    print("alturas", i, min_altura, max_altura)
    print(alturas)
    print("daps", i, min_dap, max_dap)
    print(daps)
    print("dbs", i, min_db, max_db)
    print(dbs)


