from django.urls import path
from veiculo.views import ListarVeiculos, FotoVeiculo, CriarVeiculo


urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculo.as_view(), name='criar-veiculos'),
    path('foto/<str:arquivo>/', FotoVeiculo.as_view(), name='foto-veiculos')

]