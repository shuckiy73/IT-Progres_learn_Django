from django.db import models


class Mebel(models.Model):
    link = models.TextField('Ссылка')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField('Описание')

    def __str__(self):
        return f'{self.price} | {self.description[:60]}'
