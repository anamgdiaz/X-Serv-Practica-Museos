from django.shortcuts import render
from .models import Museo,Comentarios,Cambio_Estilo, Museo_Seleccionado,Museo_CSV
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.template.loader import get_template
from django.template import Context,RequestContext
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
import csv
# Create your views here.

def pagina_pie():
	url_xml = "https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full"
	url_descr = "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default"
	respuesta = '<html><body><p>Esta aplicacion utilza datos del portal de datos abiertos de la ciudad de Madrid</p></body></html>'
	respuesta += '<p><a href="' + url_xml + '">Enlace al fichero XML </a></p>'
	respuesta += '<p><a href="' + url_descr + '">Enlace a la descripción </a></p>'
	return respuesta

@csrf_exempt
def cargar_datos_csv(request):	
	with open('MuseosApp/201132-0-museos.csv',encoding='ISO-8859-1') as csvfile:
		reader = csv.reader(csvfile, delimiter=';')
		i = 0
		for row in reader:
			try:
				id_museo = row[0]
				nombre = row[1]
				descripcion = row[2]
				horario =  row[3]
				equipamiento = row[4]
				transporte = row[5]
				accesibilidad = row[7]
				content_url = row[8]
				nombre_via = row[9]
				num = row[12]
				localidad = row[17]
				provincia = row[18]
				codigo_postal = row[19]
				barrio = row[20]
				distrito = row[21]
				telefono = row[26]
				email = row[28]
				if i != 0:
					museo_csv = Museo_CSV(id_museo=id_museo,nombre = nombre,descripcion = descripcion,horario = horario,transporte=transporte,accesibilidad = accesibilidad,nombre_via = nombre_via,num = num,
					 localidad = localidad,provincia = provincia,codigo_postal = codigo_postal,barrio = barrio,distrito= distrito,telefono =telefono,email= email)
					museo_csv.save()
				i = i + 1
			except IndexError:
				pass

	return HttpResponseRedirect('/')

@csrf_exempt
def cargar_datos(request):
	tree = ET.parse('MuseosApp/201132-0-museos.xml')
	contenidos = tree.getroot()
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
def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username,password = password)
	if user is not None:
		login(request,user)
		return HttpResponseRedirect('/'+str(user))
	else:
		newuser = User.objects.create_user(username = username,password = password)
		users = User.objects.get(username = username)
		titulo_pagina = 'Página de ' + newuser.username
		cambios_estilo = Cambio_Estilo(titulo = titulo_pagina,usuario =users)
		cambios_estilo.save()
		return HttpResponseRedirect('/')

@csrf_exempt
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

@csrf_exempt
def logueado_form(request):
	login = '<form action="login" method="POST">'
	login += 'Usuario    	<input type="text" name="username"><br><br>'
	login += 'Contraseña	<input type="password" name="password"><br><br>'
	login += '<input type="submit" value="Entrar"></form>'
	return login 
def boton_accesible(valor_acc):
	respuesta =  """
			<form action="" method="POST">
			<button type="submit" name = "accesible"value=""" +str(valor_acc)+ """>Mostrar museos accesibles</button>
			</form>
		"""
	return respuesta 
@csrf_exempt
def pagina_principal(request):
	template = get_template("pagina_principal.html")
	lista_usuarios = ''
	lista = ''
	usuario=''
	valor = 1
	titulo_pagina = ''
	cargar = ''
	cargar_csv = ''
	if request.user.is_authenticated():
		usuario = str(request.user)
		form_logueado = 'Bienvenid@,' + usuario + '<br>'
		form_logueado += '<a href="http://localhost:8000/'+ usuario + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ usuario + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ usuario + '/json"> Mi página en JSON</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a>'
	else:
		form_logueado = logueado_form(request)
	if request.method == 'POST':
		key = request.body.decode("utf-8").split('=')[0]
		valor = request.body.decode("utf-8").split('=')[1]
		if key == 'accesible' and valor == '1':	
			valor = 0	
			museos = Museo.objects.all()
			museos_c_acc = museos.order_by('-num_comentario')[:5]
			for i in museos_c_acc:
				comentarios = Comentarios.objects.filter(museo = i)
				if len(comentarios) != 0 and i.accesibilidad == '1':
					nombre_museo = i.nombre
					content_url = i.content_url
					lista += '<br><a href="'+ content_url + '">' + nombre_museo + '</a><br>'
					lista += "<h4>Direccion: </h4>" + i.nombre_via + "," + str(i.num) + '<br>'
					lista += '<p><a href="http://localhost:8000/museos/'+ str(i.id_museo)+ '">'+'Más Información</a></p><br>'
		elif key == 'accesible' and valor == '0':
			valor = 1
			museos = Museo.objects.all()
			museos_c_acc = museos.order_by('-num_comentario')[:5]
			for i in museos_c_acc:
				comentarios = Comentarios.objects.filter(museo = i)
				if len(comentarios) != 0 :
					nombre_museo = i.nombre
					content_url = i.content_url
					lista += '<br><a href="'+ content_url + '">' + nombre_museo + '</a><br>'
					lista += "<h4>Direccion: </h4>" + i.nombre_via + "," + str(i.num) + '<br>'
					lista += '<a href="http://localhost:8000/museos/' + str(i.id_museo) + '">' + "Más información" + '</a><br>'
	else:
		museos = Museo.objects.all()
		museos_c_acc = museos.order_by('-num_comentario')[:5]
		for i in museos_c_acc:
			comentarios = Comentarios.objects.filter(museo = i)
			if len(comentarios) != 0 :
				nombre_museo = i.nombre
				content_url = i.content_url
				lista += '<br><a href="'+ content_url + '">' + nombre_museo + '</a><br>'
				lista += "<h4>Direccion: </h4>" + i.nombre_via + "," + str(i.num) + '<br>'
				lista += '<a href="http://localhost:8000/museos/' + str(i.id_museo) + '">' + "Más información" + '</a><br>'
	museos = Museo.objects.all()
	if len(museos) == 0:
		cargar = '<form method="post" action="/cargar_datos">'
		cargar += '<input type="submit" value="Cargar_museos" name="Cargar"></form>'
	museos_csv = Museo_CSV.objects.all()
	if len(museos_csv) == 0:
		cargar_csv = '<form method="post" action="/cargar_datos_csv">'
		cargar_csv += '<input type="submit" value="Cargar_museos_csv" name="Cargar CSV"></form>'
	pie_pagina = pagina_pie()
	Boton = boton_accesible(valor)
	usuario_entra = User.objects.all()
	lista_usuarios += "<h3>Lista de paginas personales: </h3>"+'<br>'
	for usuario in usuario_entra:
		lista_usuarios += usuario.username + ':'
		try :
			cambio_estilos = Cambio_Estilo.objects.filter(usuario = usuario)
			if len(cambio_estilos) == 0:
				titulo_pagina = 'Página de ' + usuario.username
				cambios_estilo = Cambio_Estilo(titulo = titulo_pagina,usuario=usuario)
				cambios_estilo.save()
			else:
				for j in cambio_estilos:
					titulo_pagina = j.titulo
			lista_usuarios += '<a href=http://localhost:8000/'+ str(usuario.username) + '>' + titulo_pagina +'</a><br>'
		except ObjectDoesNotExist:
			lista_usuarios += "Pagina personal de " + str(usuario.username)	

	c = Context({'Boton':Boton,'pie_pagina':pie_pagina,'form_logueado':form_logueado,'lista':lista,'lista_usuarios':lista_usuarios,'cargar':cargar,'cargar_csv':cargar_csv})	
	return HttpResponse(template.render(c))		

@csrf_exempt		
def pagina_museos(request):
	template = get_template('pagina_museos.html')
	seleccion = ''
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@,' + user + '<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/json"> Mi página en JSON</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a><br>'
	else:
		form_logueado = 'Para entrar al sitio vaya al '+'<a href="http://localhost:8000/">Inicio</a>'
	valor = 1
	museos_filtrados = ""
	lista_filtros = ""
	filtro_distrito = ""
	if request.method == "POST":
		key = request.body.decode("utf-8").split('=')[0]
		valor = request.body.decode("utf-8").split('=')[1]
		if key == 'accesible' and valor == '1':	
			valor = 0	
			museos = Museo.objects.all()
			for i in museos:
				if i.accesibilidad == '1':
					lista_filtros += '<h3>'+i.nombre+'</h3>'
					lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
					lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
					lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
		elif key == 'accesible' and valor == '0':
			valor = 1
			museos = Museo.objects.all()
			paginator = Paginator(museos,15)
			page = request.GET.get('page')
			try:
	 			seleccion = paginator.page(page)
			except PageNotAnInteger:
				seleccion = paginator.page(1)
			except EmptyPage:
				seleccion = paginator.page(paginator.num_pages)
			for i in seleccion:
				lista_filtros += '<h3>'+i.nombre+'</h3>'
				lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
				lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
				lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
		elif key == 'distrito':
			filtro_distrito = request.POST["distrito"].upper()
			if filtro_distrito != "":				
				museos_filtrados = Museo.objects.filter(distrito = filtro_distrito)
				filtrado = False
				lista_filtros = "<h2>Los museos del " + filtro_distrito + " son:</h2><br>"				
				for i in museos_filtrados:	
					if filtro_distrito == i.distrito:
						filtrado = True
						lista_filtros += '<h3>'+i.nombre+'</h3>'
						lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
						lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
						lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
			if filtrado == False:
				distritos = Museo.objects.all().values_list('distrito')
				distinct_distrito = list(set(distritos))
				lista_filtros = "Escriba correctamente el distrito<br>"
				for i in distinct_distrito:
					lista_filtros += i[0] + '<br>'

	else:
		museos_filtrados = Museo.objects.all()
		paginator = Paginator(museos_filtrados,15)
		page = request.GET.get('page')
		try:
	 		seleccion = paginator.page(page)
		except PageNotAnInteger:
			seleccion = paginator.page(1)
		except EmptyPage:
			seleccion = paginator.page(paginator.num_pages)
		for i in seleccion:
			lista_filtros += '<h3>'+i.nombre+'</h3>'
			lista_filtros += 'Dirección:' + i.nombre_via + ',' + str(i.num) +'<br>'
			lista_filtros +='<a href="' + i.content_url + '">' + i.content_url +'</a><br>'
			lista_filtros+= '<a href=http://localhost:8000/museos/'+ str(i.id_museo)+ '>'+'Más Información</a><br>'
	Boton = boton_accesible(valor)
	pie_pagina = pagina_pie()
	c = Context({'form_logueado': form_logueado,'lista_filtros':lista_filtros,'seleccion':seleccion,'pie_pagina':pie_pagina,'Boton':Boton})
	
	return HttpResponse(template.render(c))			


@csrf_exempt
def pagina_museo(request,identidad):
	template = get_template('pagina_museo.html')
	puntuar = ''
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@, ' + user + '<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/json"> Mi página en JSON</a><br>'
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
		puntuacion = museo.puntuacion
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
		muestra_museos += "<h4>		 Puntuación: </h4>"+str(puntuacion)+'<br>'
		puntuar += '<br><br><form action="" method ="POST">'
		puntuar += '<button type="submit" name="Puntuar" value="'+nombre+'"><img src="/images/like.png"width="50"></button></form><br>'
		form_comentario = ''
		muestra_comentarios = ''
		if request.user.is_authenticated():
			form_comentario += '<p>Añada un comentario: <br></p>'
			form_comentario += '<form action="" method="POST">'
			form_comentario += '<input type="text" name="comentario">'
			form_comentario += '<input type="submit" value="Enviar"></form>'
			muestra_museos += '<form action="" method ="POST">'
			muestra_museos += '<button type="submit" name="Seleccionar" value="'+nombre+'">Seleccionar</button></form>'
		if request.method == "POST":
			key = request.body.decode("utf-8").split('=')[0]
			if key == "comentario":
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
			elif key == "Seleccionar":
				nombre_mus = request.POST['Seleccionar']
				fecha = datetime.datetime.today()
				lista_museos_seleccionados = Museo_Seleccionado.objects.all()
				try:
					museo = Museo.objects.get(nombre = nombre_mus)
					esta_seleccionado = False
					for i in lista_museos_seleccionados:
						if str(i.usuario) == str(request.user):
							if nombre_mus == i.museo.nombre:
								esta_seleccionado = True
					if esta_seleccionado == False:
						museo_sel = Museo_Seleccionado(museo = museo,usuario = request.user,fecha = fecha)
						museo_sel.save()
				except ObjectDoesNotExist:
					return('')		
			elif key == 'Puntuar':
				nombre_mus = request.POST['Puntuar']
				museo_punt = Museo.objects.get(nombre= nombre_mus)
				museo_punt.puntuacion = museo_punt.puntuacion + 1 
				museo_punt.save()
		else:
			lista_comentarios = Comentarios.objects.all()
			muestra_comentarios = '<h4>Lista de Comentarios:</h4>'
			for comentario in lista_comentarios:
				if museo.nombre == comentario.museo.nombre:
					muestra_comentarios += comentario.txt
					muestra_comentarios += '<br>'
		pie_pagina = pagina_pie()
		c = Context({'form_logueado':form_logueado,'muestra_museos':muestra_museos,'form_comentario':form_comentario,'muestra_comentarios':muestra_comentarios,'puntuar':puntuar,'pie_pagina':pie_pagina})
		return HttpResponse(template.render(c))		
	except ObjectDoesNotExist:
		return HttpResponse("No existe ningún museos para ese id")
@csrf_exempt
def pagina_usuario(request,usuario):
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@,' + user +'<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/json"> Mi página en JSON</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a><br>'
	else:
		form_logueado = 'Para entrar al sitio vaya al '+'<a href="http://localhost:8000/">Inicio</a>'
	museos = Museo.objects.all()
	paginator = Paginator(museos,5)
	page = request.GET.get('page')
	try:
	 	seleccion = paginator.page(page)
	except PageNotAnInteger:
		seleccion = paginator.page(1)
	except EmptyPage:
		seleccion = paginator.page(paginator.num_pages)
	lista_museos = "<h4>Museos de Madrid que puede seleccionar:</h4><br>"
	for museo in seleccion:
		nombre_museo = museo.nombre
		lista_museos += '<a href="http://localhost:8000/museos/'+ str(museo.id_museo)+'">'+ nombre_museo +'</a>'
		lista_museos +=	'<form action="" method ="POST">'
		lista_museos += '<button type="submit" name="Seleccionar" value="'+nombre_museo+'">Seleccionar</button></form>'
	usuario_entra = User.objects.get(username = usuario)
	if request.method == 'POST':
		key = request.body.decode("utf-8").split('=')[0]
		if key == 'titulo':
			titulo = request.POST['titulo']
			try:
				usuario_bbdd = Cambio_Estilo.objects.get(usuario= usuario_entra)
				usuario_bbdd.titulo = titulo
				usuario_bbdd.save()
			except ObjectDoesNotExist:
				titulo = "Pagina de " + str(usuario_entra)
				not_exist = Cambio_Estilo(usuario =usuario_entra,titulo=titulo)
				not_exist.save()
		elif key == "Seleccionar":
			nombre_mus = request.POST['Seleccionar']
			fecha = datetime.datetime.today()
			lista_museos_seleccionados = Museo_Seleccionado.objects.all()
			try:
				museo = Museo.objects.get(nombre = nombre_mus)
				esta_seleccionado = False
				for i in lista_museos_seleccionados:
					if str(i.usuario) == str(usuario):
						if nombre_mus == i.museo.nombre:
							esta_seleccionado = True
				if esta_seleccionado == False:
					museo_sel = Museo_Seleccionado(museo = museo,usuario = usuario_entra,fecha = fecha)
					museo_sel.save()
			except ObjectDoesNotExist:
				return('')	
		elif key == 'letra':
			try:
				usuario_camb = Cambio_Estilo.objects.get(usuario = usuario_entra)
			except:
				not_user = Cambio_Estilo(usuario = usuario_entra)
				not_user.save()
				usuario_estilo = Cambio_Estilo.objects.get(usuario = usuario_entra)
			usuario_camb.tamaño = request.POST['letra']
			usuario_camb.color = request.POST['color']
			usuario_camb.save()
	lista_museos_sel = ''
	museos_seleccionados = Museo_Seleccionado.objects.filter(usuario = usuario_entra)
	paginator = Paginator(museos_seleccionados,5)
	page = request.GET.get('page')
	try:
	 	seleccionados = paginator.page(page)
	except PageNotAnInteger:
		seleccionados = paginator.page(1)
	except EmptyPage:
		seleccionados = paginator.page(paginator.num_pages)
	for i in seleccionados:
		lista_museos_sel += '<p><a href="'+ i.museo.content_url + '">'+'<h4>'+i.museo.nombre +'</h4></a></p><br>'
		lista_museos_sel += "Fecha de selección" + str(i.fecha) + '<br>'
		lista_museos_sel += 'Dirección:' + i.museo.nombre_via + ',' + str(i.museo.num)  + '<br>'
		lista_museos_sel += '<p><a href=http://localhost:8000/museos/'+ str(i.museo.id_museo)+ '>'+'Más Información</a></p><br>'
	
	if request.user.is_authenticated():
		username = str(request.user)
		if usuario == username:
			template = get_template("pagina_usuario.html")
			try:
				titulo_pagina = Cambio_Estilo.objects.get(usuario= usuario_entra).titulo
			except ObjectDoesNotExist:
				titulo_pagina = "Pagina personal de " + str(request.user)	
		pie_pagina = pagina_pie()
		c = Context({'lista_museos':lista_museos,'titulo_pagina':titulo_pagina,'form_logueado':form_logueado,'lista_museos_sel':lista_museos_sel,'seleccion':seleccion,'seleccionados':seleccionados,'pie_pagina':pie_pagina})
	else:
		template = get_template("pagina_publica.html")
		titulo_pagina = Cambio_Estilo.objects.get(usuario= usuario_entra).titulo
		pie_pagina = pagina_pie()
		c = Context({'titulo_pagina':titulo_pagina,'lista_museos_sel':lista_museos_sel,'seleccionados':seleccionados,'pie_pagina':pie_pagina})
	
	return HttpResponse(template.render(c))	
def pagina_xml(request,usuario):
	template = get_template('usuario_xml.xml')
	usuario_entra = User.objects.get(username = usuario)
	museos_seleccionados = Museo_Seleccionado.objects.filter(usuario = usuario_entra)
	cambio_estilos = Cambio_Estilo.objects.filter(usuario = usuario_entra)
	for j in cambio_estilos:
		titulo_pagina = j.titulo
	c = RequestContext(request,{'usuario':usuario,'titulo_pagina':titulo_pagina,'museos_seleccionados':museos_seleccionados})
	return HttpResponse(template.render(c),content_type="text/xml")	
def about(request):
	template = get_template('about.html')
	pie_pagina = pagina_pie()
	context = RequestContext(request,{'pie_pagina':pie_pagina})
	return HttpResponse(template.render(context))

def personalizar_css(request):
	if request.user.is_authenticated():
		usuario_entra = User.objects.get(username = request.user)
		letra =  Cambio_Estilo.objects.get(usuario = usuario_entra).tamaño +'px'
		color =  Cambio_Estilo.objects.get(usuario = usuario_entra).color
	else:
		letra = "12px";
		color = "#17202A";

	template = get_template('style.css')
	c = Context({'color':color,'letra':letra})
	return HttpResponse(template.render(c),content_type="text/css")
	
def pagina_principal_xml(request):
	template = get_template('pagina_principal.xml')
	museos = Museo.objects.all()
	lista_museos = museos.order_by('-num_comentario')[:5]
	c = RequestContext(request,{'lista_museos':lista_museos})
	return HttpResponse(template.render(c),content_type="text/xml")

def pagina_json(request,usuario):
	template = get_template('usuario_json.json')
	usuario_entra = User.objects.get(username = usuario)
	museos_seleccionados = Museo_Seleccionado.objects.filter(usuario = usuario_entra)
	cambio_estilos = Cambio_Estilo.objects.filter(usuario = usuario_entra)
	for j in cambio_estilos:
		titulo_pagina = j.titulo
	c = RequestContext(request,{'usuario':usuario,'titulo_pagina':titulo_pagina,'museos_seleccionados':museos_seleccionados})
	return HttpResponse(template.render(c),content_type="text/json")	

def pagina_principal_json(request):
	template = get_template('pagina_principal.json')
	museos = Museo.objects.all()
	lista_museos = museos.order_by('-num_comentario')[:5]
	c = RequestContext(request,{'lista_museos':lista_museos})
	return HttpResponse(template.render(c),content_type="text/json")

def canal_rss(request):
	template = get_template('canal_comentarios.rss')
	museos_comentarios = Comentarios.objects.all()
	c = RequestContext(request,{'museos_comentarios':museos_comentarios})
	return HttpResponse(template.render(c),content_type="text/rss+xml")

@csrf_exempt
def puntuar(request):
	template = get_template('pagina_puntuar.html')
	ranking = ''
	if request.user.is_authenticated():
		user = str(request.user)
		form_logueado = 'Bienvenid@,' + user +'<br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '"> Mi página</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/xml"> Mi página en XML</a><br>'
		form_logueado += '<a href="http://localhost:8000/'+ user + '/json"> Mi página en JSON</a><br>'
		form_logueado += '<a href="http://localhost:8000/logout">	Logout</a><br>'
	else:
		form_logueado = 'Para entrar al sitio vaya al '+'<a href="http://localhost:8000/">Inicio</a>'
	museos = Museo.objects.all()
	paginator = Paginator(museos,15)
	page = request.GET.get('page')
	try:
	 	seleccion = paginator.page(page)
	except PageNotAnInteger:
		seleccion = paginator.page(1)
	except EmptyPage:
		seleccion = paginator.page(paginator.num_pages)
	lista_museos_punt = "<h4>Museos de Madrid que puede seleccionar:</h4><br>"
	for museo in seleccion:
		nombre_museo = museo.nombre
		lista_museos_punt += '<a href="http://localhost:8000/museos/'+ str(museo.id_museo)+'">'+ nombre_museo +'</a><br>'
		lista_museos_punt +=	'<form action="" method ="POST">'
		lista_museos_punt += '<button type="submit" name="Puntuar" value="'+nombre_museo+'"><img src="/images/like.png"width="10"></button></form><br>'
	if request.method == 'POST':
		key = request.body.decode("utf-8").split('=')[0]
		if key == 'Puntuar':
			nombre_mus = request.POST['Puntuar']
			museo_punt = Museo.objects.get(nombre= nombre_mus)
			museo_punt.puntuacion = museo_punt.puntuacion + 1 
			museo_punt.save()
		ranking = '<h3>TOP 5 Museos<h3>'
		museo = Museo.objects.all()
		lista_ranking = museos.order_by('-puntuacion')[:5]
		for i in lista_ranking:
			ranking += '<a href="http://localhost:8000/museos/'+ str(i.id_museo)+'">'+ str(i.nombre) +'</a><br>'
			ranking += 'Puntuación: '+ str(i.puntuacion) +'<br>'
	else:
		ranking = '<h3>TOP 5 Museos<h3>'
		museo = Museo.objects.all()
		lista_ranking = museos.order_by('-puntuacion')[:5]
		for i in lista_ranking:
			ranking += '<a href="http://localhost:8000/museos/'+ str(i.id_museo)+'">'+ str(i.nombre) +'</a><br>'
			ranking += 'Puntuación: '+ str(i.puntuacion) +'<br>'
	pie_pagina = pagina_pie()
	c = Context({'form_logueado':form_logueado,'lista_museos_punt':lista_museos_punt,'seleccion':seleccion,'ranking':ranking,'pie_pagina':pie_pagina})
	return HttpResponse(template.render(c))
