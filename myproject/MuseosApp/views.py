from django.shortcuts import render
from .models import Museo,Comentarios,Cambio_Estilo, Museo_Seleccionado
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context,RequestContext
from django.views.decorators.csrf import csrf_exempt
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def pagina_pie():
	url_xml = "https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full"
	url_descr = "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default"
	respuesta = '<html><body><p>Esta aplicacion utilza datos del portal de datos abiertos de la ciudad de Madrid</p></body></html>'
	respuesta += '<p><a href="' + url_xml + '">Enlace al fichero XML </a></p>'
	respuesta += '<p><a href="' + url_descr + '">Enlace a la descripción </a></p>'
	return respuesta
@csrf_exempt
def cargar_datos(request):
	tree = ET.parse('MuseosApp/201132-0-museos.xml')
	contenidos = tree.getroot()
#contenidos = ET.tostring(root, encoding='unicode', method='xml')
	equipamiento = ""
	for contenido in contenidos.findall('contenido'):
		for atributos in contenido.findall('atributos'):
			for atributo in atributos.findall('atributo'):
				if atributo.get('nombre') == "ID-ENTIDAD":
					id_museo = atributo.text
					id_museo = id_museo.encode(encoding='UTF-8')
				if atributo.get('nombre') == "NOMBRE":
					nombre = atributo.text
					nombre = nombre.encode(encoding='UTF-8')
				if atributo.get('nombre') == "DESCRIPCION-ENTIDAD":
					descripcion = atributo.text
					descripcion = descripcion.encode(encoding='UTF-8')
				if atributo.get('nombre') == "HORARIO":
					horario = atributo.text
					horario = horario.encode(encoding='UTF-8')
				if atributo.get('nombre') == "TRANSPORTE":
					transporte = atributo.text
					transporte = transporte.encode(encoding='UTF-8')
				if atributo.get('nombre') == "EQUIPAMIENTO":
					equipamiento = atributo.text
					equipamiento = equipamiento.encode(encoding='UTF-8')
				if atributo.get('nombre') == "ACCESIBILIDAD":
					accesibilidad = atributo.text
					accesibilidad = accesibilidad.encode(encoding='UTF-8')
				if atributo.get('nombre') == "CONTENT-URL":
					content_url = atributo.text
					content_url = content_url.encode(encoding='UTF-8')
				if atributo.get('nombre') == "LOCALIZACION":
					for subAtributo in atributo.findall('atributo'):
						if subAtributo.get('nombre') == "NOMBRE-VIA":
							nombre_via = subAtributo.text
							nombre_via = nombre_via.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "CLASE-VIAL":
							clase_vial = subAtributo.text
							clase_vial = clase_vial.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "NUM":
							num = subAtributo.text
							num = num.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "LOCALIDAD":
							localidad = subAtributo.text
							localidad = localidad.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "PROVINCIA":
							provincia = subAtributo.text
							provincia = provincia.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "CODIGO-POSTAL":
							codigo_postal = subAtributo.text
							codigo_postal = codigo_postal.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "BARRIO":
							barrio = subAtributo.text
							barrio = barrio.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "DISTRITO":
							distrito = subAtributo.text
							distrito = distrito.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "COORDENADA-X":
							coordenada_x = subAtributo.text
							coordenada_x = coordenada_x.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "COORDENADA-Y":
							coordenada_y = subAtributo.text
							coordenada_y = coordenada_y.encode(encoding='UTF-8')							
						if subAtributo.get('nombre') == "LATITUD":
							latitud = subAtributo.text
							latitud = latitud.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "LONGITUD":
							longitud = subAtributo.text
							longitud = longitud.encode(encoding='UTF-8')
				if atributo.get('nombre') == "DATOSCONTACTOS":
					for subAtributo in atributo.findall('atributo'):
						if subAtributo.get('nombre') == "TELEFONO":
							telefono = subAtributo.text
							telefono = telefono.encode(encoding='UTF-8')
						if subAtributo.get('nombre') == "EMAIL":
							email = subAtributo.text
							email = email.encode(encoding='UTF-8')
		museos = Museo(id_museo = id_museo,nombre = nombre,descripcion = descripcion,horario = horario,equipamiento = equipamiento,transporte = transporte,accesibilidad = accesibilidad, content_url = content_url,nombre_via = nombre_via,clase_vial = clase_vial,num = num,
			localidad = localidad,provincia = provincia,codigo_postal = codigo_postal,barrio = barrio, distrito = distrito,coordenada_x = coordenada_x,coordenada_y = coordenada_y, latitud = latitud, longitud = longitud,
             telefono = telefono, email = email)
		museos.save()
	return HttpResponseRedirect('/')

@csrf_exempt
def pagina_principal(request): #DE MOMENTO SACO LA LISTA DE MUSEOS 	
	template = get_template("pagina_principal.html")
	pie_pagina = pagina_pie()	
	c = Context({'pie_pagina':pie_pagina})
	return HttpResponse(template.render(c))		

@csrf_exempt		
def pagina_museos(request):
	template = get_template('pagina_museos.html')
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@,' + user + '<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a><br>'
	else:
		form_logueado = 'Para entrar al sitio vaya al '+'<a href="http://localhost:8000/">Inicio</a>'

	museos_filtrados = ""
	lista_filtros = ""
	filtro_distrito = ""
	if request.method == "POST":
		filtro_distrito = request.POST["distrito"].upper()
		if filtro_distrito != "":				
			museos_filtrados = Museo.objects.filter(distrito = filtro_distrito)
			lista_filtros = "<h2>Los museos del " + filtro_distrito + " son:</h2><br>"				
			for i in museos_filtrados:	
				lista_filtros += '<h3>'+i.nombre+'</h3>'
				lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
				lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
				lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
				if filtro_distrito != i.distrito:
					lista_filtros += filtro_distrito + "no existe: NO HAY MUSEOS" + i.distrito

	else:
		museos_filtrados = Museo.objects.all()
		for i in museos_filtrados:
			lista_filtros += '<h3>'+i.nombre+'</h3>'
			lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
			lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
			lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
	pie_pagina = pagina_pie()
	c = Context({'form_logueado': form_logueado,'lista_filtros':lista_filtros,'pie_pagina':pie_pagina,})
	
	return HttpResponse(template.render(c))			


@csrf_exempt
def pagina_museo(request,identidad):
	template = get_template('pagina_museo.html')
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@, ' + user + '<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a><br>'
	else:
		form_logueado = 'Para entrar al sitio vaya al '+'<a href="http://localhost:8000/">Inicio</a>'
	try:
		id_mus = identidad.split('/')[0]
		museo = Museo.objects.get(id_museo = id_mus)
		nombre = museo.nombre
		descripcion = museo.descripcion
		horario = museo.horario
		transporte = museo.transporte
		barrio = museo.barrio
		distrito = museo.distrito
		email = museo.email
		num = museo.num
		clase_vial = museo.clase_vial
		nombre_via = museo.nombre_via
		telefono = museo.telefono
		localidad = museo.localidad
		provincia = museo.provincia
		codigo_postal = museo.codigo_postal
		coordenada_x = museo.coordenada_x
		coordenada_y = museo.coordenada_y
		latitud = museo.latitud
		longitud = museo.longitud
		content_url = museo.content_url
		accesibilidad = museo.accesibilidad
		equipamiento = museo.equipamiento
		muestra_museos = '<h2>' + '<a href="' + content_url + '">' + nombre +'</a></h2>'
		muestra_museos += "<h4>Descripcion: </h4>" + descripcion + '<br>'
		muestra_museos += "<h4>Equipamiento: </h4>" + equipamiento + '<br>'
		if accesibilidad == 1:
			entrar = "SI"
		else:
			entrar = "NO"
		muestra_museos += "<h4>Accesible: </h4>" + entrar + '<br>'
		muestra_museos += "<h4>Horario: </h4>" + horario+ '<br>'
		muestra_museos += "<h4>Direccion: </h4>" + nombre_via + "," + str(num) + "en el barrio de " + barrio + " perteneciente al distrito " + distrito+ ' con codigo postal: ' + str(codigo_postal) +'<br>'
		muestra_museos += "<h4>Como llegar con transporte público: </h4>" + transporte+ '<br>'
		muestra_museos += "<h3>Datos de Contacto: </h3>"+ '<br>'
		muestra_museos += "<h4>      Telefono: </h4>" + telefono+ '<br>'
		muestra_museos += "<h4>      Email: </h4>" + email+ '<br>'
		form_comentario = ''
		muestra_comentarios = ''
		if request.user.is_authenticated():
			form_comentario += '<p>Añada un comentario: <br></p>'
			form_comentario += '<form action="" method="POST">'
			form_comentario += '<input type="text" name="comentario"'
			form_comentario += '<<input type="submit" value=""></form>'
		if request.method == "POST":
			comentario = request.POST['comentario']
			museo = Museo.objects.get(id_museo = id_mus)
			museo.num_comentario = museo.num_comentario + 1
			nuevo_comentario = Comentarios(museo = museo,txt = comentario)
			nuevo_comentario.save()
			museo.save()
			lista_comentarios = Comentarios.objects.all()
			muestra_comentarios = '<h4>Lista de Comentarios:</h4>'
			for comentario in lista_comentarios:
				if museo.nombre == comentario.museo.nombre:
					muestra_comentarios += comentario.txt
					muestra_comentarios += '<br>'
		else:
			lista_comentarios = Comentarios.objects.all()
			muestra_comentarios = '<h4>Lista de Comentarios:</h4>'
			for comentario in lista_comentarios:
				if museo.nombre == comentario.museo.nombre:
					muestra_comentarios += comentario.txt
					muestra_comentarios += '<br>'
		pie_pagina = pagina_pie()
		c = Context({'form_logueado':form_logueado,'muestra_museos':muestra_museos,'form_comentario':form_comentario,'muestra_comentarios':muestra_comentarios,'pie_pagina':pie_pagina})
		return HttpResponse(template.render(c))		
	except ObjectDoesNotExist:
		return HttpResponse("No existe ningún museos para ese id")