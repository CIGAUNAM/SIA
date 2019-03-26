from rest_framework import serializers
from experiencia_profesional.models import *



class ExperienciaLaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienciaProfesional
        usuario = serializers.ReadOnlyField(source='usuario.username')
        fields = ('id', 'dependencia', 'nombramiento', 'es_nombramiento_definitivo', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuario')


class LineaInvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaInvestigacion
        usuario = serializers.ReadOnlyField(source='usuario.username')
        fields = ('id', 'linea_investigacion', 'descripcion', 'dependencia', 'fecha_inicio', 'fecha_fin', 'usuario')


class CapacidadPotencialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacidadPotencialidad
        usuario = serializers.ReadOnlyField(source='usuario.username')
        fields = ('id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuario')


