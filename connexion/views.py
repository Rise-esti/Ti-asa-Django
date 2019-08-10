from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profil
import random, datetime, time

# Create your views here.

    
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


def apropos(request, username):
    nbr = random.choice((2, 1, 1, 3, 1, 1, 4, 5, 1))
    p = Personne.objects.get(username=username)
    couleurs = {
    'FF0000':'rouge', 
    'ED7F10':'orange', 
    'FFFF00':'jaune', 
    '00FF00':'vert', 
    '0000FF':'bleu', 
    '4B0082':'indigo', 
    '660099':'violet',
    }
    return render(request, 'connexion/apropos.html', {'nbr': nbr, 'prenom': p.prenom, 'nom': p.nom, 'couleurs': couleurs})


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
    return render(request, 'connexion/home.html', {'info_user': info_user})


@login_required
def profilEdit(request):
    profil = Profil.objects.get(username_id=request.user.id)
    user = User.objects.get(id=request.user.id)
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
        profil.mois = profil.dateNaissance.strftime("%b")
        profil.annee = profil.dateNaissance.strftime("%Y")
    except:
        profil.jour = 'Jour'
        profil.mois = 'Mois'
        profil.annee = 'Annee'
    
    if profil.adresse is None:
        profil.adresse = ''
    
    if profil.biographie is None:
        profil.biographie = ''
    
    profil.prenom = user.last_name.split(' ')[0]

    context = {'user': user, 'years': year, 'days': day, 'info_user': profil, 'phone':phone}
    return render(request, 'connexion/edit-profile.html', context)


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
            dateNaissance=datetime.date(int(request.POST.get('annee')), int(request.POST.get('mois')), int(request.POST.get('jour')))
        except:
            dateNaissance = None
        finally:
            user.update(phone=phone,
            adresse = request.POST.get('adresse'),
            biographie = request.POST.get('bio'),
            sexe = request.POST.get('radio'),
            ville = request.POST.get('ville'),
            dateNaissance=dateNaissance
            )
    return redirect(profilInfo, username=request.user.username)

@login_required
def profilInfo(request, username):
    user = get_object_or_404(User, username=username)
    info_user = Profil.objects.get(username_id=user.id)
    return render(request, 'connexion/info-profil.html', locals())


def getImage(request):
    print(request.POST.get('pdp-file'))
    return redirect(profilInfo)