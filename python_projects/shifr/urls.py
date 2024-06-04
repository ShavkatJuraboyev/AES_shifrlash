from django.urls import path
from shifr.views import home, shifrlash, deshifrlash, edit, delete
urlpatterns = [
    path('', home, name="home"),
    path('shifrlash/', shifrlash, name="shifrlash"),
    path('deshifrlash/', deshifrlash, name="deshifrlash"),
    path('edit/', edit, name="edit"),
    path('delete/', delete, name="delete"),
]