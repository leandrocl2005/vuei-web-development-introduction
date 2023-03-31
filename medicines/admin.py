from django.contrib import admin
from .models import Medicine

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'denominacao_generica', 'concentracao_composicao')
    
admin.site.register(Medicine, MedicineAdmin)
