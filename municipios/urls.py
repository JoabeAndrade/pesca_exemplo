from django.urls import path
from .views import uf_list, uf_detail, municipio_list, municipio_detail

urlpatterns = [
    path('', municipio_list),               # localhost:8000/municipios/
    path('<int:pk>/', municipio_detail),    # localhost:8000/municipios/<id>/
    path('estados/', uf_list),              # localhost:8000/municipios/estados/
    path('estados/<int:pk>/', uf_detail),   # localhost:8000/municipios/estados/<id>/
]
