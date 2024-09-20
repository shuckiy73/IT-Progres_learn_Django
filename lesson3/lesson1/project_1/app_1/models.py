from django.db import models


class Mebel(models.Model):
    link = models.TextField('Ссылка')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(
        verbose_name='Описание с куфара'
    )
    parse_datetime = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата прихода к нам'
    )

    def get_absolute_url(self):
        return self.link

    def __str__(self):
        return f'{self.price} | {self.description[:60]}'

    class Meta:
        verbose_name = 'Мебель'
        verbose_name_plural = 'Мебель'
        ordering = ['parse_datetime', '-price']
