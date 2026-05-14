from django.core.management.base import BaseCommand

from base.models import SiteParameter
from base.parameters_data import DEFAULT_PARAMETERS


class Command(BaseCommand):
    help = (
        "Crea en la base de datos los SiteParameter que falten según DEFAULT_PARAMETERS. "
        "Es idempotente: no modifica filas ya existentes (no pisa valores editados en staff)."
    )

    def handle(self, *args, **options):
        valid_types = set(SiteParameter.ParameterType.values)
        created = 0
        for row in DEFAULT_PARAMETERS:
            key = row["key"]
            ptype = row.get("parameter_type") or SiteParameter.ParameterType.TEXT
            if ptype not in valid_types:
                ptype = SiteParameter.ParameterType.TEXT

            defaults = {
                "label": row["label"],
                "value": row.get("value") or "",
                "description": row.get("description", ""),
                "parameter_type": ptype,
            }
            if row.get("image"):
                defaults["image"] = row["image"]

            obj, was_created = SiteParameter.objects.get_or_create(
                key=key,
                defaults=defaults,
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Parámetro creado: {key}"))
            else:
                self.stdout.write(f"Parámetro ya existente (sin cambios): {key}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo. Parámetros nuevos en esta pasada: {created}."
            )
        )
