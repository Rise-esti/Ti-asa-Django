from django.urls import path
from . import views

urlpatterns = [
    path('create_account', views.create_account, name = 'create_account'),
    path('connect', views.connect, name ='connect'),
    path('deconnexion', views.deconnect, name = 'deconnect'),
    path('index', views.index, name='homepage'),
    path('profil-edit-info', views.profilEdit, name='profil-edit-info'),
    path('profil-edit-info-action', views.infoProfilEdit, name='profil-edit-info-action'),
    path('profil-info/<username>', views.profilInfo, name='profil-info'),
    path('get-image', views.getImage, name='getimage'),
]