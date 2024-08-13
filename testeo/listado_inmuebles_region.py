import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testeo.settings')
django.setup()

from testeo_app.models import Inmueble

def listar_inmuebles_por_region():
    inmuebles = Inmueble.objects.filter(arrendado=False).values('region__nombre', 'nombre', 'descripcion')
    
    with open('inmuebles_por_region.txt', 'w', encoding='utf-8') as file:  # Cambié el nombre del archivo a "inmuebles_por_region.txt"
        current_region = None
        for inmueble in inmuebles:
            region = inmueble['region__nombre']
            if region != current_region:
                if current_region is not None:
                    file.write('\n')  # Añadir una línea en blanco entre regiones
                file.write(f'\nRegión: {region}\n')
                current_region = region
            file.write(f"Nombre: {inmueble['nombre']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write('---\n')

if __name__ == '__main__':
    listar_inmuebles_por_region()
