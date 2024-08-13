from django.contrib import admin
from .models import Region, Comuna, TipoUsuario, Usuario, TipoInmueble,Inmueble

# Register your models here.
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(TipoInmueble)
admin.site.register(Inmueble)

