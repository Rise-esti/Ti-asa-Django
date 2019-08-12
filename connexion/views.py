from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profil, Formation
import random, datetime, time, os

# Create your views here.
def getImage(request, ino):
    upload_file(request, ino)
    return HttpResponseRedirect(reverse('profil-info', args=[request.user.username]))


def upload_file(req, ino):
    if ino == 'profil':
        with open('connexion/static/connexion/images/Picture/profil/'+str(req.user.id)+'_'+str(time.time())+'.png', 'wb+') as destination:
            for chunk in req.FILES.get('pdp-file').chunks():
                destination.write(chunk)
        Profil.objects.filter(username_id=req.user.id).update(profilpic='connexion/images/Picture/profil/'+str(req.user.id)+'_'+str(time.time())+'.png')

    elif  ino == 'cover':
        with open('connexion/static/connexion/images/Picture/cover/'+str(req.user.id)+'_'+str(time.time())+'.png', 'wb+') as destination:
            for chunk in req.FILES.get('pdc-file').chunks():
                destination.write(chunk)
        Profil.objects.filter(username_id=req.user.id).update(coverpic='connexion/images/Picture/cover/'+str(req.user.id)+'_'+str(time.time())+'.png')


    
def connect(request):
    if request.method == "POST":
        email = request.POST.get('mail').lower()
        password = request.POST.get('password')
        if '@' in email:
            try:
                username = User.objects.get(email=email).username
            except:
                return redirect(index)
        else:
            username = email
        user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
        if user:  # Si l'objet renvoyé n'est pas None
            login(request, user)  # nous connectons l'utilisateur
            return redirect(home)
        else: # sinon une erreur sera affichée
            return render(request, 'connexion/index.html', {'error': True})
    else:
        return redirect(index)
    

def deconnect(request):
    logout(request)
    return redirect(home)


def create_account(request):
    if (request.POST.get('password') == (request.POST.get('password_conf'))):
        username = request.POST.get('nom').lower()+str(int(time.time()))
        user = User.objects.create_user(username=username, email=request.POST.get('mail').strip(), password=request.POST.get('password'), first_name=request.POST.get('nom').upper().strip(), last_name=request.POST.get('prenom').capitalize().strip())
        user.save()
        nb = User.objects.get(username=username).id
        User.objects.filter(username=username).update(username=request.POST.get('prenom').lower().split(' ')[0]+str(nb))
        username = User.objects.get(id=nb).username
        Profil(username=User.objects.get(username=username)).save()

    return redirect(index)


def index(request):
    if request.user.is_authenticated:
        return redirect(home)
    return render(request, 'connexion/index.html', {'error': False})


@login_required
def home(request):
    info_user = Profil.objects.get(username_id=request.user.id)                 
    return render(request, 'connexion/home.html', locals())


@login_required
def profilEdit(request):
    profil = Profil.objects.filter(username_id=request.user.id)[0]
    user = User.objects.filter(id=request.user.id)[0]
    day, month, year = [], [], []
    # jour 
    for y in range(1, 32):
        day.append(y)
    # mois
    for y in range(1, 12):
        month.append(y)
    # annee
    for y in range(1970, 2005):
        year.append(y)

    if profil.phone is None or profil.phone == '':
        phone ='+261'
    else:
        phone = profil.phone

    try:
        profil.jour = profil.dateNaissance.strftime("%d")
        profil.moisl, profil.moisn = profil.dateNaissance.strftime("%b"), profil.dateNaissance.strftime("%m")
        profil.annee = profil.dateNaissance.strftime("%Y")
    except:
        profil.jour = 'Jour'
        profil.moisl, profil.moisn = 'Mois', 'Mois'
        profil.annee = 'Annee'
    
    if profil.adresse is None:
        profil.adresse = ''
    
    if profil.biographie is None:
        profil.biographie = ''
    
    profil.prenom = user.last_name.split(' ')[0]

    context = {'user_viewed': user, 'years': year, 'days': day,
    'info_user_viewed': profil,
    'info_user':profil,
    'phone':phone,
    'moded':'active'
    }
    return render(request, 'connexion/profil/edit-profile.html', context)


@login_required
def formationEdit(request, id):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded ='active'
    years = [x for x in range(int(datetime.datetime.today().strftime('%Y')) + 1, 1980, -1)]

    user_formation = Formation.objects.get(pk=id)

    return render(request, 'connexion/profil/formation-profil-edit.html', locals())


@login_required
def formationAdd(request):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    try:
        formation_user_viewed = Profil.objects.filter(username_id=user_viewed.id)
    except:
        pass

    moded ='active'
    years = [x for x in range(int(datetime.datetime.today().strftime('%Y')) + 1, 1980, -1)]

    return render(request, 'connexion/profil/formation-profil-add.html', locals())
    

def infoProfilEdit(request):
    User.objects.filter(id=request.user.id).update(username=request.POST.get('username'),
    first_name=request.POST.get('nom').capitalize(),
    last_name=request.POST.get('prenom').capitalize(),
    email=request.POST.get('mail').lower()
    )
    phone = request.POST.get('phone')
    if phone == '+261':
        phone = ''
    try:
        user = Profil.objects.filter(username_id=request.user.id)
    except:
        pass
    else:
        try:
            dateNaissance=datetime.date(int(request.POST.get('annee')), int(request.POST.get('mois')), int(request.POST.get('jour'))).strftime('%Y-%m-%d')
        except:
            dateNaissance = None
        finally:
            user.update(phone=phone,
            adresse = request.POST.get('adresse'),
            biographie = request.POST.get('bio'),
            sexe = request.POST.get('radio'),
            ville = request.POST.get('ville'),
            dateNaissance=dateNaissance,
            poste=request.POST.get('poste'),
            lieu=request.POST.get('lieu')
            )
    return redirect(profilInfo, username=request.user.username)


def infoFormationEdit(request):
    if request.POST.get('lieu') != '':
        try:
            int(request.POST.get('Annee_deb'))
        except:
            return HttpResponse("Il faut entrer l'annee de debut")
        else:
            Formation.objects.filter(pk=request.POST.get('id')).update(lieu = request.POST.get('lieu'),
            mois_debut = request.POST.get('Mois_deb'),
            annee_debut = request.POST.get('Annee_deb'),
            mois_fin = request.POST.get('Mois_fin'),
            annee_fin = request.POST.get('Annee_fin'),
            filiere = request.POST.get('filiere'),
            niveau = request.POST.get('niveau'),
            obtention = request.POST.get('obtention')
            )
            return redirect(formationInfo, username=request.user.username)
    else:
        return HttpResponse("Il faut entrer le lieu du formation")

    
def infoFormationAdd(request):
    if request.POST.get('lieu') != '':
        try:
            int(request.POST.get('Annee_deb'))
        except:
            return HttpResponse("Il faut entrer l'annee de debut")
        else:
            Formation(username_id=request.user.id,
            lieu = request.POST.get('lieu'),
            mois_debut = request.POST.get('Mois_deb'),
            annee_debut = request.POST.get('Annee_deb'),
            mois_fin = request.POST.get('Mois_fin'),
            annee_fin = request.POST.get('Annee_fin'),
            filiere = request.POST.get('filiere'),
            niveau = request.POST.get('niveau'),
            obtention = request.POST.get('obtention')
            ).save()
            return redirect(formationInfo, username=request.user.username)
    else:
        return HttpResponse("Il faut entrer le lieu du formation")
    return redirect(formationInfo, username=request.user.username)


@login_required
def profilInfo(request, username):
    user_viewed = get_object_or_404(User, username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    apropos ='active'
    try:
        info_user_viewed.dateNaissance = info_user_viewed.dateNaissance.strftime('%d %m %Y')
    except:
        pass
    return render(request, 'connexion/profil/info-profil.html', locals())


@login_required
def formationInfo(request, username):
    user_viewed = get_object_or_404(User, username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    users_formation = Formation.objects.filter(username_id=user_viewed.id).order_by('-annee_debut').all()
    formation ='active'
    if user_viewed.id == request.user.id:
        if len(users_formation) ==0:
            return redirect(formationAdd)
    return render(request, 'connexion/profil/formation-profil.html', locals())


def formationDelete(request, id):
    Formation.objects.filter(pk=id).delete()
    return redirect(formationInfo, request.user.username)