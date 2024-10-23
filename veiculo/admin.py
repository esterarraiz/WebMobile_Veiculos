from django.contrib import admin
from veiculo.models import Veiculo

# Register your models here.
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['id', 'marca', 'modelo','ano', 'cor', 'combustivel','foto']
    search_fields = ['modelo']

admin.site.register(Veiculo,VeiculoAdmin)