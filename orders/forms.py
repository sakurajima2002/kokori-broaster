from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'hidden',
                'id': 'rating-score',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-100 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 transition-colors text-sm text-gray-700 resize-none',
                'rows': 4,
                'placeholder': '¿Qué te pareció tu pedido? (Opcional)'
            }),
        }
