from django import forms  # Tsy maintsy importer-na
from .models import Person, Student, Employee


# 1- CREATION D'UN FORMULAIRE A L"AIDE DU BIBLIOTHEQUE forms
class LoginForm(forms.Form):  # LoginForm est une classe heritant la classe Form se trouvant dans forms
    email = forms.EmailField(label='Courriel')  # Voici comment on cree un champ pour remplir un email avec django
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)  # Creation champ mot de passe

    # ireo nom ireo no,lasa any anaty objet request.GET(na request.POST) rehefa ilay manao print
    # ireo nom ireo ihany ilay "name" any anaty html raha tsy nampiasa bibliotheque
    # forms isika rehefa mamorona formulaire

    # 2 - VALIDATION DES MOT DE PASSE ET ADRESSE ELECTRONIQUE
    def clean(self):  # Naverina nantsoina ny methode clean izay methode avy ao amin'ny classe parente (PAGE 233)
        cleaned_data = super(LoginForm, self).clean()  # ito super ito no niantso an'ilay clean ka natao
        # tanaty variable "clean_data" izy vao nampiasaina (DICTIONNAIRE NY CLEANED_DATA)
        _email = cleaned_data.get("email")  # Natao ato anaty variable "_email" ilay email azo tao amin'ny request.POST
        _password = cleaned_data.get("password")  # On a fait de meme pour le password se trouvant dans request.POST
        print("nandalo test")
        print(_email)  # test fotsiny
        print(cleaned_data)
        # VERIFICATION DES DEUX CHAMPS
        # a- Raha validé tao amin'ny formulaire ilay mdp sy courriel, izany hoe voamarina fa tsy vide na adresse mazava
        if _email and _password:  # raha misy ilay _email sy _password, izany hoe tsy "None"
            # EXPLICATION PAGE 259
            result = Person.objects.filter(mot_de_passe=_password, email=_email)  # Verifier si les mdp et couriel
            # sont dans la base de données
            if len(result) != 1:  # Raha tsy olona tokana  no manana an'ireo dia diso izany ny mdp na couriel
                raise forms.ValidationError("Identifiant ou Mot de passe erroné.")

        return cleaned_data     # {'email': 'ny.rindra.rk@gmail.com', 'password': 'asdfasdfasdf'}
                                # (Dictionnaire Otrnio le cleaned_data), izany hoe mi-retourner an'io
                                # ilay fonction "clean" rehefa antsoina

        # Si les champs n'etaient pas valide, cleaned_data.get retournera "None"


# 2- FORMULAIRE A L'AIDE DU BIBLIOTHEQUES ModelForm
# -----------------------------------Formulaire de creation de compte ETUDIANT------------------------------------------
# Nous allons ici utiliser la classe ModelForm au lieu d'utiliser la classe Form
# Les ModelForm s'utilisent pratiquement de la meme maniere que le modele Form, ils ajoutent simplement une methode
# "save" qui, une fois les données du formulaire validées, les sauvegardent dans la base de données


class StudentProfileForm(forms.ModelForm):  # Class heritant la classe ModelForm
    # On n'ecrit plus les formulaires comme dans la page login,
    # on utilise la classe Student qui possedent les attributs
    # de la class Person, ils vont etre convertit comme formulaire

    class Meta:  # Classe Meta qui sert a configurer notre formulaire, il precise sur quel model on doit se baser
        model = Student  # Utilisation du modele Student
        exclude = ('friends', 'fichier', 'fichiercalculé', 'RFU', 'RU', "faculty")  # On exclus l'attibut fiends(C'est une liaison mais nous n'allons pas parler d'amitier
                                # dans la creation du compte

# -----------------------------------Formulaire de creation de compte Employé------------------------------------------
class EmployeeProfileForm(forms.ModelForm):  # Class heritant la classe ModelForm
    # On n'ecrit plus les formulaires comme dans la page login,
    # on utilise la classe Student qui possedent les attributs
    # de la class Person, ils vont etre convertit comme formulaire

    class Meta:  # Classe Meta qui sert a configurer notre formulaire, il precise sur quel model on doit se baser
        model = Employee  # Utilisation du modele Employee
        exclude = ('friends', 'fichier', "fichiercalculé",'RFU', 'RU', "faculty", "job", "campus")  # On exclus l'attibut fiends(C'est une liaison mais nous n'allons pas parler d'amitier
                                            # dans la creation du compte
# ------------------------------Formulaire d'upload dans welcome--------------------------------------------------------
class welcomePerson(forms.ModelForm):
    class Meta:
        model = Person        # Mi-se baser amin'ny model Student aho eto
        fields = ['fichier']  # ilay attribut fichier ihany no asehoko (Hita tam net) , asina virgule dia ampina
                                # attribut hafa raha toa ka te hanampy champ amin'ilay formulaire(ex: ['fichier','name'])


