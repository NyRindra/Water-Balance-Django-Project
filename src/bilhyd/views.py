from django.shortcuts import render, redirect
from datetime import datetime

from .dataupload import takedata
from .forms import LoginForm, StudentProfileForm, EmployeeProfileForm, welcomePerson
from .models import Student, Employee, Person
from .calcul import ETPTHORNTWAITE, ETPTURC, ETRTURC, ETRTHORNTWAITE
from .writeexcel import excelthorn, excelturc

import numpy as np

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
        formulaire = LoginForm(request.POST)  # rehefa misy request.POST ao dia misy an'ilay attribut value
        # ao anaty input ilay formulaire
        # rehefa tsy misy request.POST ao
        # a- si l'information a propos du couriel est valide (PAGE 229)
        if formulaire.is_valid():  # VALIDATION AU NIVEAU DU FORMULAIRE FA TSY VALIDATION MDP SY ADRESSE ELECTRONIQUE
            # print("ireto ilay clean")
            # print(formulaire.clean)
            # print("ireto indray ilay cleaned_data")
            # print(type(formulaire.cleaned_data))
            # print(formulaire.cleaned_data)
            # print(formulaire.cleaned_data.get)
            # print(formulaire.cleaned_data['email'])
            # print(formulaire.cleaned_data.get('email'))

            # tsy maintsy manana id ao anaty session ny visiteur na olona connecté vao mahazo mampiasa ny site
            user_email = formulaire.cleaned_data['email']  # alaina ilay email nosaisisser-na (P 275 resaka session)
            logged_user = Person.objects.get(email=user_email)  # alaina ao anaty base olona manana an'iny mail iny
            request.session['logged_user_id'] = logged_user.id  # Enregistrer-na anaty session ny id-any)...
            # ...ilay olona connecté
            # request.session.set_expiry(10)     # Expiration du session dans 120s d'inactivité
            # Izay page(olona) rehetra tsy manana id hita ao anaty session dia redirigé any am page login avokoa

            return redirect("/welcome")
        # b- Sinon
        else:
            print("formulaire non valide")
            print(formulaire)
            print(formulaire.cleaned_data)
            return render(request, "login.html", {'form': formulaire, 'dat': date})
    # 2- Formulaire non envoyé
    else:
        formulaire = LoginForm()
        print(formulaire)
        request.session.set_expiry(1)
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

            print(student_formulaire)
            print("ito ny request.GET")
            print(request.GET)  # test ahitana ilay endrik'ilay prefix

            # prefix st et em vont se montrer si l'on ecrit print request.GET ('st-last_name':['last_name'])

            # a- si l'information a propos du couriel est valide (PAGE 229)
            if student_formulaire.is_valid():  # VALIDATION AU NIVEAU DU FORMULAIRE FA TSY VALIDATION MDP SY
                # ADRESSE ELECTRONIQUE
                resultat = Person.objects.filter(email=request.GET["st-email"])
                if request.GET["st-confirmation"] != request.GET["st-mot_de_passe"]:
                    erreur = "Mot de passe et confirmation de mot de passe non identique"
                    return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                                 'employee_formu': employee_formulaire, 'erreur': erreur})
                elif len(resultat)>=1:
                    erreur = "Ce courriel est deja utilisé par un autre compte"
                    return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                                 'employee_formu': employee_formulaire,
                                                                 'erreur': erreur})
                else:
                    student_formulaire.save()
                    return redirect("/login")
            else:
                return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                             'employee_formu': employee_formulaire})
        elif request.GET['profileType'] == 'employee':
            employee_formulaire = EmployeeProfileForm(request.GET, prefix='em')
            if employee_formulaire.is_valid():
                resultat = Person.objects.filter(email=request.GET["em-email"])
                erreur1 = "Mot de passe et confirmation de mot de passe non identique"
                if request.GET["em-confirmation"] != request.GET["em-mot_de_passe"]:
                    return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                                 'employee_formu': employee_formulaire, 'erreur1':erreur1})
                elif len(resultat)>=1:
                    erreur1 = "Ce courriel est deja utilisé par un autre compte"
                    return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                                 'employee_formu': employee_formulaire,
                                                                 'erreur': erreur1})
                else:
                    employee_formulaire.save()
                    return redirect("/login")

            else:
                return render(request, "user_profile.html", {'student_formu': student_formulaire,
                                                             'employee_formu': employee_formulaire})
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
    logged_User = get_logged_user_from_request(request)  # Resaka session ito (miverifier hoe misy olona actif ve?)


    if not logged_User:
        return redirect('/login')  # Raha tsy ao izy dia 'intru' mitsapatsapa, tsy maintsy manao login

    else:  # Raha misy id ao anaty session,
        print("logged user id")
        print(request.session["logged_user_id"])
        if len(request.POST) > 0:  # efa nisy donnée de formulaire envoyés par la methode post ve?
            # averiko atao vide ilay emplacement de fichier isaky ny mankao am welcome sao misy alaim-panahy
            # hitsapatsapa url "succes". Raha vide izy manko dia tsy marina ilay extension de fichier accepté
            # ato amin'ny logiciel antsika (tsy maintsy xlsx na xlmt no raisina)

            print("Voici le request.POST:", request.POST)
            print("Voici le request.FILES: ", request.FILES)

            # instance va permettre à django de connaitre que le formulaire est associé à un objet deja présent dans la
            # base de données (donc, django va modifier cette objet en ajoutant la valeur(fichier) donnée dans le formulaire)
            # , sinon, django va creer un nouvel objet lors de l'application de la methode save()
            # request.POST traite les données envoyés par le requete via la methode POST...
            # ...tandis que request.FILES traitera les fichiers televersés
            # par le formulaire (tuto Upload File with django)
            # BOKY PAGE 308 et Django website: "File Uploads"
            uploadForm = welcomePerson(request.POST, request.FILES, instance=logged_User)  # BOKY page 308

            if uploadForm.is_valid():

                uploadForm.save()  # on sauvegarde les données obtenu du formulaire
                # et on l'affecte à l'instance logged_User
                RU = request.POST["RU"]
                RFU = request.POST["RFU"]
                print("RU :")
                print(request.POST)

                try:
                    rfu = 100 / float(
                        RFU)  # Nataoko 0 ny RFU raha manana RU ilay olona. Donc mcapturer ZeroDivisionerror za eto
                except:
                    logged_User.RFU = 0
                    logged_User.RU = float(RU)
                    logged_User.save()
                    return redirect('/succes')
                else:
                    logged_User.RU = 0
                    logged_User.RFU = float(RFU)
                    logged_User.save()

                    return redirect('/succes')  # puis, on va aller dans l'url succes
            else:
                # averiko atao vide ilay emplacement de fichier isaky ny mankao am welcome sao misy alaim-panahy
                # hitsapatsapa url "succes". Raha vide izy manko dia tsy marina ilay extension de fichier accepté
                # ato amin'ny logiciel antsika
                logged_User.fichier = ""
                logged_User.save()
                uploadForm = welcomePerson()
                return render(request, 'welcome.html', {'formulaire': uploadForm, 'logged_user': logged_User})

        else:
            # averiko atao vide ilay emplacement de fichier isaky ny mankao am welcome sao misy alaim-panahy
            # hitsapatsapa url "succes". Raha vide izy manko dia tsy marina ilay extension de fichier accepté
            # ato amin'ny logiciel antsika (fonction fichierrecu(request) ligne 211)
            logged_User.fichier = ""
            logged_User.save()
            uploadForm = welcomePerson()
            return render(request, 'welcome.html', {"formulaire": uploadForm,
                                                    "logged_user": logged_User})


# -------------------------------------------TSY VUE IRETO ROA IRETO----------------------------------------------------
# ato isika no hi-verifier hoe misy id ve ao anaty session? id an'iza ? ilaina mba hamantarana ilay olona connecté
def get_logged_user_from_request(request):
    # On va regarder si on trouve un id d'utilisateur dans la session.
    # Si non on renvoie directement None (parceque personne n'est authentifié,
    # ... et il va falloir remplir le formulaire login)
    # Si un utilisateur est authentifié, on cherche d'abord s'il sagit d'un etudiant ou un employé
    # Si rien n'est trouvé, alors, on retourne None.

    if 'logged_user_id' in request.session:  # 'logged_user' ilay natsofotsika t@ nameno ny formulaire login(code ligne 36)
        logged_user_id = request.session['logged_user_id']
        if len(Student.objects.filter(
                id=logged_user_id)) == 1:  # l'importation de l'objet Student du modele est requise
            print(Student.objects.get(id=logged_user_id))  # test fotsiny ito ooo!
            return Student.objects.get(id=logged_user_id)  # Miretourner ny anaran'ilay student ilay fonction
        elif len(Employee.objects.filter(id=logged_user_id)) == 1:
            return Employee.objects.get(id=logged_user_id)
        else:
            return None
    else:
        return None


def load_excel_file(request):
    if "logged_user_id" in request.session:
        if len(Person.objects.filter(id=request.session['logged_user_id'])) == 1:
            Excel = Person.objects.get(id=request.session['logged_user_id']).fichier
            print("FICHIER")
            print(Excel)
            return Excel
        else:
            return None
    else:
        return "No user found"


# -----------------------------------------FICHIER RECU-------------------------------------------------------------
def fichierrecu(request):
    logged_User = get_logged_user_from_request(request)
    if logged_User:
        # on va jouer sur le nom du fichier telechargé, pour ne pas avoir qu'un fichier excel
        nom_du_fichier_recu = logged_User.fichier.name  # Normalement ce sera de type string
        # Io resaka "name" io itako tao @ Django website : Managing File

        required_extension = ['xlsx', 'xltm', 'xltx', 'xlsm']
        if nom_du_fichier_recu[-4:] in required_extension:
            fichier = load_excel_file(request)

            if fichier != "No user found":
                Uploaded_data = takedata(request)
                if Uploaded_data:
                    if Uploaded_data == "bad file":  # sao misy mi-renommer fichier hafa de mody lazaina fa excel
                        message = "Veuillez entrer un fichier excel ()"
                        return render(request, "Fichier_non_recu.html", {'message': message})
                    elif type(Uploaded_data) == list:
                        return render(request, "Fichier_non_recu.html", {'message': Uploaded_data[0]})
                    elif type(Uploaded_data) == tuple:
                        # Nahazo tuple isika vao milamina ny donnée
                        Latitude = Uploaded_data[-1:]
                        ETPturc = ETPTURC(request)  # TEST DES DONNEES VIDES
                        ETPthorn = ETPTHORNTWAITE(request)  # TEST DES DONNEES VIDES
                        print(Latitude)
                        print(ETPturc)
                        print(ETPthorn)

                        # Mahazo str (message d'erreur ireo fonction ETPTURC sy THORN) raha vide daholo ny case temp
                        # na case pluie (vide iray manontolo)
                        if type(ETPthorn) == str:
                            return render(request, "Fichier_non_recu.html", {'message': ETPthorn})

                        else:
                            # raha tsy misy erreur dia efa voacalcul izany ny ETP, izay midika fa complet ny données
                            données = Uploaded_data[0]  # je me rappel que c'est une liste
                            name = Uploaded_data[1]
                            année = Uploaded_data[2]
                            Temperature = données[0]
                            Pluie = données[1]
                            if "Insolation" in name:
                                Insolation = données[2]
                            else:
                                Insolation = "ts clé"
                            if "Humidité" in name:
                                Humidité = données[3]

                            else:
                                Humidité = "ts clé"  # mba hi-capturer-ko ilay erreur fotsiny ilay "str"

                            list_len = []  # ilaiko rehefa ampiseho ilay template (sao mitsatoka année tsy misy)
                            for i in range(len(année)):
                                list_len.append(i + 1)

                            context = {'logged_user': logged_User, "Nb_année": list_len, "Année":année}

                            # ________________________ Maka RFU na RU_________________
                            if logged_User.RFU == 100:
                                context["RFU"] = 100
                            else:   # amin'ito cas ito dia logged_User.RFU = 0 fa ny logged_User.RU no misy valeur
                                context["RU"] = logged_User.RU
                            # ________________________________________________________


# I - Raha misy insolation #############################################################################################
                            if type(Insolation) is not str:

        # I-1 Raha misy humidité ######################################################################################
                                if type(Humidité) is not str:
                                    for i in range(len(année)):
                                        context["T" + str(i + 1)] = Temperature[i]
                                        context["P" + str(i + 1)] = Pluie[i]
                                        context["I" + str(i + 1)] = Insolation[i]
                                        context["H" + str(i + 1)] = Humidité[i]
                                        context["A" + str(i + 1)] = année[i]

                                    # Raha vao mipotsitra VALIDER dia NASIKO VALEUR FOANA ny request.GET
                                    # na tsy nisy formulaire aza (via <a href=>)
                                    if len(request.GET) > 0:

                # A- RFU avancé no ao rehefa profondeur != 0 **********************************************************
                                        if float(request.GET["profondeur"]) != 0 :

                                            # 1-Rehefa voa-selectionner ny methode sy ny enracinement
                                            if request.GET["rapport_RU_RFU"] != "" and request.GET["methode"] != "":
                                                # print("RFU VOARAY e", float( request.GET["rapport_RU_RFU"]))

                                    # Calcul de RU et RFU ==============================================================
                                        # logged_User.RU ilay "RU par centimetre de terre" izay nalaina tao @ welcome
                                        # izay nalefa tany anaty base de données
                                                RU = logged_User.RU * float(request.GET["profondeur"])
                                                RFU = float(request.GET["rapport_RU_RFU"]) * RU
                                                logged_User.RFU = RFU
                                                logged_User.save()

                                    # ==================================================================================
                                                # 1- METHODE DE THORNTWAITE --------------------------------------------
                                                if request.GET["methode"]=="THORNTWAITE":
                                                    Valiny = ETRTHORNTWAITE(request, RFU)
                                                    if type(Valiny) is not str:

                                                        print("ETR")
                                                        print(Valiny[0])

                                                        Precipitation = Pluie
                                                        ETP = ETPthorn
                                                        ETR = Valiny[0]
                                                        Ruissellement = Valiny[1]
                                                        Deficit = Valiny[2]
                                                        VariationStock = Valiny[3]
                                                        RFUparmois = Valiny[4]

                                                        annual_result = excelthorn(request)
                                                        
                                                        context["ETPsum"] = annual_result[0]
                                                        context["ETRsum"] = annual_result[1]
                                                        context["RUISSsum"] = annual_result[2]
                                                        context["DEFICITsum"] = annual_result[3]
                                                        context["STOCKsum"] = annual_result[4]
                                                        context["RFUsum"] = annual_result[5]

                                                        for i in range(len(année)):
                                                            context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                            context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                            context["Ruissellement" + str(i + 1)] = Ruissellement[
                                                                i].tolist()
                                                            context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                            context["VariationStock" + str(i + 1)] = VariationStock[
                                                                i].tolist()
                                                            context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                            context["Année" + str(i + 1)] = année[i]
                                                            context["Methode"] = "THORNTWAITE"


                                                        return render(request, "courbe.html", context)
                                                    else:
                                                        return render(request, "Fichier_non_recu.html", {"message": Valiny})

                                                    # 2- METHODE DE TURC -----------------------------------------------
                                                else:
                                                    Valiny = ETRTURC(request, RFU)
                                                    if type(Valiny) is not str:

                                                        print("ETR")
                                                        print(Valiny[0])

                                                        Precipitation = Pluie
                                                        ETP = ETPturc
                                                        ETR = Valiny[0]
                                                        Ruissellement = Valiny[1]
                                                        Deficit = Valiny[2]
                                                        VariationStock = Valiny[3]
                                                        RFUparmois = Valiny[4]

                                                        annual_result = excelturc(request)
                                                        
                                                        context["ETPsum"] = annual_result[0]
                                                        context["ETRsum"] = annual_result[1]
                                                        context["RUISSsum"] = annual_result[2]
                                                        context["DEFICITsum"] = annual_result[3]
                                                        context["STOCKsum"] = annual_result[4]
                                                        context["RFUsum"] = annual_result[5]
                                                        for i in range(len(année)):
                                                            context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                            context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                            context["Ruissellement" + str(i + 1)] = Ruissellement[
                                                                i].tolist()
                                                            context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                            context["VariationStock" + str(i + 1)] = VariationStock[
                                                                i].tolist()
                                                            context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                            context["Année" + str(i + 1)] = année[i]
                                                            context["Methode"] = "TURC"


                                                        return render(request, "courbe.html", context)
                                                    else:
                                                        return render(request, "Fichier_non_recu.html", {"message": Valiny})

                                            # 2-Rehefa tsy voa-selectionner ny methode sy enracinement
                                            else:
                                                context["erreur"] = "Vous devez selectionner une methode " \
                                                                    "et specifier l'enracinement de votre sol" \
                                                                    " avant de continuer"
                                                return render(request, "resultat.html", context)
                            # B- RFU tsotra (100 mm) no azo rehefa profondeur = 0 **************************************
                                        else:
                                            RFU = logged_User.RFU
                                            # 1-Rehefa tsy voa-selectionner ny methode
                                            if request.GET["methode"] == "":
                                                context["erreur"] = "Avant de continuer, vous devez selectionner une methode"
                                                return render(request, "resultat.html", context)

                                            # 2-Rehefa THORNTWAITE no voaselectionner
                                            elif request.GET["methode"] == "THORNTWAITE":
                                                Valiny = ETRTHORNTWAITE(request, RFU)
                                                if type(Valiny) is not str:
                                                    
                                                    print("ETR")
                                                    print(Valiny[0])

                                                    Precipitation = Pluie
                                                    ETP = ETPthorn
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]
                                                    annual_result = excelthorn(request)
                                                    
                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]
                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]
                                                        context["Methode"] = "THORNTWAITE"

                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message": Valiny})

                                            # 3-Rehefa TURC no voaselectionner
                                            else :
                                                Valiny = ETRTURC(request, RFU)
                                                if type(Valiny) is not str:
                                                    print("ETR")
                                                    print(Valiny[0])

                                                    Precipitation = Pluie
                                                    ETP = ETPturc
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]
                                                    annual_result = excelturc(request)

                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]
                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]
                                                        context["Methode"] = "TURC"

                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message":Valiny})

                                    # RAHA TSY POSITIVE NY request.GET dia mbola tsy nipotsitra VALIDER mihitsy
                                    else:
                                        return render(request, "resultat.html", context)
        # I-2 Raha tsy misy humidité ###################################################################################
                                else:
                                    for i in range(len(année)):
                                        context["T" + str(i + 1)] = Temperature[i]
                                        context["P" + str(i + 1)] = Pluie[i]
                                        context["I" + str(i + 1)] = Insolation[i]
                                        context["A" + str(i + 1)] = année[i]

                                    # Raha vao mipotsitra VALIDER dia NASIKO VALEUR FOANA ny request.GET
                                    # na tsy nisy formulaire aza (via <a href=>)
                                    if len(request.GET)>0:

                            # A- RFU avancé no ao rehefa profondeur != 0 ***********************************************
                                        if float(request.GET["profondeur"]) != 0 :     # RFU avancé

                                        # 1-Rehefa voa-selectionner ny methode sy ny enracinement
                                            if request.GET["rapport_RU_RFU"] != "" and request.GET["methode"] != "":
                                                print("RFU VOARAY", str( request.GET["profondeur"]))

                                    # Calcul de RU et RFU ==============================================================
                                                # logged_User.RU ilay "RU par centimetre de terre" izay nalaina tao @ welcome
                                                # izay nalefa tany anaty base de données
                                                RU = logged_User.RU * float(request.GET["profondeur"])
                                                RFU = float(request.GET["rapport_RU_RFU"]) * RU
                                                logged_User.RFU = RFU
                                                logged_User.save()
                                    # ==================================================================================
                                                if request.GET["methode"]=="THORNTWAITE":
                                                    Valiny = ETRTHORNTWAITE(request, RFU)
                                                    if type(Valiny) is not str:
                                                        Precipitation = Pluie
                                                        ETP = ETPthorn
                                                        ETR = Valiny[0]
                                                        Ruissellement = Valiny[1]
                                                        Deficit = Valiny[2]
                                                        VariationStock = Valiny[3]
                                                        RFUparmois = Valiny[4]

                                                        print("Variation stock")
                                                        print(Valiny[3])
                                                        annual_result = excelthorn(request)

                                                        context["ETPsum"] = annual_result[0]
                                                        context["ETRsum"] = annual_result[1]
                                                        context["RUISSsum"] = annual_result[2]
                                                        context["DEFICITsum"] = annual_result[3]
                                                        context["STOCKsum"] = annual_result[4]
                                                        context["RFUsum"] = annual_result[5]
                                                        for i in range(len(année)):
                                                            context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                            context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                            context["Ruissellement" + str(i + 1)] = Ruissellement[
                                                                i].tolist()
                                                            context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                            context["VariationStock" + str(i + 1)] = VariationStock[
                                                                i].tolist()
                                                            context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                            context["Année" + str(i + 1)] = année[i]
                                                            context["Methode"] = "THORNTWAITE"

                                                        return render(request, "courbe.html", context)
                                                    else:
                                                        print("type valiny")
                                                        print(type(Valiny))
                                                        print(Valiny)
                                                        return render(request, "Fichier_non_recu.html", {"message":Valiny})
                                                # 2- METHODE DE TURC
                                                else:
                                                    Valiny = ETRTURC(request, RFU)
                                                    if type(Valiny) is not str:

                                                        Precipitation = Pluie
                                                        ETP = ETPturc
                                                        ETR = Valiny[0]
                                                        Ruissellement = Valiny[1]
                                                        Deficit = Valiny[2]
                                                        VariationStock = Valiny[3]
                                                        RFUparmois = Valiny[4]
                                                        annual_result = excelturc(request)

                                                        context["ETPsum"] = annual_result[0]
                                                        context["ETRsum"] = annual_result[1]
                                                        context["RUISSsum"] = annual_result[2]
                                                        context["DEFICITsum"] = annual_result[3]
                                                        context["STOCKsum"] = annual_result[4]
                                                        context["RFUsum"] = annual_result[5]

                                                        for i in range(len(année)):
                                                            context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                            context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                            context["Ruissellement" + str(i + 1)] = Ruissellement[
                                                                i].tolist()
                                                            context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                            context["VariationStock" + str(i + 1)] = VariationStock[
                                                                i].tolist()
                                                            context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                            context["Année" + str(i + 1)] = année[i]
                                                            context["Methode"] = "TURC"
                                                            # Resultat annuel
                                                            context["ETPsum"] = annual_result[0]

                                                        return render(request, "courbe.html", context)
                                                    else:
                                                        return render(request, "Fichier_non_recu.html", {"message":Valiny})

                                        # 2-Rehefa tsy voa-selectionner ny methode sy enracinement
                                            else:
                                                context["erreur"] = "Vous devez selectionner une methode " \
                                                                    "et specifier l'enracinement de votre sol" \
                                                                    " avant de continuer"
                                                return render(request, "resultat_without_humidity.html", context)

                            # B- RFU tsotra (100 mm) no azo rehefa profondeur = 0 **************************************


                                        else:                                   # RFU tsotra (100 mm)
                                            print("zany ny type e")
                                            print(type(logged_User.fichiercalculé.name))
                                            print(logged_User.fichiercalculé.name)
                                            RFU = logged_User.RFU
                                            # 1-Rehefa tsy voa-selectionner ny methode
                                            if request.GET["methode"] == "":
                                                context["erreur"] = "Avant de continuer, vous devez selectionner une methode"
                                                return render(request, "resultat_without_humidity.html", context)

                                            # 2-Rehefa THORNTWAITE no voaselectionner
                                            elif request.GET["methode"] == "THORNTWAITE":
                                                Valiny = ETRTHORNTWAITE(request, RFU)
                                                if type(Valiny) is not str:

                                                    print("RFU oooo")
                                                    print(Valiny[4])
                                                    Precipitation = Pluie
                                                    ETP = ETPthorn
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]

                                                    annual_result = excelthorn(request)
                                                    

                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]

                                                   

                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]

                                                        context["Methode"] = "THORNTWAITE"

                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message":Valiny})

                                            # 3-Rehefa TURC no voaselectionner
                                            else:
                                                Valiny = ETRTURC(request, RFU)
                                                if type(Valiny) is not str:
                                                    print("TYPE VALINY")
                                                    print(type(Valiny))
                                                    print(Valiny)
                                                    print("Stock")
                                                    print(Valiny[3])
                                                    Precipitation = Pluie
                                                    ETP = ETPturc
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]

                                                    annual_result = excelturc(request)

                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]
                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]
                                                        context["Methode"] = "TURC"

                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message":Valiny})

                                    else:
                                        return render(request, "resultat_without_humidity.html", context)

# II - Raha tsy misy insolation#########################################################################################

                            else:
                                for i in range(len(année)):
                                    context["T" + str(i + 1)] = Temperature[i]
                                    context["P" + str(i + 1)] = Pluie[i]
                                    context["A" + str(i + 1)] = année[i]
                                if len(request.GET) > 0:
                            # A- RFU avancé no ao rehefa profondeur != 0 -----------------------------------------------
                                    if float(request.GET["profondeur"]) != 0:  # RFU avancé
                                        if request.GET["rapport_RU_RFU"] != "" and request.GET["methode"] != "":
                                            print("RFU VOARAY", str(request.GET["profondeur"]))
                                    # Calcul de RU et RFU ==============================================================
                                        # logged_User.RU ilay "RU par centimetre de terre" izay nalaina tao @ welcome
                                        # izay nalefa tany anaty base de données
                                            RU = logged_User.RU * float(request.GET["profondeur"])
                                            RFU = float(request.GET["rapport_RU_RFU"]) * RU
                                            logged_User.RFU = RFU
                                            logged_User.save()
                                    # ==================================================================================
                                            if request.GET["methode"] == "THORNTWAITE":
                                                Valiny = ETRTHORNTWAITE(request, RFU)
                                                if type(Valiny) is not str:

                                                    print("ETR")
                                                    print(Valiny[0])

                                                    Precipitation = Pluie
                                                    ETP = ETPthorn
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]

                                                    annual_result = excelthorn(request)
                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]
                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]
                                                        context["Methode"] = "THORNTWAITE"

                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message": Valiny})
                                            # 2- METHODE DE TURC -----------------------------------------------
                                            else:
                                                Valiny = ETRTURC(request, RFU)
                                                if type(Valiny) is not str:
                                                    print("ETR")
                                                    print(Valiny[0])

                                                    Precipitation = Pluie
                                                    ETP = ETPturc
                                                    ETR = Valiny[0]
                                                    Ruissellement = Valiny[1]
                                                    Deficit = Valiny[2]
                                                    VariationStock = Valiny[3]
                                                    RFUparmois = Valiny[4]
                                                    annual_result = excelturc(request)
                                                    context["ETPsum"] = annual_result[0]
                                                    context["ETRsum"] = annual_result[1]
                                                    context["RUISSsum"] = annual_result[2]
                                                    context["DEFICITsum"] = annual_result[3]
                                                    context["STOCKsum"] = annual_result[4]
                                                    context["RFUsum"] = annual_result[5]
                                                    for i in range(len(année)):
                                                        context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                        context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                        context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                        context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                        context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                        context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                        context["Année" + str(i + 1)] = année[i]
                                                        context["Methode"] = "TURC"



                                                    return render(request, "courbe.html", context)
                                                else:
                                                    return render(request, "Fichier_non_recu.html", {"message":Valiny})
                                        else:
                                            context["erreur"] = "Specifier l'enracinement de votre sol" \
                                                                " avant de continuer"
                                            return render(request, "resultat_without_insolation.html", context)

                            # B- RFU tsotra (100 mm) no azo rehefa profondeur = 0 --------------------------------------
                                    else:  # RFU tsotra (100 mm)
                                        RFU = logged_User.RFU
                                        # 1-Rehefa tsy voa-selectionner ny methode
                                        if request.GET["methode"] == "":
                                            context[
                                                "erreur"] = "Avant de continuer, vous devez selectionner une methode"
                                            return render(request, "resultat_without_humidity.html", context)

                                        # 2-Rehefa THORNTWAITE no voaselectionner
                                        elif request.GET["methode"] == "THORNTWAITE":
                                            Valiny = ETRTHORNTWAITE(request, RFU)
                                            if type(Valiny) is not str:
                                                print("ETR")
                                                print(Valiny[0])

                                                Precipitation = Pluie
                                                ETP = ETPthorn
                                                ETR = Valiny[0]
                                                Ruissellement = Valiny[1]
                                                Deficit = Valiny[2]
                                                VariationStock = Valiny[3]
                                                RFUparmois = Valiny[4]
                                                annual_result = excelthorn(request)
                                                context["ETPsum"] = annual_result[0]
                                                context["ETRsum"] = annual_result[1]
                                                context["RUISSsum"] = annual_result[2]
                                                context["DEFICITsum"] = annual_result[3]
                                                context["STOCKsum"] = annual_result[4]
                                                context["RFUsum"] = annual_result[5]
                                                for i in range(len(année)):
                                                    context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                    context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                    context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                    context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                    context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                    context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                    context["Année" + str(i + 1)] = année[i]
                                                    context["Methode"] = "THORNTWAITE"

                                                return render(request, "courbe.html", context)
                                            else:
                                                return render(request, "Fichier_non_recu.html", {"message":Valiny})

                                        # 3-Rehefa TURC no voaselectionner
                                        else:
                                            Valiny = ETRTURC(request, RFU)
                                            if type(Valiny) is not str:
                                                print("ETR")
                                                print(Valiny[0])

                                                Precipitation = Pluie
                                                ETP = ETPturc
                                                ETR = Valiny[0]
                                                Ruissellement = Valiny[1]
                                                Deficit = Valiny[2]
                                                VariationStock = Valiny[3]
                                                RFUparmois = Valiny[4]
                                                annual_result = excelturc(request)
                                                context["ETPsum"] = annual_result[0]
                                                context["ETRsum"] = annual_result[1]
                                                context["RUISSsum"] = annual_result[2]
                                                context["DEFICITsum"] = annual_result[3]
                                                context["STOCKsum"] = annual_result[4]
                                                context["RFUsum"] = annual_result[5]
                                                for i in range(len(année)):
                                                    context["ETP" + str(i + 1)] = ETP[i].tolist()
                                                    context["ETR" + str(i + 1)] = ETR[i].tolist()
                                                    context["Ruissellement" + str(i + 1)] = Ruissellement[i].tolist()
                                                    context["Deficit" + str(i + 1)] = Deficit[i].tolist()
                                                    context["VariationStock" + str(i + 1)] = VariationStock[i].tolist()
                                                    context["RFUparmois" + str(i + 1)] = RFUparmois[i].tolist()
                                                    context["Année" + str(i + 1)] = année[i]
                                                    context["Methode"] = "TURC"

                                                return render(request, "courbe.html", context)
                                            else:
                                                return render(request, "Fichier_non_recu.html", {"message": Valiny})
                                else:
                                    return render(request, "resultat_without_insolation.html", context)
                    else:
                        return redirect('/welcome')
                else:
                    return redirect('/login')  # satria tsy misy id anaty session raha None ny valin'ny Uploaded_data
            else:
                print(" No user found, you must logg in before using this site")
                return redirect('/login')
        else:
            print("l'extension est : ", nom_du_fichier_recu[-4:])
            message = "Veuillez entrer fichier excel (.xlsx, .xltm, .xltx, .xlsm)"
            return render(request, "Fichier_non_recu.html", {"message": message})

    else:
        return redirect('/login')

def courbeannuel(request):
    return render(request, "courbe_annuel.html")