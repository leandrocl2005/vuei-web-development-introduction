from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..models import Medicine

@require_http_methods(["GET", "POST"])
def list_medicines(request):
    if request.method == "POST":
        denominacao_generica = request.POST.get(
            'denominacao_generica'
        )
        medicines = Medicine.objects.filter(
            denominacao_generica=denominacao_generica
        )
        if medicines:
            context = {"medicines": medicines}
        else:
            context = {"search_message": "Medicamento não encontrado"}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
