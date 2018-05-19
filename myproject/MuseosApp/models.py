from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Museo(models.Model): 
	id_museo = models.IntegerField()
	nombre = models.CharField(max_length = 128)
	descripcion = models.TextField(null = True)
	horario =  models.TextField(null = True)
	equipamiento = models.TextField(null = True)
	transporte = models.TextField(null = True)
	accesibilidad = models.CharField(max_length= 8)
	content_url = models.URLField()
	nombre_via = models.CharField(max_length = 128)
	clase_vial = models.CharField(max_length = 64)
	num = models.FloatField()
	localidad = models.CharField(max_length = 64)
	provincia = models.CharField(max_length = 64)
	codigo_postal = models.IntegerField(null = True)
	barrio =models.CharField(max_length = 64)
	distrito = models.CharField(max_length = 64)
	coordenada_x = models.IntegerField(null = True)
	coordenada_y = models.IntegerField(null = True)
	latitud = models.FloatField(null = True)
	longitud = models.FloatField(null = True)
	telefono = models.TextField(null = True)
	email = models.CharField(max_length = 128,null = True)
	num_comentario = models.IntegerField(default = 0)
	
class Comentarios(models.Model):
	museo = models.ForeignKey(Museo)
	txt = models.TextField()
	usuario = models.CharField(max_length = 32)


class Cambio_Estilo(models.Model):
	usuario = models.ForeignKey(User)
	tamaño = models.CharField(max_length = 32)
	color = models.CharField(max_length = 32)
	titulo = models.TextField()

class Museo_Seleccionado(models.Model):
	usuario = models.ForeignKey(User)
	museo = models.ForeignKey(Museo)
	fecha = models.DateField()