from django import forms

from .models import SiteParameter


class SiteParameterForm(forms.ModelForm):
    clear_image = forms.BooleanField(
        required=False,
        label="Eliminar imagen actual",
        help_text="Marca esto para volver a usar solo el valor de texto (por ejemplo la letra del icono).",
    )

    class Meta:
        model = SiteParameter
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ptype = self.instance.parameter_type
        if ptype == SiteParameter.ParameterType.TEXT:
            self.fields.pop("clear_image", None)
        else:
            self.fields["image"] = forms.ImageField(
                required=False,
                label="Imagen",
                help_text="Opcional. Si subes una imagen, se usará en lugar del texto donde aplique.",
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.parameter_type != SiteParameter.ParameterType.TEXT:
            image = self.cleaned_data.get("image")
            clear_image = self.cleaned_data.get("clear_image")
            if image:
                instance.image = image
            elif clear_image:
                if instance.pk and instance.image:
                    instance.image.delete(save=False)
                instance.image = None
        if commit:
            instance.save()
        return instance
