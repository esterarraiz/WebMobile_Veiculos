from django.urls import path
from veiculo.views import ListarVeiculos, FotoVeiculo, CriarVeiculo, EditarVeiculo, DeletarVeiculo, APIListarVeiculos

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculo.as_view(), name = 'criar-veiculos'),
    path('<int:pk>/', EditarVeiculo.as_view(), name = 'editar-veiculos'),
    path('deletar/<int:pk>/', DeletarVeiculo.as_view(), name = 'deletar-veiculos'),
    path('foto/<str:arquivo>/', FotoVeiculo.as_view(), name='foto-veiculo'),
    path('api/', APIListarVeiculos.as_view(),name='api-listar-veiculos')
]