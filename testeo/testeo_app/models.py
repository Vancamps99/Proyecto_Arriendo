from django.db import models
from django.contrib.auth.models import User



#NULL=FALSE ---->DEBE TENER SIEMPRE UN VALOR // BLANK=FALSE ----> SE USA EN FORMULARIOS E INDICA QUE NO DEBE ESTAR EL CAMPO VACIO
class Region(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return f'{self.id} región - {self.nombre}'

class Comuna(models.Model):
    nombre = models.CharField(max_length=70, null=False, blank=False)
    region = models.ForeignKey(Region, null=False, blank=False, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id} comuna "{self.nombre}" - Región {self.region.nombre} ({self.region.id})'

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=70, null=False, blank=False)
    descripcion = models.CharField(max_length=40, null=True, blank=True)
    def __str__(self):
        return f'({self.id})-({self.nombre})'

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=9)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.id} {self.user.username} - {self.user.email}'

class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f" {self.nombre}"
    
class Inmueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(null=False, blank=False)
    direccion = models.TextField(max_length=255)
    depto = models.CharField(max_length=20, blank=True)
    m2_construidos = models.FloatField(null=False, blank=False)
    m2_totales = models.FloatField(null=False, blank=False)
    estacionamientos = models.IntegerField(null=False, blank=False)
    habitaciones = models.IntegerField(null=False, blank=False)
    banios = models.IntegerField(null=False, blank=False)
    precio = models.FloatField(null=False, blank=False)
    arrendado = models.BooleanField(null=False, default=False)
    tipo_inmueble = models.ForeignKey(TipoInmueble, null=False, blank=False, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=False, blank=False, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, null=False, blank=False, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(Usuario, related_name='inmuebles', blank=True)  # Asegúrate de que sea opcional

    def __str__(self):
        usuarios_str = ', '.join([usuario.user.username for usuario in self.usuarios.all()])
        return (f'{self.id} - Propiedad: {self.nombre} - Región: {self.region.nombre} - '
                f'Comuna: {self.comuna.nombre} - Usuarios: {usuarios_str}')
    
