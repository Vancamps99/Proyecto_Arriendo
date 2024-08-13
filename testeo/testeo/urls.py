"""
URL configuration for testeo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from testeo_app.views import  registro,index,listar_propiedades,ajax_load_comunas  ,editar_perfil  ,perfil_usuario,crear_inmueble,editar_inmueble,listar_inmuebles,acceso_denegado,eliminar_inmueble
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('inmuebles/', listar_propiedades, name='propiedades'),
    path('ajax/load-comunas/', ajax_load_comunas, name='ajax_load_comunas'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('perfil/', perfil_usuario, name='perfil'),
    path('registro/', registro, name='registro'),  # Ruta para el registro de usuarios
    path('inmuebles/crear/', crear_inmueble, name='crear_inmueble'),
    path('acceso-denegado/', acceso_denegado, name='acceso_denegado'),
    path('inmuebles/editar/<int:inmueble_id>/', editar_inmueble, name='editar_inmueble'),
    path('inmuebles/eliminar/<int:inmueble_id>/', eliminar_inmueble, name='eliminar_inmueble'),
    path('mis-propiedades/', listar_inmuebles, name='listar_inmuebles'),

]
 
