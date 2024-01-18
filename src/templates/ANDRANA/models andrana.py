from django.db import models  # import du bibliotheque models
from django import forms



# ___________________________________Modele mi-gerer ny table bilhyd_person_____________________________________________



class Person(models.Model):  # Creation d'une classe heritant la classe Model
    # On defini ensuite tous nos champs en specifiant leur types (Comme lors de la creation des formulaires


    nom = models.CharField(max_length=30)
    prénom = models.CharField(max_length=30)
    date_de_naissance = models.DateField(max_length=8)
    téléphone = models.CharField(
        max_length=25)  # Charfield because we can have numbers that contains + / (like +261)
    email = models.EmailField()
    mot_de_passe = models.CharField(max_length=32)  # dans le cas reel, nous ne devons pas stocker le mdp en clair
    confirmation = models.CharField(null=True ,max_length=32)
    RU = models.FloatField(null=True)  #null DJANGO DOCUMENTATION PAGE 115 in Field option
    RFU = models.FloatField(null=True)

# ______________________________________________________________________________________________________________________
    # ito ilaina rehefa te ampiditra fichier anaty dossier files
    # (mila parametrer-na ny fichier settings (MEDIA_ROOT))
    # raha tsy parametrer-na dia lasa MEDIA_ROOT = '' par defaut io
    fichier = models.FileField(upload_to='User_data/User_data_upload')    # afaka tsy asina upload_to dia
                                                                # lasa any am repertoire MEDIA_ROOT fotsiny ilay fichier
    fichiercalculé = models.FileField()

# ______________________________________________________________________________________________________________________

# ------------------------Liaison entre les personnes (liaison n-n)----------------------------
    friends = models.ManyToManyField('self')
    # ------------------------Liaison entre faculty et personne------------------------------------
    faculty = models.ForeignKey('Faculty', on_delete=models.DO_NOTHING)  # il est recommandé que le nom du champ
    # foreign soit le nom de la classe mais en minuscule
    genre = models.ForeignKey('Genre', on_delete=models.DO_NOTHING)

    # Attribut statique (ampiasaina rehefa te haka zavatra ato anatin'ny classe ex: Person.Attribut)
    person_type = 'generic' # Ohatra: Nampiasaina any amin'ny templates welcome ito

    # -----------Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        return self.nom + ' ' + self.prénom


# __________________________________Modele mi-gerer ny table bilhyd_message_____________________________________________
class Message(models.Model):  # Mamorona modele iray ho an'ny message (izany hoe hilalao table hafa aho izany)
    author = models.ForeignKey('Person', on_delete=models.DO_NOTHING)  # Liaison 1-n avec la classe (ou
    # l'objet ou le model) Person
    message_content = models.TextField()
    publication_date = models.DateField()

    # Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        if len(self.message_content) > 20:
            return self.message_content[:19] + '...'
        else:
            return self.message_content


# ----------------------------------------------------------------------------------------------------------------------
# ireto manaraka ireto dia model en relation (manana liaison) avec les classes filles que l'on va creer encore plus bas
class Job(models.Model):
    title = models.CharField(max_length=30)

    # Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        return self.title


class Faculty(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30)

    # Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        return self.name


class Cursus(models.Model):
    title = models.CharField(max_length=30)

    # Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        return self.title


class Campus(models.Model):
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=30)

    # Affichage dans l'interface d'administration   (AFFICHAGE ANY AM ADMIN NO HILANA AN"IRETO)
    def __str__(self):
        return self.name


class Genre(models.Model):
    g = models.CharField(max_length=5)

    def __str__(self):
        return self.g


# --------------------------Modele heritant la classe Person, donc ce sont des personnes...-----------------------------

class Employee(Person):  # Ny employé dia personne ihany fa classe fille fotsiny
    office = models.CharField(max_length=30)

    # -----------Liaison 1-n avec la classe Campus et la classe Job-------------
    campus = models.ForeignKey('Campus',
                               on_delete=models.DO_NOTHING)  # Ny Campus afaka mandray olona(employe) betsaka,
    # fa ny employe iray ana campus iray
    job = models.ForeignKey('Job',
                            on_delete=models.DO_NOTHING)  # Ny Job afaka ataon'olona betsaka, fa ny employé dia
    # mpiandraikitra @ asa iray
    # -------------attribut statique------------
    person_type = 'emloyee'


class Student(Person):  # Ny Student dia personne ihany koa fa classe fille fotsiny
    année = models.IntegerField()

    # --------Liaison 1-n avec la classe--------
    cursus = models.ForeignKey('Cursus', on_delete=models.DO_NOTHING)
    # -------------attribut statique------------
    person_type = 'student'

# ----------------------------------------------------------------------------------------------------------------------
# Je vais maintenant creer les modeles necessaires pour le calcule


class Thorntwaite_coeff_corr(models.Model):
    Latitude = models.IntegerField()
    Janvier = models.FloatField()
    Fevrier = models.FloatField()
    Mars = models.FloatField()
    Avril = models.FloatField()
    Mai = models.FloatField()
    Juin = models.FloatField()
    Juillet = models.FloatField()
    Aout = models.FloatField()
    Septembre = models.FloatField()
    Octobre = models.FloatField()
    Novembre = models.FloatField()
    Decembre = models.FloatField()


class Thorntwaite_etp_non_corrigee(models.Model):
    Temperature = models.FloatField()
    Etp_non_corrigee = models.FloatField()


class Turc_duree_astro(models.Model):
    Latitude = models.IntegerField()
    Janvier = models.FloatField()
    Fevrier = models.FloatField()
    Mars = models.FloatField()
    Avril = models.FloatField()
    Mai = models.FloatField()
    Juin = models.FloatField()
    Juillet = models.FloatField()
    Aout = models.FloatField()
    Septembre = models.FloatField()
    Octobre = models.FloatField()
    Novembre = models.FloatField()
    Decembre = models.FloatField()


class Turc_radiation_globale(models.Model):
    Latitude = models.IntegerField()
    Janvier = models.FloatField()
    Fevrier = models.FloatField()
    Mars = models.FloatField()
    Avril = models.FloatField()
    Mai = models.FloatField()
    Juin = models.FloatField()
    Juillet = models.FloatField()
    Aout = models.FloatField()
    Septembre = models.FloatField()
    Octobre = models.FloatField()
    Novembre = models.FloatField()
    Decembre = models.FloatField()
