from django.urls import path
from .views import uf_list, uf_detail, municipio_list, municipio_detail, area_pesca_list, area_pesca_detail, arte_pesca_list, arte_pesca_detail

app_name = 'pescadores'

urlpatterns = [
    path('municipios/', municipio_list, name='municipio_list'),               
    path('municipios/<int:pk>/', municipio_detail, name='municipio_detail'),   
    path('estados/', uf_list, name='uf_list'),              
    path('estados/<int:pk>/', uf_detail, name='uf_detail'),   
    path('areapesca/', area_pesca_list, name='area_pesca_list'),
    path('areapesca/<int:pk>/', area_pesca_detail, name='area_pesca_detail'),
    path('artepesca/', arte_pesca_list, name='arte_pesca_list'),
    path('artepesca/<int:pk>/', arte_pesca_detail, name='area_pesca_detail'),
]
