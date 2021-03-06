from graphos.renderers.gchart import PieChart, BarChart
from graphos.sources.simple import SimpleDataSource




class ArbolHistogramas(View):
    template_name = 'histogramas.html'

    def get(self, request):
        data = {}
        especies = EspecieArbol.objects.all().annotate(num=Count('arbol'))
        for i in especies:
            data[i.id] = {}

            countt = Arbol.objects.filter(especie__id=i.id).count()
            data[i.id]['count'] = countt

            # altura
            esp_altura = 50
            #alturas = {}
            alturas = [['tope', 'cantidad']]
            arboles = Arbol.objects.filter(especie__id=i.id, altura__gte=1)
            min_altura = None
            max_altura = None

            if arboles.count() > 0:
                min_altura = int(arboles.order_by('altura')[0].altura)
                max_altura = int(arboles.order_by('-altura')[0].altura)
                max_alturaa = int(arboles.order_by('-altura')[0].altura)

            if (min_altura and max_altura):
                if min_altura == max_altura:
                    max_altura += 1
                for j in range(min_altura - min_altura%esp_altura + 1 - esp_altura, max_altura, esp_altura):
                    q = Arbol.objects.filter(especie__id=i.id).filter(Q(altura__gte=j) & Q(altura__lte=j + esp_altura - 1))
                    # alturas[j+esp_altura - 1] = q.count()
                    alturas.append([str(j+esp_altura - 1), q.count()])

            altura_avg = EspecieArbol.objects.filter(id=i.id, arbol__altura__gte=1).annotate(altura_avg=Avg('arbol__altura'))[0].altura_avg
            altura_stdev = EspecieArbol.objects.filter(id=i.id, arbol__altura__gte=1).annotate(altura_stdev=StdDev('arbol__altura'))[0].altura_stdev
            altura_var = EspecieArbol.objects.filter(id=i.id, arbol__altura__gte=1).annotate(altura_var=Var('arbol__altura'))[0].altura_var

            alturas_source = SimpleDataSource(data=alturas)
            data[i.id]['min_altura'] = min_altura
            data[i.id]['max_altura'] = max_alturaa
            data[i.id]['altura_avg'] = altura_avg
            data[i.id]['altura_stdev'] = altura_stdev
            data[i.id]['altura_var'] = altura_var
            # data[i.id]['alturas'] = alturas
            data[i.id]['alturas'] = BarChart(alturas_source)

            # dap
            esp_dap = 5
            # daps = {}
            daps = [['tope', 'cantidad']]
            arboles = Arbol.objects.filter(especie__id=i.id, diametro_altura_pecho__gte=1)
            min_dap = None
            max_dap = None

            if arboles.count() > 0:
                min_dap = int(arboles.order_by('diametro_altura_pecho')[0].diametro_altura_pecho)
                max_dap = int(arboles.order_by('-diametro_altura_pecho')[0].diametro_altura_pecho)
                max_dapp = int(arboles.order_by('-diametro_altura_pecho')[0].diametro_altura_pecho)

            if (min_dap and max_dap):
                if min_dap == max_dap:
                    max_dap += 1
                for j in range(min_dap - min_dap%esp_dap + 1 - esp_dap, max_dap + esp_dap, esp_dap):

                    q = Arbol.objects.filter(especie__id=i.id).filter(Q(diametro_altura_pecho__gte=j) & Q(diametro_altura_pecho__lte=j + esp_dap - 1))
                    #daps[j+esp_dap - 1] = q.count()
                    daps.append([str(j + esp_dap - 1), q.count()])

            dap_avg   = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(dap_avg=Avg('arbol__diametro_altura_pecho'))[0].dap_avg
            dap_stdev = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(dap_stdev=StdDev('arbol__diametro_altura_pecho'))[0].dap_stdev
            dap_var   = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(dap_var=Var('arbol__diametro_altura_pecho'))[0].dap_var

            daps_source = SimpleDataSource(data=daps)

            data[i.id]['min_dap'] = min_dap
            data[i.id]['max_dap'] = max_dapp
            data[i.id]['dap_avg'] = dap_avg
            data[i.id]['dap_stdev'] = dap_stdev
            data[i.id]['dap_var'] = dap_var
            #data[i.id]['daps'] = daps
            data[i.id]['daps'] = BarChart(daps_source)


            # db
            esp_db = 5
            # dbs = {}
            dbs = [['tope', 'cantidad']]
            arboles = Arbol.objects.filter(especie__id=i.id, diametro_basal__gte=1)
            min_db = None
            max_db = None

            if arboles.count() > 0:
                min_db = int(arboles.order_by('diametro_basal')[0].diametro_basal)
                max_db = int(arboles.order_by('-diametro_basal')[0].diametro_basal)
                max_dbb = int(arboles.order_by('-diametro_basal')[0].diametro_basal)

            if (min_db and max_db):
                if min_db == max_db:
                    max_db += 1
                for j in range(min_db - min_db % esp_db + 1 - esp_db, max_db + esp_db, esp_db):
                    q = Arbol.objects.filter(especie__id=i.id).filter(
                        Q(diametro_altura_pecho__gte=j) & Q(diametro_altura_pecho__lte=j + esp_db - 1))
                    # dbs[j + esp_db - 1] = q.count()
                    dbs.append([str(j + esp_db - 1), q.count()])

            db_avg   = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(db_avg=Avg('arbol__diametro_altura_pecho'))[0].db_avg
            db_stdev = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(db_stdev=StdDev('arbol__diametro_altura_pecho'))[0].db_stdev
            db_var   = EspecieArbol.objects.filter(id=i.id, arbol__diametro_altura_pecho__gte=1).annotate(db_var=Var('arbol__diametro_altura_pecho'))[0].db_var

            dbs_source = SimpleDataSource(data=dbs)
            data[i.id]['min_db'] = min_db
            data[i.id]['max_db'] = max_dbb
            data[i.id]['db_avg'] = db_avg
            data[i.id]['db_stdev'] = db_stdev
            data[i.id]['db_var'] = db_var
            #data[i.id]['dbs'] = dbs
            data[i.id]['dbs'] = BarChart(dbs_source)


            # densidad
            esp_densidad = 1
            # densidades = {}
            densidades = [['tope', 'cantidad']]
            arboles = Arbol.objects.filter(especie__id=i.id, densidad__gte=1)
            min_densidad = None
            max_densidad = None

            if arboles.count() > 0:
                min_densidad = int(arboles.order_by('densidad')[0].densidad)
                max_densidad = int(arboles.order_by('-densidad')[0].densidad)
                max_densidadd = int(arboles.order_by('-densidad')[0].densidad)

            if (min_densidad and max_densidad):
                if min_densidad == max_densidad:
                    max_densidad += 1
                for j in range(min_densidad - min_densidad % esp_densidad + 1 - esp_densidad, max_densidad + esp_densidad, esp_densidad):
                    q = Arbol.objects.filter(especie__id=i.id).filter(
                        Q(densidad__gte=j) & Q(densidad__lte=j + esp_densidad - 1))
                    # densidades[j + esp_densidad - 1] = q.count()
                    densidades.append([str(j + esp_densidad - 1), q.count()])

            densidad_avg = EspecieArbol.objects.filter(id=i.id, arbol__densidad__gte=1).annotate(densidad_avg=Avg('arbol__densidad'))[0].densidad_avg
            densidad_stdev = EspecieArbol.objects.filter(id=i.id, arbol__densidad__gte=1).annotate(densidad_stdev=StdDev('arbol__densidad'))[0].densidad_stdev
            densidad_var = EspecieArbol.objects.filter(id=i.id, arbol__densidad__gte=1).annotate(densidad_var=Var('arbol__densidad'))[0].densidad_var

            densidades_source = SimpleDataSource(data=densidades)

            data[i.id]['min_densidad'] = min_densidad
            data[i.id]['max_densidad'] = max_densidadd
            data[i.id]['densidad_avg'] = densidad_avg
            data[i.id]['densidad_stdev'] = densidad_stdev
            data[i.id]['densidad_var'] = densidad_var
            # data[i.id]['densidades'] = densidades
            data[i.id]['densidades'] = BarChart(densidades_source)


            # cobertura
            esp_cobertura = 5
            # coberturas = {}
            coberturas = [['tope', 'cantidad']]
            arboles = Arbol.objects.filter(especie__id=i.id, cobertura__gte=1)
            min_cobertura = None
            max_cobertura = None

            if arboles.count() > 0:
                min_cobertura = int(arboles.order_by('cobertura')[0].cobertura)
                max_cobertura = int(arboles.order_by('-cobertura')[0].cobertura)
                max_coberturaa = int(arboles.order_by('-cobertura')[0].cobertura)

            if (min_cobertura and max_cobertura):
                if min_cobertura == max_cobertura:
                    max_cobertura += 1
                for j in range(min_cobertura - min_cobertura % esp_cobertura + 1 - esp_cobertura, max_cobertura + esp_cobertura,
                               esp_cobertura):
                    q = Arbol.objects.filter(especie__id=i.id).filter(
                        Q(cobertura__gte=j) & Q(cobertura__lte=j + esp_cobertura - 1))
                    # coberturas[j + esp_cobertura - 1] = q.count()
                    coberturas.append([str(j + esp_cobertura - 1), q.count()])

                cobertura_avg = EspecieArbol.objects.filter(id=i.id, arbol__cobertura__gte=1).annotate(cobertura_avg=Avg('arbol__cobertura'))[0].cobertura_avg
                cobertura_stdev = EspecieArbol.objects.filter(id=i.id, arbol__cobertura__gte=1).annotate(cobertura_stdev=StdDev('arbol__cobertura'))[0].cobertura_stdev
                cobertura_var = EspecieArbol.objects.filter(id=i.id, arbol__cobertura__gte=1).annotate(cobertura_var=Var('arbol__cobertura'))[0].cobertura_var

                coberturas_source = SimpleDataSource(data=coberturas)

                data[i.id]['min_cobertura'] = min_cobertura
                data[i.id]['max_cobertura'] = max_coberturaa
                data[i.id]['cobertura_avg'] = cobertura_avg
                data[i.id]['cobertura_stdev'] = cobertura_stdev
                data[i.id]['cobertura_var'] = cobertura_var
                # data[i.id]['coberturas'] = coberturas
                data[i.id]['coberturas'] = BarChart(coberturas_source)


            # CAMPO

                # c_altura
                esp_c_altura = 50
                # c_alturas = {}
                c_alturas = [['tope', 'cantidad']]
                arboles = Arbol.objects.filter(especie__id=i.id, c_altura__gte=1)
                min_c_altura = None
                max_c_altura = None

                if arboles.count() > 0:
                    min_c_altura = int(arboles.order_by('c_altura')[0].c_altura)
                    max_c_altura = int(arboles.order_by('-c_altura')[0].c_altura)
                    max_c_alturaa = int(arboles.order_by('-c_altura')[0].c_altura)

                if (min_c_altura and max_c_altura):
                    if min_c_altura == max_c_altura:
                        max_c_altura += 1
                    for j in range(min_c_altura - min_c_altura % esp_c_altura + 1 - esp_c_altura, max_c_altura, esp_c_altura):
                        q = Arbol.objects.filter(especie__id=i.id).filter(Q(c_altura__gte=j) & Q(c_altura__lte=j + esp_c_altura - 1))
                        # c_alturas[j + esp_c_altura - 1] = q.count()
                        c_alturas.append([str(j + esp_c_altura - 1), q.count()])

                c_altura_avg = EspecieArbol.objects.filter(id=i.id, arbol__c_altura__gte=1).annotate(c_altura_avg=Avg('arbol__c_altura'))[0].c_altura_avg
                c_altura_stdev = EspecieArbol.objects.filter(id=i.id, arbol__c_altura__gte=1).annotate(c_altura_stdev=StdDev('arbol__c_altura'))[0].c_altura_stdev
                c_altura_var = EspecieArbol.objects.filter(id=i.id, arbol__c_altura__gte=1).annotate(c_altura_var=Var('arbol__c_altura'))[0].c_altura_var

                c_alturas_source = SimpleDataSource(data=c_alturas)

                data[i.id]['min_c_altura'] = min_c_altura
                data[i.id]['max_c_altura'] = max_c_alturaa
                data[i.id]['c_altura_avg'] = c_altura_avg
                data[i.id]['c_altura_stdev'] = c_altura_stdev
                data[i.id]['c_altura_var'] = c_altura_var
                # data[i.id]['c_alturas'] = c_alturas
                data[i.id]['c_alturas'] = BarChart(c_alturas_source)

                # dap
                esp_c_dap = 5
                # c_daps = {}
                c_daps = [['tope', 'cantidad']]
                arboles = Arbol.objects.filter(especie__id=i.id, c_diametro_altura_pecho__gte=1)
                min_c_dap = None
                max_c_dap = None

                if arboles.count() > 0:
                    min_c_dap = int(arboles.order_by('c_diametro_altura_pecho')[0].c_diametro_altura_pecho)
                    max_c_dap = int(arboles.order_by('-c_diametro_altura_pecho')[0].c_diametro_altura_pecho)
                    max_c_dapp = int(arboles.order_by('-c_diametro_altura_pecho')[0].c_diametro_altura_pecho)

                if (min_c_dap and max_c_dap):
                    if min_c_dap == max_c_dap:
                        max_c_dap += 1
                    for j in range(min_c_dap - min_c_dap % esp_c_dap + 1 - esp_c_dap, max_c_dap + esp_c_dap, esp_c_dap):
                        q = Arbol.objects.filter(especie__id=i.id).filter(
                            Q(c_diametro_altura_pecho__gte=j) & Q(c_diametro_altura_pecho__lte=j + esp_c_dap - 1))
                        # c_daps[j + esp_c_dap - 1] = q.count()
                        c_daps.append([str(j + esp_c_dap - 1), q.count()])

                c_dap_avg = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_altura_pecho__gte=1).annotate(c_dap_avg=Avg('arbol__c_diametro_altura_pecho'))[0].c_dap_avg
                c_dap_stdev = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_altura_pecho__gte=1).annotate(c_dap_stdev=StdDev('arbol__c_diametro_altura_pecho'))[0].c_dap_stdev
                c_dap_var = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_altura_pecho__gte=1).annotate(c_dap_var=Var('arbol__c_diametro_altura_pecho'))[0].c_dap_var

                c_daps_source = SimpleDataSource(data=c_daps)

                data[i.id]['min_c_dap'] = min_c_dap
                data[i.id]['max_c_dap'] = max_c_dapp
                data[i.id]['c_dap_avg'] = c_dap_avg
                data[i.id]['c_dap_stdev'] = c_dap_stdev
                data[i.id]['c_dap_var'] = c_dap_var
                # data[i.id]['c_daps'] = c_daps
                data[i.id]['c_daps'] = BarChart(c_daps_source)


                # c_db
                esp_c_db = 5
                # c_dbs = {}
                c_dbs = [['tope', 'cantidad']]
                arboles = Arbol.objects.filter(especie__id=i.id, c_diametro_basal__gte=1)
                min_c_db = None
                max_c_db = None

                if arboles.count() > 0:
                    min_c_db = int(arboles.order_by('c_diametro_basal')[0].c_diametro_basal)
                    max_c_db = int(arboles.order_by('-c_diametro_basal')[0].c_diametro_basal)
                    max_c_dbb = int(arboles.order_by('-c_diametro_basal')[0].c_diametro_basal)

                if (min_c_db and max_c_db):
                    if min_c_db == max_c_db:
                        max_c_db += 1
                    for j in range(min_c_db - min_c_db % esp_c_db + 1 - esp_c_db, max_c_db + esp_c_db, esp_c_db):
                        q = Arbol.objects.filter(especie__id=i.id).filter(
                            Q(c_diametro_basal__gte=j) & Q(c_diametro_basal__lte=j + esp_c_db - 1))
                        # c_dbs[j + esp_c_db - 1] = q.count()
                        c_dbs.append([str(j + esp_c_db - 1), q.count()])

                c_db_avg = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_basal__gte=1).annotate(c_db_avg=Avg('arbol__c_diametro_basal'))[0].c_db_avg
                c_db_stdev = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_basal__gte=1).annotate(c_db_stdev=StdDev('arbol__c_diametro_basal'))[0].c_db_stdev
                c_db_var = EspecieArbol.objects.filter(id=i.id, arbol__c_diametro_basal__gte=1).annotate(c_db_var=Var('arbol__c_diametro_basal'))[0].c_db_var

                c_dbs_source = SimpleDataSource(data=c_dbs)

                data[i.id]['min_c_db'] = min_c_db
                data[i.id]['max_c_db'] = max_c_dbb
                data[i.id]['c_db_avg'] = c_db_avg
                data[i.id]['c_db_stdev'] = c_db_stdev
                data[i.id]['c_db_var'] = c_db_var
                # data[i.id]['c_dbs'] = c_dbs
                data[i.id]['c_dbs'] = BarChart(c_dbs_source)


                # c_densidad_follaje
                esp_c_densidad_follaje = 1
                # c_densidad_follajes = {}
                c_densidad_follajes = [['tope', 'cantidad']]
                arboles = Arbol.objects.filter(especie__id=i.id, c_densidad_follaje__gte=1)
                min_c_densidad_follaje = None
                max_c_densidad_follaje = None

                if arboles.count() > 0:
                    min_c_densidad_follaje = int(arboles.order_by('c_densidad_follaje')[0].c_densidad_follaje)
                    max_c_densidad_follaje = int(arboles.order_by('-c_densidad_follaje')[0].c_densidad_follaje)
                    max_c_densidad_follajee = int(arboles.order_by('-c_densidad_follaje')[0].c_densidad_follaje)

                if (min_c_densidad_follaje and max_c_densidad_follaje):
                    if min_c_densidad_follaje == max_c_densidad_follaje:
                        max_c_densidad_follaje += 1
                    for j in range(min_c_densidad_follaje - min_c_densidad_follaje % esp_c_densidad_follaje + 1 - esp_c_densidad_follaje, max_c_densidad_follaje + esp_c_densidad_follaje,
                                   esp_c_densidad_follaje):
                        q = Arbol.objects.filter(especie__id=i.id).filter(
                            Q(c_densidad_follaje__gte=j) & Q(c_densidad_follaje__lte=j + esp_c_densidad_follaje - 1))
                        # c_densidad_follajes[j + esp_c_densidad_follaje - 1] = q.count()
                        c_densidad_follajes.append([str(j + esp_c_densidad_follaje - 1), q.count()])

                c_densidad_follaje_avg = EspecieArbol.objects.filter(id=i.id, arbol__c_densidad_follaje__gte=1).annotate(c_densidad_follaje_avg=Avg('arbol__c_densidad_follaje'))[0].c_densidad_follaje_avg
                c_densidad_follaje_stdev = EspecieArbol.objects.filter(id=i.id, arbol__c_densidad_follaje__gte=1).annotate(c_densidad_follaje_stdev=StdDev('arbol__c_densidad_follaje'))[0].c_densidad_follaje_stdev
                c_densidad_follaje_var = EspecieArbol.objects.filter(id=i.id, arbol__c_densidad_follaje__gte=1).annotate(c_densidad_follaje_var=Var('arbol__c_densidad_follaje'))[0].c_densidad_follaje_var

                c_densidad_follajes_source = SimpleDataSource(data=c_densidad_follajes)

                data[i.id]['min_c_densidad_follaje'] = min_c_densidad_follaje
                data[i.id]['max_c_densidad_follaje'] = max_c_densidad_follajee
                data[i.id]['c_densidad_follaje_avg'] = c_densidad_follaje_avg
                data[i.id]['c_densidad_follaje_stdev'] = c_densidad_follaje_stdev
                data[i.id]['c_densidad_follaje_var'] = c_densidad_follaje_var
                data[i.id]['c_densidad_follajes'] = BarChart(c_densidad_follajes_source)


                # c_cobertura_follaje
                esp_c_cobertura_follaje = 5
                # c_cobertura_follajes = {}
                c_cobertura_follajes = [['tope', 'cantidad']]
                arboles = Arbol.objects.filter(especie__id=i.id, c_cobertura_follaje__gte=1)
                min_c_cobertura_follaje = None
                max_c_cobertura_follaje = None

                if arboles.count() > 0:
                    min_c_cobertura_follaje = int(arboles.order_by('c_cobertura_follaje')[0].c_cobertura_follaje)
                    max_c_cobertura_follaje = int(arboles.order_by('-c_cobertura_follaje')[0].c_cobertura_follaje)
                    max_c_cobertura_follajee = int(arboles.order_by('-c_cobertura_follaje')[0].c_cobertura_follaje)

                if (min_c_cobertura_follaje and max_c_cobertura_follaje):
                    if min_c_cobertura_follaje == max_c_cobertura_follaje:
                        max_c_cobertura_follaje += 1
                    for j in range(min_c_cobertura_follaje - min_c_cobertura_follaje % esp_c_cobertura_follaje + 1 - esp_c_cobertura_follaje, max_c_cobertura_follaje + esp_c_cobertura_follaje,
                                   esp_c_cobertura_follaje):
                        q = Arbol.objects.filter(especie__id=i.id).filter(
                            Q(c_cobertura_follaje__gte=j) & Q(c_cobertura_follaje__lte=j + esp_c_cobertura_follaje - 1))
                        # c_cobertura_follajes[j + esp_c_cobertura_follaje - 1] = q.count()
                        c_cobertura_follajes.append([str(j + esp_c_cobertura_follaje - 1), q.count()])

                c_cobertura_follaje_avg = EspecieArbol.objects.filter(id=i.id, arbol__c_cobertura_follaje__gte=1).annotate(c_cobertura_follaje_avg=Avg('arbol__c_cobertura_follaje'))[0].c_cobertura_follaje_avg
                c_cobertura_follaje_stdev = EspecieArbol.objects.filter(id=i.id, arbol__c_cobertura_follaje__gte=1).annotate(c_cobertura_follaje_stdev=StdDev('arbol__c_cobertura_follaje'))[0].c_cobertura_follaje_stdev
                c_cobertura_follaje_var = EspecieArbol.objects.filter(id=i.id, arbol__c_cobertura_follaje__gte=1).annotate(c_cobertura_follaje_var=Var('arbol__c_cobertura_follaje'))[0].c_cobertura_follaje_var

                c_cobertura_follajes_source = SimpleDataSource(data=c_cobertura_follajes)

                data[i.id]['min_c_cobertura_follaje'] = min_c_cobertura_follaje
                data[i.id]['max_c_cobertura_follaje'] = max_c_cobertura_follajee
                data[i.id]['c_cobertura_follaje_avg'] = c_cobertura_follaje_avg
                data[i.id]['c_cobertura_follaje_stdev'] = c_cobertura_follaje_stdev
                data[i.id]['c_cobertura_follaje_var'] = c_cobertura_follaje_var
                data[i.id]['c_cobertura_follajes'] = BarChart(c_cobertura_follajes_source)





            """
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
            print("----------------------------------------------------") """

        return render(request, self.template_name, data)