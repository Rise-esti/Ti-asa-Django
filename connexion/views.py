from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profil, Formation, Competence, Experience, Interet, Publication
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


@login_required
def changePasswd(request):
    user_viewed = User.objects.get(pk=request.user.id)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded ='active'
    return render(request, 'connexion/profil/edit-password.html', locals())
    

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
    pubs = Publication.objects.filter(valable=True).order_by('-id')
    users_viewed = []
    for user_viewed in pubs:
        user = User.objects.get(pk=user_viewed.username_id)
        user_viewed.first_name = user.first_name
        user_viewed.last_name = user.last_name
        if user_viewed.langue != '' and user_viewed.langue is not None:
            user_viewed.langue = user_viewed.langue.split(';')
        if user_viewed.mission != '' and user_viewed.mission is not None:
            user_viewed.mission = user_viewed.mission.split(';')
        if user_viewed.competence != '' and user_viewed.competence is not None:
            user_viewed.competence = user_viewed.competence.split(';')
        if user_viewed.experience != '' and user_viewed.experience is not None:
            user_viewed.experience = user_viewed.experience.split(';')
        if user_viewed.formation != '' and user_viewed.formation is not None:
            user_viewed.formation = user_viewed.formation.split(';')
        profil = Profil.objects.get(username_id=user_viewed.username_id)
        user_viewed.pdp = profil.profilpic 
        users_viewed.append(user_viewed)
    days = [x for x in range(1, 32)]
    context = {'info_user':info_user, 'users_viewed':users_viewed, 'days':days}          
    return render(request, 'connexion/home.html', context)


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


def infoCompetenceAdd(request):
    if request.POST.get('competence') != '':
        Competence(username_id=request.user.id,
        competence=request.POST.get('competence'),
        description=request.POST.get('description'),
        niveau=request.POST.get('niveau')
        ).save()
        return redirect(competenceInfo, username=request.user.username)
    else:
        return HttpResponse('not okey')


def infoCompetenceEdit(request):
    if request.POST.get('competence') != '':
        Competence.objects.filter(pk=request.POST.get('id')).update(username_id=request.user.id,
        competence=request.POST.get('competence'),
        description=request.POST.get('description'),
        niveau=request.POST.get('niveau')
        )
        return redirect(competenceInfo, username=request.user.username)
    else:
        return HttpResponse('not okey')


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


def competenceInfo(request, username):
    user_viewed = get_object_or_404(User, username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    users_competence = Competence.objects.filter(username_id=user_viewed.id).all()
    competence = 'active'
    if  request.user.id == user_viewed.id:
        if len(users_competence) == 0:
            return redirect(competenceAdd)
    return render(request, 'connexion/profil/competence-profil.html', locals())


def formationDelete(request, id):
    Formation.objects.filter(pk=id).delete()
    return redirect(formationInfo, request.user.username)


def competenceAdd(request):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    try:
        formation_user_viewed = Profil.objects.filter(username_id=user_viewed.id)
    except:
        pass

    moded = 'active'

    return render(request, 'connexion/profil/competence-profil-add.html', locals())


def competenceDelete(request, id):
    Competence.objects.filter(pk=id).delete()
    return redirect(competenceInfo, request.user.username)


def competenceEdit(request, id):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded = 'active'
    user_competence = Competence.objects.get(pk=id)
    return render(request, 'connexion/profil/competence-profil-edit.html', locals())


def experienceInfo(request, username):
    user_viewed = get_object_or_404(User, username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    users_experience= Experience.objects.filter(username_id=user_viewed.id).order_by('-annee_debut').all()
    experience ='active'
    if user_viewed.id == request.user.id:
        if len(users_experience) ==0:
            return redirect(experienceAdd)
    return render(request, 'connexion/profil/experience-profil.html', locals())


def experienceAdd(request):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded = 'active'
    years = [x for x in range(int(datetime.datetime.today().strftime('%Y')) + 1, 1980, -1)]
    return render(request, 'connexion/profil/experience-profil-add.html', locals())


def experienceEdit(request, id):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded ='active'
    years = [x for x in range(int(datetime.datetime.today().strftime('%Y')) + 1, 1980, -1)]

    user_experience= Experience.objects.get(pk=id)

    return render(request, 'connexion/profil/experience-profil-edit.html', locals())


def experienceDelete(request, id):
    Experience.objects.filter(pk=id).delete()
    return redirect(experienceInfo, request.user.username)


def infoExperienceAdd(request):
    if request.POST.get('lieu') != '':
        try:
            int(request.POST.get('Annee_deb'))
        except:
            return HttpResponse("Il faut entrer l'annee de debut")
        else:
            Experience(username_id=request.user.id,
            lieu = request.POST.get('lieu'),
            mois_debut = request.POST.get('Mois_deb'),
            annee_debut = request.POST.get('Annee_deb'),
            mois_fin = request.POST.get('Mois_fin'),
            annee_fin = request.POST.get('Annee_fin'),
            poste = request.POST.get('poste'),
            description = request.POST.get('description')
            ).save()
            return redirect(experienceInfo, username=request.user.username)
    else:
        return HttpResponse("Il faut entrer le lieu du formation")
    return redirect(experienceInfo, username=request.user.username)


def infoExperienceEdit(request):
    if request.POST.get('lieu') != '':
        try:
            int(request.POST.get('Annee_deb'))
        except:
            return HttpResponse("Il faut entrer l'annee de debut")
        else:
            Experience.objects.filter(pk=request.POST.get('id')).update(lieu = request.POST.get('lieu'),
            mois_debut = request.POST.get('Mois_deb'),
            annee_debut = request.POST.get('Annee_deb'),
            mois_fin = request.POST.get('Mois_fin'),
            annee_fin = request.POST.get('Annee_fin'),
            poste = request.POST.get('poste'),
            description = request.POST.get('description')
            )
            return redirect(experienceInfo, username=request.user.username)
    else:
        return HttpResponse("Il faut entrer le lieu du formation")


def interetAdd(request):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded = 'active'

    return render(request, 'connexion/profil/interet-profil-add.html', locals())


def interetEdit(request, id):
    user_viewed = get_object_or_404(User, username=request.user.username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    moded ='active'

    user_interet= Interet.objects.get(pk=id)

    return render(request, 'connexion/profil/interet-profil-edit.html', locals())


def interetInfo(request, username):
    user_viewed = get_object_or_404(User, username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    users_interet = Interet.objects.filter(username_id=user_viewed.id).all()
    interet ='active'
    if user_viewed.id == request.user.id:
        if len(users_interet) ==0:
            return redirect(interetAdd)
    return render(request, 'connexion/profil/interet-profil.html', locals())


def infoInteretAdd(request):
    Interet(username_id=request.user.id , interet=request.POST.get('interet'), description=request.POST.get('description')).save()
    return redirect(interetInfo, request.user.username)


def interetDelete(request, id):
    Interet.objects.filter(pk=id).delete()
    return redirect(interetInfo, request.user.username)


def infoInteretEdit(request):
    Interet.objects.filter(pk=request.POST.get('id')).update(interet=request.POST.get('interet'), description=request.POST.get('description'))
    return redirect(interetInfo, request.user.username)


def publier(request):

    try:
        datelimit_jour = int(request.POST.get('jour'))
    except:
        datelimit_jour = None

    try:
        image = publish_image(request)
    except:
       image = ''

    Publication(username_id=request.user.id,
    legende = request.POST.get('texte'),
    experience = request.POST.get('experience'),
    formation = request.POST.get('formation'),
    competence = request.POST.get('competence'),
    personnalite = request.POST.get('personnalite'),
    langue = request.POST.get('langue'),
    image = image,
    date_limit_jour = datelimit_jour,
    date_limit_mois = request.POST.get('mois'),
    lieu = request.POST.get('lieu'),
    mission = request.POST.get('mission')
    ).save()
    return redirect(home)


def publish_image(req):
    with open('connexion/static/connexion/images/Picture/pub/'+str(req.user.id)+'_'+str(time.time())[:10]+'.png', 'wb+') as destination:
        for chunk in req.FILES.get('image').chunks():
            destination.write(chunk)
    return 'connexion/images/Picture/pub/'+str(req.user.id)+'_'+str(time.time())[:10]+'.png'


def updatePasswd(request):
    Personne = User.objects.get(pk=request.user.id)
    if Personne.check_password(request.POST.get('ex-mdp')):
        Personne.set_password(request.POST.get('new-mdp'))
        Personne.save()
        user = authenticate(username=Personne.username, password=request.POST.get('new-mdp'))
        login(request, user)
        
    return redirect(changePasswd)

def infoJournal(request, username):
    user_viewed = User.objects.get(username=username) 
    pubs = Publication.objects.filter(valable=True, username_id=user_viewed.id).order_by('-id')
    users_viewed = []
    for user_viewed in pubs:
        user = User.objects.get(pk=user_viewed.username_id)
        user_viewed.first_name = user.first_name
        user_viewed.last_name = user.last_name
        if user_viewed.langue != '' and user_viewed.langue is not None:
            user_viewed.langue = user_viewed.langue.split(';')
        if user_viewed.mission != '' and user_viewed.mission is not None:
            user_viewed.mission = user_viewed.mission.split(';')
        if user_viewed.competence != '' and user_viewed.competence is not None:
            user_viewed.competence = user_viewed.competence.split(';')
        if user_viewed.experience != '' and user_viewed.experience is not None:
            user_viewed.experience = user_viewed.experience.split(';')
        if user_viewed.formation != '' and user_viewed.formation is not None:
            user_viewed.formation = user_viewed.formation.split(';')
        profil = Profil.objects.get(username_id=user_viewed.username_id)
        user_viewed.pdp = profil.profilpic 
        users_viewed.append(user_viewed)
    days = [x for x in range(1, 32)]
    user_viewed = User.objects.get(username=username)
    info_user_viewed = Profil.objects.get(username_id=user_viewed.id)
    info_user = Profil.objects.get(username_id=request.user.id)
    context = {'info_user':info_user, 'users_viewed':users_viewed, 'days':days, 'user_viewed':user_viewed, 'info_user_viewed':info_user_viewed, 'journal':'active'}          
    return render(request, 'connexion/profil/journal-info.html', context)