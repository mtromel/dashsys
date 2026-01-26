from django.shortcuts import render
from .models import Maquina

def dashboard_pcp(request):
    # Buscamos todas as máquinas, trazendo junto o apontamento para ganhar performance
    maquinas = Maquina.objects.filter(exibir_no_dashboard=True).prefetch_related('apontamento').all().order_by('data_entrega')
    
    return render(request, 'dashboard.html', {'maquinas': maquinas})
