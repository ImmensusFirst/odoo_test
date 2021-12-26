from django.db import models


class FbForm(models.Model):
    text = models.CharField('имя сделки', max_length=250,
                            help_text='Введите имя сделки')
    email_from = models.EmailField(help_text='Укажите существующий email')
    partner_name = models.CharField('имя заказчика', max_length=250,
                                    help_text='Введите имя заказчика')

    def __str__(self):
        return self.partner_name
