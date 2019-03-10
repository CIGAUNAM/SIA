from rest_framework import serializers
from nucleo.models import *
from formacion_academica.models import *






class UserSerializer(serializers.ModelSerializer):
    cursos_especializacion = serializers.PrimaryKeyRelatedField(many=True, queryset=CursoEspecializacion.objects.all())
    licenciaturas = serializers.PrimaryKeyRelatedField(many=True, queryset=Licenciatura.objects.all())
    maestrias = serializers.PrimaryKeyRelatedField(many=True, queryset=Maestria.objects.all())
    doctorados = serializers.PrimaryKeyRelatedField(many=True, queryset=Doctorado.objects.all())
    postdoctorados = serializers.PrimaryKeyRelatedField(many=True, queryset=PostDoctorado.objects.all())


    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'tipo', 'fecha_nacimiento', 'pais_origen', 'rfc',
                  'direccion', 'direccion_continuacion', 'ciudad', 'telefono', 'celular', 'url', 'sni', 'pride', 'ingreso_unam', 'ingreso_entidad',
                  'cursos_especializacion', 'licenciaturas', 'maestrias', 'doctorados', 'postdoctorados')
        read_only_fields = ('username',)


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitucionSimple
        fields = '__all__'


class ProgramaLicenciaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaLicenciatura
        fields = '__all__'

class ProgramaMaestriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaMaestria
        fields = '__all__'

class ProgramaDoctoradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaDoctorado
        fields = '__all__'

class RevistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revista
        fields = '__all__'








class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('id', 'nombre', 'descripcion', 'tipo_cargo')


class NombramientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nombramiento
        fields = ('id', 'nombramiento', 'clave', 'descripcion')


class AreaConocimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaConocimiento
        fields = ('id', 'area_conocimiento', 'categoria', 'descripcion')


class AreaEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaEspecialidad
        fields = ('id', 'especialidad', 'descripcion', 'area_conocimiento')


class ImpactoSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactoSocial
        fields = ('id', 'impacto_social', 'descripcion')


class FinanciamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financiamiento
        fields = ('id', 'tipo_financiamiento', 'descripcion', 'programas_financiamiento', 'dependencias_financiamiento', 'clave_proyecto')


class MetodologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodologia
        fields = ('id', 'metodologia', 'descripcion')


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoInvestigacion
        fields = ('id', 'nombre_proyecto', 'descripcion', 'es_permanente', 'fecha_inicio', 'fecha_fin', 'responsables', 'participantes', 'status', 'clasificacion', 'organizacion', 'modalidad', 'tematica_genero', 'dependencias', 'financiamientos', 'metodologias', 'especialidades', 'impactos_sociales', 'tecnicos', 'alumnos_doctorado', 'alumnos_maestria', 'alumnos_licenciatura')
