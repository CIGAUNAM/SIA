especies = EspecieArbol.objects.all().annotate(num=Count('arbol'))
esp_altura = 50

for i in especies:

    # altura
    esp_altura = 50
    alturas = {}
    arboles = Arbol.objects.filter(especie__id=i.id, altura__gte=0)
    min_altura = None
    max_altura = None

    if arboles.count() > 0:
        min_altura = int(arboles.order_by('altura')[0].altura)
        max_altura = int(arboles.order_by('-altura')[0].altura)

    if (min_altura and max_altura):
        if min_altura == max_altura:
            max_altura += 1
        for j in range(min_altura - min_altura%esp_altura + 1 - esp_altura, max_altura, esp_altura):
            q = Arbol.objects.filter(especie__id=i.id).filter(Q(altura__gte=j) & Q(altura__lte=j + esp_altura - 1))
            alturas[j+esp_altura - 1] = q.count()

    # dap
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

    # db
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
            max_db += 1
        for j in range(min_db - min_db % esp_db + 1 - esp_db, max_db + esp_db, esp_db):
            q = Arbol.objects.filter(especie__id=i.id).filter(
                Q(diametro_altura_pecho__gte=j) & Q(diametro_altura_pecho__lte=j + esp_db - 1))
            dbs[j + esp_db - 1] = q.count()

    # densidad
    esp_densidad = 1
    densidades = {}
    arboles = Arbol.objects.filter(especie__id=i.id, densidad__gte=0)
    min_densidad = None
    max_densidad = None

    if arboles.count() > 0:
        min_densidad = int(arboles.order_by('densidad')[0].densidad)
        max_densidad = int(arboles.order_by('-densidad')[0].densidad)

    if (min_densidad and max_densidad):
        if min_densidad == max_densidad:
            max_densidad += 1
        for j in range(min_densidad - min_densidad % esp_densidad + 1 - esp_densidad, max_densidad + esp_densidad, esp_densidad):
            q = Arbol.objects.filter(especie__id=i.id).filter(
                Q(densidad__gte=j) & Q(densidad__lte=j + esp_densidad - 1))
            densidades[j + esp_densidad - 1] = q.count()

    # cobertura
    esp_cobertura = 5
    coberturas = {}
    arboles = Arbol.objects.filter(especie__id=i.id, cobertura__gte=0)
    min_cobertura = None
    max_cobertura = None

    if arboles.count() > 0:
        min_cobertura = int(arboles.order_by('cobertura')[0].cobertura)
        max_cobertura = int(arboles.order_by('-cobertura')[0].cobertura)

    if (min_cobertura and max_cobertura):
        if min_cobertura == max_cobertura:
            max_cobertura += 1
        for j in range(min_cobertura - min_cobertura % esp_cobertura + 1 - esp_cobertura, max_cobertura + esp_cobertura,
                       esp_cobertura):
            q = Arbol.objects.filter(especie__id=i.id).filter(
                Q(cobertura__gte=j) & Q(cobertura__lte=j + esp_cobertura - 1))
            coberturas[j + esp_cobertura - 1] = q.count()


    # CAMPO

        # c_altura
        esp_c_altura = 50
        c_alturas = {}
        arboles = Arbol.objects.filter(especie__id=i.id, c_altura__gte=0)
        min_c_altura = None
        max_c_altura = None

        if arboles.count() > 0:
            min_c_altura = int(arboles.order_by('c_altura')[0].c_altura)
            max_c_altura = int(arboles.order_by('-c_altura')[0].c_altura)

        if (min_c_altura and max_c_altura):
            if min_c_altura == max_c_altura:
                max_c_altura += 1
            for j in range(min_c_altura - min_c_altura % esp_c_altura + 1 - esp_c_altura, max_c_altura, esp_c_altura):
                q = Arbol.objects.filter(especie__id=i.id).filter(Q(c_altura__gte=j) & Q(c_altura__lte=j + esp_c_altura - 1))
                c_alturas[j + esp_c_altura - 1] = q.count()

        # dap
        esp_c_dap = 5
        c_daps = {}
        arboles = Arbol.objects.filter(especie__id=i.id, c_diametro_altura_pecho__gte=0)
        min_c_dap = None
        max_c_dap = None

        if arboles.count() > 0:
            min_c_dap = int(arboles.order_by('c_diametro_altura_pecho')[0].c_diametro_altura_pecho)
            max_c_dap = int(arboles.order_by('-c_diametro_altura_pecho')[0].c_diametro_altura_pecho)

        if (min_c_dap and max_c_dap):
            if min_c_dap == max_c_dap:
                max_c_dap += 1
            for j in range(min_c_dap - min_c_dap % esp_c_dap + 1 - esp_c_dap, max_c_dap + esp_c_dap, esp_c_dap):
                q = Arbol.objects.filter(especie__id=i.id).filter(
                    Q(c_diametro_altura_pecho__gte=j) & Q(c_diametro_altura_pecho__lte=j + esp_c_dap - 1))
                c_daps[j + esp_c_dap - 1] = q.count()

        # c_db
        esp_c_db = 5
        c_dbs = {}
        arboles = Arbol.objects.filter(especie__id=i.id, c_diametro_basal__gte=0)
        min_c_db = None
        max_c_db = None

        if arboles.count() > 0:
            min_c_db = int(arboles.order_by('c_diametro_basal')[0].c_diametro_basal)
            max_c_db = int(arboles.order_by('-c_diametro_basal')[0].c_diametro_basal)

        if (min_c_db and max_c_db):
            if min_c_db == max_c_db:
                max_c_db += 1
            for j in range(min_c_db - min_c_db % esp_c_db + 1 - esp_c_db, max_c_db + esp_c_db, esp_c_db):
                q = Arbol.objects.filter(especie__id=i.id).filter(
                    Q(c_diametro_basal__gte=j) & Q(c_diametro_basal__lte=j + esp_c_db - 1))
                c_dbs[j + esp_c_db - 1] = q.count()

        # c_densidad_follaje
        esp_c_densidad_follaje = 1
        c_densidad_follajees = {}
        arboles = Arbol.objects.filter(especie__id=i.id, c_densidad_follaje__gte=0)
        min_c_densidad_follaje = None
        max_c_densidad_follaje = None

        if arboles.count() > 0:
            min_c_densidad_follaje = int(arboles.order_by('c_densidad_follaje')[0].c_densidad_follaje)
            max_c_densidad_follaje = int(arboles.order_by('-c_densidad_follaje')[0].c_densidad_follaje)

        if (min_c_densidad_follaje and max_c_densidad_follaje):
            if min_c_densidad_follaje == max_c_densidad_follaje:
                max_c_densidad_follaje += 1
            for j in range(min_c_densidad_follaje - min_c_densidad_follaje % esp_c_densidad_follaje + 1 - esp_c_densidad_follaje, max_c_densidad_follaje + esp_c_densidad_follaje,
                           esp_c_densidad_follaje):
                q = Arbol.objects.filter(especie__id=i.id).filter(
                    Q(c_densidad_follaje__gte=j) & Q(c_densidad_follaje__lte=j + esp_c_densidad_follaje - 1))
                c_densidad_follajees[j + esp_c_densidad_follaje - 1] = q.count()

        # c_cobertura_follaje
        esp_c_cobertura_follaje = 5
        c_cobertura_follajes = {}
        arboles = Arbol.objects.filter(especie__id=i.id, c_cobertura_follaje__gte=0)
        min_c_cobertura_follaje = None
        max_c_cobertura_follaje = None

        if arboles.count() > 0:
            min_c_cobertura_follaje = int(arboles.order_by('c_cobertura_follaje')[0].c_cobertura_follaje)
            max_c_cobertura_follaje = int(arboles.order_by('-c_cobertura_follaje')[0].c_cobertura_follaje)

        if (min_c_cobertura_follaje and max_c_cobertura_follaje):
            if min_c_cobertura_follaje == max_c_cobertura_follaje:
                max_c_cobertura_follaje += 1
            for j in range(min_c_cobertura_follaje - min_c_cobertura_follaje % esp_c_cobertura_follaje + 1 - esp_c_cobertura_follaje, max_c_cobertura_follaje + esp_c_cobertura_follaje,
                           esp_c_cobertura_follaje):
                q = Arbol.objects.filter(especie__id=i.id).filter(
                    Q(c_cobertura_follaje__gte=j) & Q(c_cobertura_follaje__lte=j + esp_c_cobertura_follaje - 1))
                c_cobertura_follajes[j + esp_c_cobertura_follaje - 1] = q.count()





    print("----------------------------------------------------")
    print("alturas", i, min_altura, max_altura)
    print(alturas)

    print("daps", i, min_dap, max_dap)
    print(daps)

    print("dbs", i, min_db, max_db)
    print(dbs)

    print("densidades", i, min_densidad, max_densidad)
    print(densidades)

    print("coberturas", i, min_cobertura, max_cobertura)
    print(coberturas)

    # campo
    print("c_alturas", i, min_altura, max_altura)
    print(alturas)

    print("c_daps", i, min_dap, max_dap)
    print(daps)

    print("c_dbs", i, min_db, max_db)
    print(dbs)

    print("c_densidad_follajees", i, min_densidad, max_densidad)
    print(c_densidad_follajees)

    print("c_cobertura_follajes", i, min_cobertura, max_cobertura)
    print(c_cobertura_follajes)
    print("----------------------------------------------------")
