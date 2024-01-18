from django.shortcuts import render, redirect
from datetime import datetime
from .forms import LoginForm, StudentProfileForm, EmployeeProfileForm
from .models import Person, Student, Employee


# ----------------------------------------------------VUE LOGIN---------------------------------------------------------
# 1 - Test d'envoie du formulaire
# Creation d'un objet de class LoginForm (creation d'un formulaire)
# en lui passant les valeurs obtenues du requetes HTTP afin que nous
# puissions les verifier avec la methode is_valid()

# a- Si le formulaire est valide:
# on redirige l'utilisateur dans la page d'acceuil

# is_valid() est un methode des formulaires de django pour verifier si le
# couriel est une adresse valide, si les champs obligatoire sont bels et bien fourni (attribut request dans le
# html (takona ao amin'ny formulaire io)).
# La validation du mdp necessite un code
# que nous devons coder nous meme       (PAGE 229)

# b- Sinon
# on reaffiche la meme page mais avec l'objet form contenant le message d'erreur pour les champs incorrects
def login(request):
    date = datetime.now
    # 1- Test si le formulaire a été envoyé:
    print(request.POST)
    if len(request.POST) > 0:
        formulaire = LoginForm(request.POST)
        # a- si l'information a propos du couriel est valide (PAGE 229)
        if formulaire.is_valid():  # VALIDATION AU NIVEAU DU FORMULAIRE FA TSY VALIDATION MDP SY ADRESSE ELECTRONIQUE

            # tsy maintsy manana id ao anaty session ny visiteur na olona connecté vao mahazo mampiasa ny site
            user_email = formulaire.cleaned_data['email']  # alaina ilay email nosaisisser-na (P 275 resaka session)
            logged_user = Person.objects.get(email=user_email)  # alaina ao anaty base olona manana an'iny mail iny
            request.session['logged_user_id'] = logged_user.id  # Enregistrer-na anaty session ny id-any)...
            # ...ilay olona connecté
            # Izay page(olona) rehetra tsy manana id hita ao anaty session dia redirigé any am page login avokoa
            return redirect("/welcome")
        # b- Sinon
        else:
            print("ato oah")
            return render(request, "login.html", {'form': formulaire, 'dat': date})
    # 2- Formulaire non envoyé
    else:
        formulaire = LoginForm()
        return render(request, "login.html", {'form': formulaire, 'dat': date})


# -------------------------------VUE CREATION DE COMPTE STUDENT et EMPLOYEE---------------------------------------------
def register(request):  # LES EXPLICATIONS SONT DANS LA PAGE 266
    # 1- Test si le formulaire a été envoyé:
    print(len(request.GET))
    if len(request.GET) > 0 and 'profileType' in request.GET:
        student_formulaire = StudentProfileForm(prefix="st")  # Mbola formulaire vide aloha ireto
        employee_formulaire = EmployeeProfileForm(prefix="em")  # Mbola formulaire vide aloha ireto
        if request.GET['profileType'] == 'student':
            student_formulaire = StudentProfileForm(request.GET, prefix='st')  # On creer un objet de type
            # StudentProfileForm et on lui passe
            # les données GET de la requete HTTP
            # On peut ensuite appliquer la methode
            # is.valid()
            # a- si l'information a propos du couriel est valide (PAGE 229)
            if student_formulaire.is_valid():  # VALIDATION AU NIVEAU DU FORMULAIRE FA TSY VALIDATION MDP SY
                # ADRESSE ELECTRONIQUE
                student_formulaire.save()
                return redirect("/login")
            else:
                return render(request, "base.html")
        elif request.GET['profileType'] == 'employee':
            employee_formulaire = EmployeeProfileForm(request.GET, prefix='em')
            if employee_formulaire.is_valid():
                employee_formulaire.save()
                return redirect("/login")
        else:  # Ato no hilana ireo formulaire vide raha toa ka tsy nisy formulaire envoyé
            return render(request, 'user_profile.html', {'student_formu': student_formulaire,
                                                         'employee_formu': employee_formulaire})

    # 2- Formulaire non envoyé
    else:
        student_formulaire = StudentProfileForm(prefix='st')
        employee_formulaire = EmployeeProfileForm(prefix='em')
        return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                     'employee_formu': employee_formulaire})


# -----------------------------------Page d'acceuil avec verification de session---------------------------------------
# Tsy tafatsofoka ato amin'ny welcome raha tsy mi-verifier ny session (Page 276)
def welcome(request):
    print("ato e")
    print(Student.objects.get(email="ny.rindra.rk@gmail.com").last_name)  # test fotsiny ireto
    if 'logged_user_id' in request.session:  # Raha misy id ao anaty session,
        logged_user_id = request.session['logged_user_id']  # dia alaivo iny id iny
        logged_user = Person.objects.get(id=logged_user_id)  # dia jereo hoe ao anaty base ve ilay olona
        return render(request, "welcome.html", {'logged_user': logged_user})  # raha ao izy dia mahazo miditra @ site

    else:
        return redirect('/login')  # Raha tsy ao izy dia 'intru' mitsapatsapa, tsy maintsy manao login


#                   --------------TSY VUE ITO IRAY ITO-----------------
# ato isika no hi-verifier hoe misy id ve ao anaty session? id an'iza ? ilaina mba hamantarana ilay olona connecté
def get_logged_user_from_request(request):
    # On va regarder si on trouve un id d'utilisateur dans la session.
    # Si non on renvoie directement None (parceque personne n'est authentifié,
    # ... et il va falloir remplir le formulaire login)
    # Si un utilisateur est authentifié, on cherche d'abord s'il sagit d'un etudiant ou un employé
    # Si rien n'est trouvé, alors, on retourne None.

    if 'logged_user' in request.session:  # 'logged_user' ilay natsofotsika t@ nameno ny formulaire login(code ligne 36)
        logged_user_id = request.session['logged_user']
        if len(Student.objects.filter(
                id=logged_user_id)) == 1:  # l'importation de l'objet Student du modele est requise
            print(Student.objects.get(id=logged_user_id))  # test fotsiny ito ooo!
            return Student.objects.get(id=logged_user_id)  # Miretourner ny anarana fotsiny ito
        elif len(Employee.objects.filter(id=logged_user_id)) == 1:
            return Employee.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None
