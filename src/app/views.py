from datetime import datetime
from django.shortcuts import render, redirect
from bilhyd.forms import LoginForm


# Create your views here.
def login(request):
    context = {}
    context['date'] = datetime.now  # Nataoko fotsiny

    # test si le formulaire a été envoyé
    print(request.POST)
    print(len(request.POST))
    if len(request.POST) > 0:
        # request est un objet de type HttpResponse, Boky resumé
        # Test si les parametres attendus ont été transmis
        if 'email' not in request.POST or 'password' not in request.POST:
            error = "Veuiller entrer un adresse email et un mot de passe"
            return render(request, "login.html", {'error': error})
        else:
            # ireo 'email' sy 'password' anaty request.POST ireo ilay "name" ary amin'ny input ao @ # html"
            email = request.POST['email']
            password = request.POST['password']
            # Test si le mot de passe est bon
            if password != 'MiandrynyDadanao' or email != 'ny.rindra.rk@gmail.com':
                error = " Identification ou mot de passe éronné."
                return render(request, 'login.html', {'error': error})
            # Si tout est bon, on va passer dans la page d'acceuil. D'ou l'utilisation de la methode redirect
            else:
                return redirect('/welcome')  # il faut importer la fonction redirect

        # Si le formulaire n'a pas été envoyé
    else:
        return render(request, 'login.html')
