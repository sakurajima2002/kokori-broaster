from .models import SiteParameter
from .parameters_data import DEFAULT_PARAMETERS

ICON_KEY = "COMPANY_ICON_LETTER"


def _default_param_by_key():
    return {p["key"]: p for p in DEFAULT_PARAMETERS}


def _config_value_for_row(ptype, value, has_image, image_url):
    """Valor expuesto en site_config[key] según el tipo de parámetro."""
    if ptype == SiteParameter.ParameterType.TEXT:
        return value or ""
    if ptype == SiteParameter.ParameterType.IMAGE:
        if has_image and image_url:
            return image_url
        return value or ""
    if ptype == SiteParameter.ParameterType.ICON:
        return value or ""
    return value or ""


def site_config(request):
    """
    Context processor para inyectar los parámetros globales en todas las plantillas.
    Combina los valores de la base de datos con los valores por defecto.
    Uso: {{ site_config.COMPANY_NAME }}
    Para el icono de marca (tipo ICON): {{ company_brand_icon }} e includes/company_brand_icon.html
    """
    params = SiteParameter.objects.all()
    db_config = {p.key: p for p in params}
    defaults_by_key = _default_param_by_key()

    config = {}
    config_objs = {}

    for param_def in DEFAULT_PARAMETERS:
        key = param_def["key"]
        default_type = param_def.get(
            "parameter_type", SiteParameter.ParameterType.TEXT
        )

        if key in db_config:
            p = db_config[key]
            ptype = p.parameter_type
            value = p.value or ""
            has_image = bool(p.image)
            image_url = p.image.url if p.image else None
        else:
            p = None
            ptype = default_type
            value = param_def.get("value", "") or ""
            raw_img = param_def.get("image") or ""
            has_image = bool(raw_img)
            image_url = f"/media/{raw_img}" if raw_img else None

        config[key] = _config_value_for_row(ptype, value, has_image, image_url)
        config_objs[key] = p if key in db_config else param_def

    company_brand_icon = _build_company_brand_icon(
        db_config, defaults_by_key[ICON_KEY]
    )

    return {
        "site_config": config,
        "site_config_objs": config_objs,
        "company_brand_icon": company_brand_icon,
    }


def _build_company_brand_icon(db_config, param_def):
    """Solo aplica lógica ICON (imagen prioritaria sobre la letra)."""
    default_type = param_def.get(
        "parameter_type", SiteParameter.ParameterType.TEXT
    )

    if ICON_KEY in db_config:
        p = db_config[ICON_KEY]
        ptype = p.parameter_type
        letter = (p.value or "").strip() or "K"
        has_image = bool(p.image)
        image_url = p.image.url if p.image else ""
    else:
        ptype = default_type
        letter = (param_def.get("value") or "").strip() or "K"
        raw_img = param_def.get("image") or ""
        has_image = bool(raw_img)
        image_url = f"/media/{raw_img}" if raw_img else ""

    if ptype != SiteParameter.ParameterType.ICON:
        return {
            "has_image": False,
            "image_url": "",
            "letter": letter,
        }

    return {
        "has_image": has_image,
        "image_url": image_url or "",
        "letter": letter,
    }
