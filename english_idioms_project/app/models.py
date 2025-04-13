from django.db import models

class Idiom(models.Model):
    LEVEL_CHOICES = [
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    
    phrase = models.CharField(max_length=200, unique=True, verbose_name="Идиома")
    definition = models.TextField(verbose_name="Определение на английском")
    example = models.TextField(verbose_name="Пример употребления")
    translation = models.TextField(verbose_name="Перевод на русский", blank=True)
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default='B2',
        verbose_name="Уровень"
    )
    
    def __str__(self):
        return self.phrase
