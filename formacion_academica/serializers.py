from rest_framework import serializers
from formacion_academica.models import *



class CursoEspecializacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoEspecializacion
        usuario = serializers.ReadOnlyField(source='usuario.username')
        fields = ('id', 'nombre_curso', 'descripcion', 'tipo', 'horas', 'fecha_inicio', 'fecha_fin', 'modalidad', 'area_conocimiento', 'dependencia', 'usuario')


class LicenciaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licenciatura
        usuario = serializers.ReadOnlyField(source='usuario.username')
        #fields = ('id', 'carrera', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')
        fields = ('id', 'carrera', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')


class MaestriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maestria
        usuario = serializers.ReadOnlyField(source='usuario.username')
        #fields = ('id', 'programa', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')
        fields = ('id', 'programa', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')


class DoctoradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctorado
        usuario = serializers.ReadOnlyField(source='usuario.username')
        #fields = ('id', 'programa', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')
        fields = ('id', 'programa', 'descripcion', 'dependencia', 'titulo_tesis', 'tesis_url', 'fecha_inicio', 'fecha_fin', 'fecha_grado', 'usuario')


class PostDoctoradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDoctorado
        usuario = serializers.ReadOnlyField(source='usuario.username')
        fields = ('titulo', 'descripcion', 'area_conocimiento', 'dependencia', 'proyecto', 'fecha_inicio', 'fecha_fin', 'usuario', 'tags')
