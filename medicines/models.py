from django.db import models

class Medicine(models.Model):
    denominacao_generica = models.CharField(max_length=222)
    concentracao_composicao = models.CharField(max_length=222)
    forma_farmaceutica = models.CharField(max_length=222)
    codigo_atc = models.CharField(max_length=222)
    componente = models.CharField(max_length=222)
    
    def __str__(self):
        return self.denominacao_generica