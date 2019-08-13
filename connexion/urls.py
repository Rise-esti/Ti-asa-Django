from django.urls import path
from . import views

urlpatterns = [
    path('create_account', views.create_account, name = 'create_account'),
    path('connect', views.connect, name ='connect'),
    path('deconnexion', views.deconnect, name = 'deconnect'),

    path('index', views.index, name='homepage'),

    path('profil-edit-info', views.profilEdit, name='profil-edit-info'),
    path('formation-info-edit/<int:id>', views.formationEdit, name='formation-info-edit'),
    path('formation-info-add', views.formationAdd, name='formation-info-add'),
    path('competence-info-add', views.competenceAdd, name='competence-info-add'),
    path('formation-info-delete/<id>', views.formationDelete, name='formation-info-delete'),
    path('competence-info-delete/<id>', views.competenceDelete, name='competence-info-delete'),
    path('competence-info-edit/<int:id>', views.competenceEdit, name='competence-info-edit'),

    path('profil-edit-info-action', views.infoProfilEdit, name='profil-edit-info-action'),
    path('formation-info-edit-action', views.infoFormationEdit, name='formation-info-edit-action'),
    path('formation-info-add-action', views.infoFormationAdd, name='formation-info-add-action'),
    path('competence-info-add-action', views.infoCompetenceAdd, name='competence-info-add-action'),
    path('competence-info-edit-action', views.infoCompetenceEdit, name='competence-info-edit-action'),
    

    path('profil-info/<username>', views.profilInfo, name='profil-info'),
    path('formation-info/<username>', views.formationInfo, name='formation-info'),
    path('competence-info/<username>', views.competenceInfo, name='competence-info'),

    path('get-image/<ino>', views.getImage, name='getimage'),
]