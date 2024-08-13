from django.contrib.auth.models import User
from testeo_app.models import Usuario, TipoUsuario, Region, Comuna, TipoInmueble, Inmueble
from baseModel import BaseModel as mb


def crear_tipo_usuario(nombre, descripcion=None):
    tipo_usuario = TipoUsuario(nombre=nombre, descripcion=descripcion)
    tipo_usuario.save()
    return tipo_usuario

def crear_usuario(username, ,password, nombre, apellido, tipo_usuario_id, telefono, rut, direccion=None):
    user = User.objects.create_user(username=username, password=password)
    tipo_usuario = TipoUsuario.objects.get(id=tipo_usuario_id)
    usuario = Usuario.objects.create(
        user=user,
        rut=rut,
        tipo_usuario=tipo_usuario,
        direccion=direccion,
        telefono=telefono,
        nombre=nombre,
        apellido=apellido
    )
    return usuario

def crear_tipo_inmueble(nombre, descripcion=None):
    tipo_inmueble = TipoInmueble(nombre=nombre, descripcion=descripcion)
    tipo_inmueble.save()
    return tipo_inmueble

def crear_inmueble(nombre, descripcion, direccion, depto, m2_construidos, m2_totales, estacionamientos, habitaciones, banios, precio, tipo_inmueble_id, region_id, comuna_id):
    tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)
    region = Region.objects.get(id=region_id)
    comuna = Comuna.objects.get(id=comuna_id)
    inmueble = Inmueble(
        nombre=nombre,
        descripcion=descripcion,
        direccion=direccion,
        depto=depto,
        m2_construidos=m2_construidos,
        m2_totales=m2_totales,
        estacionamientos=estacionamientos,
        habitaciones=habitaciones,
        banios=banios,
        precio=precio,
        tipo_inmueble=tipo_inmueble,
        region=region,
        comuna=comuna)
    inmueble.save()
    return inmueble

def listar_tipos_inmuebles():
    return TipoInmueble.objects.all()

def listar_inmuebles():
    return Inmueble.objects.all()

def actualizar_inmueble(id, **kwargs):
    Inmueble.objects.filter(id=id).update(**kwargs)
    inmueble_actualizado = Inmueble.objects.get(id=id)
    return inmueble_actualizado

def eliminar_inmueble(id):
    inmueble = Inmueble.objects.get(id=id)
    inmueble.delete()
    return None

"""
def sql_obtener_todos_inmuebles():
    sql = "select nombre, arrendada from testadl_inmueble"
    parametros = None
    inmuebles= list(bm.execute(sql,parametros))
    for inmu in inmuebles:
        print(inmu)
        return inmuebles

def obtener_todos_inmuebles():
    return Inmueble.objects.all()
    
def raw_obtener_todos_inmuebles():
    sql = "select nombre, arrendada from testadl_inmueble"
    query = Inmueble.objects.raw(sql)
    for p in query:
        print(p.nombre)
        print(p.arrendada)"""