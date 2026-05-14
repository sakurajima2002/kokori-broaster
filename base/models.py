from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteParameter(models.Model):
    """Modelo para almacenar parámetros globales del sitio."""

    class ParameterType(models.TextChoices):
        TEXT = "TEXT", _("Texto")
        ICON = "ICON", _("Icono (letra o imagen)")
        IMAGE = "IMAGE", _("Imagen")

    key = models.SlugField(
        unique=True, 
        max_length=100, 
        verbose_name="Clave",
        help_text="Identificador interno del parámetro. No debe cambiarse."
    )
    label = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        help_text="Nombre legible para el administrador."
    )
    value = models.TextField(
        blank=True, 
        verbose_name="Valor",
        help_text="El valor de texto del parámetro."
    )
    image = models.ImageField(
        upload_to='settings/', 
        blank=True, 
        null=True, 
        verbose_name="Imagen",
        help_text="Opcional: Si el parámetro es una imagen (ej. logo)."
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Explicación de para qué sirve este parámetro."
    )
    parameter_type = models.CharField(
        max_length=10,
        choices=ParameterType.choices,
        default=ParameterType.TEXT,
        verbose_name="Tipo",
        help_text="Texto: solo valor. Icono: letra en valor y/o imagen (la imagen tiene prioridad al mostrar). Imagen: principalmente archivo de imagen.",
    )

    class Meta:
        verbose_name = "Parámetro Global"
        verbose_name_plural = "Parámetros Globales"
        ordering = ['label']

    def __str__(self):
        return self.label
