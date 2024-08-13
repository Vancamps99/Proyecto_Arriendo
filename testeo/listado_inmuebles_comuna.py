import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testeo.settings')
django.setup()

from testeo_app.models import Inmueble

def listar_inmuebles_por_comuna():
    inmuebles = Inmueble.objects.filter(arrendado=False).values('comuna__nombre', 'nombre', 'descripcion')
    with open('inmuebles_por_comuna.txt', 'w', encoding='utf-8') as file:
        current_comuna = None
        for inmueble in inmuebles:
            comuna = inmueble['comuna__nombre']
            if comuna != current_comuna:
                if current_comuna is not None:
                    file.write('\n') 
                file.write(f'\nComuna: {comuna}\n')
                current_comuna = comuna
            file.write(f"Nombre: {inmueble['nombre']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write('---\n')

if __name__ == '__main__':
    listar_inmuebles_por_comuna()
