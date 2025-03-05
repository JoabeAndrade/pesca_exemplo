from django.urls import path
from .views import uf_list, uf_detail

urlpatterns = [
    path('', uf_list),              # localhost:8000/municipios/
    path('<int:pk>/', uf_detail),   # localhost:8000/municipios/<id>/
]
