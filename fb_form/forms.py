from django import forms

from .models import FbForm


class FbFormForm(forms.ModelForm):
    MSG_MIN_LEN = 10

    class Meta:
        model = FbForm
        fields = ['text', 'email_from', 'partner_name']
        labels = {
            'text': 'Имя сделки',
            'email_from': 'Почтовый ящик',
            'partner_name': 'Имя заказчика',
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < self.MSG_MIN_LEN:
            self.add_error('text', f'Текст должен быть минимум '
                                   f'{self.MSG_MIN_LEN} символов')
        return text
