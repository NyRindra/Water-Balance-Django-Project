from django import forms  # Tsy maintsy importer-na
from .models import Person


# 1- CREATION D'UN FORMULAIRE A L"AIDE DU BIBLIOTHEQUE forms
class LoginForm(forms.Form):  # LoginForm est une classe heritant la classe Form se trouvant dans forms
    email = forms.EmailField(label='Courriel')  # Voici comment en creer un champ pour remplir un email avec django
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)  # Creation champ mot de passe

    # ireo nom ireo no,lasa any anaty objet request.GET(na request.POST) rehefa ilay manao print
    # ireo nom ireo ihany ilay "name" any anaty html raha tsy nampiasa bibliotheque
    # forms isika rehefa mamorona formulaire

    # 2 - VALIDATION DES MOT DE PASSE ET ADRESSE ELECTRONIQUE
    def clean(self):  # Naverina nantsoina ny methode clean izay methode avy ao amin'ny classe parente (PAGE 233)
        cleaned_data = super(LoginForm, self).clean()  # ito super ito no niantso an'ilay clean ka natao
        # tanaty variable "clean_data" izy vao nampiasaina
        _email = cleaned_data.get("email")  # Ntatao ato anaty variable "email" ilay email azo tao amin'ny request.POST
        _password = cleaned_data.get("password")  # On a fait de meme pour le password se trouvant dans request.POST

        print(email)  # test fotsiny
        # VERIFICATION DES DEUX CHAMPS
        # a- Raha validé tao amin'ny formulaire ilay mdp sy courriel, izany hoe voamarina fa tsy vide na adresse mazava
        if _email and _password:  # raha misy ilay email sy password, izany hoe tsy "None"
            if email != 'ny.rindra.rk@gmail.com' or password != 'MiandrynyDadanao':
                raise forms.ValidationError("Identifiant ou Mot de passe erroné")
        return cleaned_data
        # Si les champs n'etaient pas valide, cleaned_data.get retournera "None"
