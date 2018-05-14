"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from MuseosApp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.pagina_principal, name = "Página principal de la práctica"),
    url(r'museos$',views.pagina_museos,name = "Página con todos los museos"),
    url(r'^museos/(.*)',views.pagina_museo,name = "Página de un museo en la aplicación"),
    url(r'(.*)/$',views.pagina_usuario,name = "Página personal del usuario"),
    url(r'^(.*)/xml$',views.pagina_xml,name = "Canal XML para los museos seleccionados por ese usuario"),
    url(r'^login',views.login_user,name = "Login de usuarios"),
    url(r'^logout',views.logout_user),
#    url(r'about$',views.about,name = "Información autoría de la práctica explicando el funcionamiento"),
    url(r'^cargar_datos$',views.cargar_datos, name = "Página donde se cargan los datos"),
]
