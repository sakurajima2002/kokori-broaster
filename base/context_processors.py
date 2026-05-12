from .models import SiteParameter
from .parameters_data import DEFAULT_PARAMETERS

def site_config(request):
    """
    Context processor para inyectar los parámetros globales en todas las plantillas.
    Combina los valores de la base de datos con los valores por defecto.
    Uso: {{ site_config.COMPANY_NAME }}
    """
    # 1. Cargar todos los parámetros de la DB
    params = SiteParameter.objects.all()
    db_config = {p.key: p for p in params}
    
    config = {}
    config_objs = {}

    # 2. Iterar sobre la definición de parámetros por defecto
    for param_def in DEFAULT_PARAMETERS:
        key = param_def['key']
        
        # Si existe en DB, usar el valor de DB
        if key in db_config:
            p = db_config[key]
            if p.image:
                config[key] = p.image.url
            else:
                config[key] = p.value
            config_objs[key] = p
        else:
            # Si no existe en DB, usar el valor por defecto
            if 'image' in param_def and param_def['image']:
                # Nota: Las imágenes por defecto deben estar en /media/
                config[key] = f"/media/{param_def['image']}"
            else:
                config[key] = param_def.get('value', '')
            
            # Crear un objeto ficticio para mantener compatibilidad si es necesario
            config_objs[key] = param_def

    return {
        'site_config': config,
        'site_config_objs': config_objs
    }
