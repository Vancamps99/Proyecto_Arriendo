from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login

from .models import Inmueble, Region, Comuna, TipoInmueble ,Usuario,TipoUsuario
from django.contrib.auth.decorators import login_required
from .forms import Editar_Perfil
from .forms import PropertyFilterForm,RegistroUsuarioForm,UsuarioForm,InmuebleForm

#from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


"""Registro"""
def registro(request):
    if request.method == 'POST':
        user_form = RegistroUsuarioForm(request.POST)
        usuario_form = UsuarioForm(request.POST)
        
        if user_form.is_valid() and usuario_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            return redirect('login')  # Redirige al usuario a la página de inicio de sesión

    else:
        user_form = RegistroUsuarioForm()
        usuario_form = UsuarioForm()

    return render(request, 'registro.html', {'user_form': user_form, 'usuario_form': usuario_form})


"""USUARIO"""

@login_required
def perfil_usuario(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        # Si no existe el objeto Usuario, redirige a la vista de edición de perfil para crearlo
        return redirect('editar_perfil')
    return render(request, 'perfil_usuario.html', {'usuario': usuario})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = Editar_Perfil(request.POST, instance=request.user.usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil después de guardar
    else:
        form = Editar_Perfil(instance=request.user.usuario)
    
    return render(request, 'editar_perfil.html', {'form': form})

"""registro propiedades"""
def listar_propiedades(request):
    form = PropertyFilterForm(request.GET or None)
    inmuebles = Inmueble.objects.all()

    if form.is_valid():
        region = form.cleaned_data.get('region')
        comuna = form.cleaned_data.get('comuna')
        tipo_inmueble = form.cleaned_data.get('tipo_inmueble')
        arrendado = form.cleaned_data.get('arrendado')

        if region:
            inmuebles = inmuebles.filter(region=region)
        if comuna:
            inmuebles = inmuebles.filter(comuna=comuna)
        if tipo_inmueble:
            inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
        if arrendado:
            inmuebles = inmuebles.filter(arrendado=(arrendado == 'True'))

    return render(request, 'lista_propiedades.html', {'form': form, 'inmuebles': inmuebles})


"""PROPIEDADES DEL USUARIO"""
@login_required
def crear_inmueble(request):
    usuario = request.user.usuario
    if usuario.tipo_usuario.nombre != 'Arrendador':
        return redirect('acceso_denegado')

    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.save()
            form.save_m2m()  # Guarda las relaciones ManyToMany
            inmueble.usuarios.add(usuario)  # Asociar el inmueble con el usuario
            return redirect('listar_inmuebles')
    else:
        form = InmuebleForm()
    
    return render(request, 'crear_inmueble.html', {'form': form})

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')


@login_required
def editar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    usuario = request.user.usuario

    # Verificar si el usuario es el propietario del inmueble
    if usuario.tipo_usuario.nombre != 'Arrendador' or inmueble not in usuario.inmuebles.all():
        return redirect('acceso_denegado')

    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.save()  # Guardar el inmueble
            form.save_m2m()  # Guardar las relaciones ManyToMany
            
            # Asegurarse de que el inmueble siga asociado con el usuario
            if usuario not in inmueble.usuarios.all():
                inmueble.usuarios.add(usuario)
                
            return redirect('listar_inmuebles')
    else:
        form = InmuebleForm(instance=inmueble)
    
    return render(request, 'editar_inmueble.html', {'form': form})

@login_required
def eliminar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    
    if request.method == 'POST':
        inmueble.delete()
        return redirect('listar_inmuebles')  # Redirige a la lista de inmuebles después de eliminar
    
    return render(request, 'confirmar_eliminacion.html', {'inmueble': inmueble})

@login_required
def listar_inmuebles(request):
    usuario = request.user.usuario

    if usuario.tipo_usuario.nombre == 'Arrendador':
        # Mostrar inmuebles asociados al usuario tipo 'Arrendador'
        inmuebles = Inmueble.objects.filter(usuarios=usuario)
    else:
        inmuebles = None

    return render(request, 'listar_inmuebles.html', {'inmuebles': inmuebles})

"""CARGAR COMUNAS"""
def ajax_load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return render(request, 'comuna_dropdown_list_options.html', {'comunas': comunas})

def index(request):
    inmuebles = Inmueble.objects.all()
    context = {'inmuebles': inmuebles}
    return render(request, 'index.html', context)

def home(request):
    return render(request, 'base.html')


