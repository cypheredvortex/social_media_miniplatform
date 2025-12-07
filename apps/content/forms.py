from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    media_file = forms.FileField(required=False, label='Media File')
    
    class Meta:
        model = Content
        fields = ['text', 'visibility', 'media_url']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full border rounded-lg p-2',
                'placeholder': 'What\'s on your mind?'
            }),
            'visibility': forms.Select(attrs={
                'class': 'w-full border rounded-lg p-2'
            }),
            'media_url': forms.URLInput(attrs={
                'class': 'w-full border rounded-lg p-2',
                'placeholder': 'Optional media URL'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media_file'].widget.attrs.update({
            'class': 'w-full border rounded-lg p-2'
        })