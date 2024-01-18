from django.shortcuts import render

from .dataupload import takedata
from .models import Thorntwaite_coeff_corr, Thorntwaite_etp_non_corrigee, Turc_duree_astro, Turc_radiation_globale, Person
import numpy as np


# Creation d'une fonction retournant l'entier la plus proche de K (Tam net fotsiny fa tsy misy fanazavana)
    # Mitady valeur la plus proche de K dans une liste
def laplusproche(list, k):
    return list[min(range(len(list)), key=lambda i: abs(list[i] - k))]

def ETPTHORNTWAITE(request):
    data = takedata(request)
    # Liste daholo ireto ambany ireto
    data_list = data[0]
    Parameters_name = data[1]
    Année = data[2]
    latitude_excel = data[3]

    if "Température" in Parameters_name:
        TEMPERATURE = data_list[0]
    else:
        Message = "Données de températures non trouvés"
        return Message
    if "Précipitation" in Parameters_name:
        PLUIE = data_list[1]
    else:
        Message = "Données de précipitation non trouvés"
        return Message

    if len(PLUIE)>0 and len(TEMPERATURE) > 0:
        indice_thermique = []
        I1 = []  # Voici la premiere liste ou l'on va stocker les 12 premiers elements de la liste "ind"
        I2 = []  # Voici la deuxieme liste ou l'on va stocker les 12 elements suivant de la liste "ind"
        I3 = []  # Voici la troisieme liste ou l'on va stocker les troisiemes douzaine d'elements de la liste "ind"
        I4 = []  # -//- la quatrieme
        I5 = []  # -//- ...
        I6 = []  # -//- ...
        I7 = []  # -//- ...
        I8 = []  # -//- ...
        I9 = []  # -//- ...
        I10 = []
        I = []  # Nous allons stocker ici les valeurs des indices thermique annuel
        a = []  # chaque année doit contenir un a... si on calcul un etp de 10 ans, nous devons avoir 10 a

        # Calcul d'indice mensuel
        for i in range(len(Année)):  # voa filtre eto ireo zeros be dia be ao am array any amle dataupload.py
            for j in range(12):
                ind_therm = ((TEMPERATURE[i][j])/5)**1.514
                indice_thermique.append(ind_therm)


        for i in range(len(indice_thermique)):
            if 0 <= i <= 11:
                I1.append(indice_thermique[i])  # Stockage des 12 premiers elements dans la liste I1
            elif 12 <= i <= 23:
                I2.append(indice_thermique[i])  # Stockage des 12 elements suivant dans la liste I2
            elif 24 <= i <= 35:
                I3.append(indice_thermique[i])  # Stockage des 3e douzaine d'elements dans la liste I3
            elif 36 <= i <= 47:
                I4.append(indice_thermique[i])  # ...
            elif 48 <= i <= 59:
                I5.append(indice_thermique[i])  # ...
            elif 60 <= i <= 71:
                I6.append(indice_thermique[i])  # ...
            elif 72 <= i <= 83:
                I7.append(indice_thermique[i])  # ...
            elif 84 <= i <= 95:
                I8.append(indice_thermique[i])  # ...
            elif 96 <= i <= 107:
                I9.append(indice_thermique[i])  # ...
            elif 108 <= i <= 119:
                I10.append(indice_thermique[i])  # ...
            else:
                pass

        # Calcul d'indice annuel :

        I.append(sum(I1))  # La somme d'indice mensuel du premiere années est stocker dans I[0]
        I.append(sum(I2))
        I.append(sum(I3))
        I.append(sum(I4))
        I.append(sum(I5))
        I.append(sum(I6))
        I.append(sum(I7))
        I.append(sum(I8))
        I.append(sum(I9))
        I.append(sum(I10))

        # Calcul de a
        for i in range(len(Année)):
            a_calcul = (((1.6 / 100) * I[i]) + 0.5)
            a.append(a_calcul)

# ETP non corrigé:______________________________________________________________________________________________________

# Arrondissement de la latitude_________________________________________________________________________________________
        model_lat = []      # Atao ato daholo ilay latitude anaty modele
        for i in range(1,45):
            Coeff_cor = Thorntwaite_coeff_corr.objects.get(id = i)
            model_lat.append(Coeff_cor.Latitude)
        latitude_calcul = laplusproche(model_lat, latitude_excel[0]) # Ampiasaina ilay fonction "laplusproche"
#_______________________________________________________________________________________________________________________

# Arrondissement de la temperature______________________________________________________________________________________
        model_temp_thorntwaite = []
        for i in range(1,25):
            model_temp = Thorntwaite_etp_non_corrigee.objects.get(id=i)
            model_temp_thorntwaite.append(model_temp)  #Nampiasaiko ao ambany ao
#_______________________________________________________________________________________________________________________

            # Calcul ETP non corrigé:
        ETPnc = np.zeros((len(Année), 12))
        erreur = []
        indice_erreur = []
        for i in range(len(Année)):
            for j in range(12):
                if TEMPERATURE[i][j] < 26.5:
                    ETPnonco = 16*(10*(TEMPERATURE[i][j])/I[i])**a[i]
                    ETPnc[i][j] = ETPnonco
                elif 26.5 <= TEMPERATURE[i][i] <= 38:
                    temp_arrondi = laplusproche(model_temp_thorntwaite, TEMPERATURE[i][j])
                    ETPnonco = Thorntwaite_etp_non_corrigee.objects.get(Temperature = temp_arrondi).Etp_noncorrigee
                    ETPnc[i][j] = ETPnonco
                elif TEMPERATURE[i][j] > 38:
                    erreur.append(TEMPERATURE[i][j])
                    indice_erreur.append(i)
                    break
        if erreur:
            Message = "Temperature superieure à 38. Année {}".format(Année[indice_erreur[0]])
            return Message

        Coefficient_de_correction = Thorntwaite_coeff_corr.objects.get(Latitude = latitude_calcul)
        ETP = np.zeros((len(Année), 12))

        for i in range(len(Année)):
            ETP[i][0] = (Coefficient_de_correction.Janvier) * ETPnc[i][0]
            ETP[i][1] = (Coefficient_de_correction.Fevrier) * ETPnc[i][1]
            ETP[i][2] = (Coefficient_de_correction.Mars) * ETPnc[i][2]
            ETP[i][3] = (Coefficient_de_correction.Avril) * ETPnc[i][3]
            ETP[i][4] = (Coefficient_de_correction.Mai) * ETPnc[i][4]
            ETP[i][5] = (Coefficient_de_correction.Juin) * ETPnc[i][5]
            ETP[i][6] = (Coefficient_de_correction.Juillet) * ETPnc[i][6]
            ETP[i][7] = (Coefficient_de_correction.Aout) * ETPnc[i][7]
            ETP[i][8] = (Coefficient_de_correction.Septembre) * ETPnc[i][8]
            ETP[i][9] = (Coefficient_de_correction.Octobre) * ETPnc[i][9]
            ETP[i][10] = (Coefficient_de_correction.Novembre) * ETPnc[i][10]
            ETP[i][11] = (Coefficient_de_correction.Decembre) * ETPnc[i][11]
        return ETP


def ETPTURC(request):
    data = takedata(request)
    Année = data[2]
    Parameters_name = data[1]
    data_list = data[0]
    latitude_excel = data[3]


    if "Température" in Parameters_name:
        TEMPERATURE = data_list[0]
    else:
        Message = "Données de températures non trouvés!"
        return Message

    if "Précipitation" in Parameters_name:
        PLUIE = data_list[1]
    else:
        Message = "Données de précipitation non trouvés!"
        return Message

    if "Insolation" in Parameters_name:
        INSOLATION = data_list[2]
    else:
        Message = "Données de non trouvés (Insolation)!"
        return Message

# ------------------------------------------------DEBUT DU CALCUL------------------------------------------------------
    ETP = np.zeros((len(Année), 12))
    Ig = np.zeros((len(Année), 12))  # Radiation globale moyenne (à calculer Ig = Iga(0,18 + 0,62(h/H))

    # Arrondissement de la latitude :
    model_lat = []
    for i in range(1, 102):  # on va prendre toutes les latitudes se trouvant dans la table duree astro de la BDD
        x = Turc_duree_astro.objects.get(id=i)
        y = x.Latitude
        model_lat.append(y)
    latitude_calcul = laplusproche(model_lat, latitude_excel[0])

    for i in range(len(Année)):
        for j in range(12):
            IGA = Turc_radiation_globale.objects.get(Latitude=latitude_calcul)
            H = Turc_duree_astro.objects.get(Latitude=latitude_calcul)
            if j == 0:
                Iga = IGA.Janvier
                duree_astro = H.Janvier
            if j == 1:
                Iga = IGA.Fevrier
                duree_astro = H.Fevrier
            if j == 2:
                Iga = IGA.Mars
                duree_astro = H.Mars
            if j == 3:
                Iga = IGA.Avril
                duree_astro = H.Avril
            if j == 4:
                Iga = IGA.Mai
                duree_astro = H.Mai
            if j == 5:
                Iga = IGA.Juin
                duree_astro = H.Juin
            if j == 6:
                Iga = IGA.Juillet
                duree_astro = H.Juillet
            if j == 7:
                Iga = IGA.Aout
                duree_astro = H.Aout
            if j == 8:
                Iga = IGA.Septembre
                duree_astro = H.Septembre
            if j == 9:
                Iga = IGA.Octobre
                duree_astro = H.Octobre
            if j == 10:
                Iga = IGA.Novembre
                duree_astro = H.Novembre
            if j == 11:
                Iga = IGA.Decembre
                duree_astro = H.Decembre

            Ig[i][j] = Iga * (0.18 + 0.62 * (INSOLATION[i][j]) / duree_astro)


    if "Humidité" in Parameters_name:
        HUMIDITE = data_list[3]

        for i in range(len(Année)):
            for j in range(12):
                if j == 1:
                    t = 0.37        # Mois du fevrier
                else:
                    t = 0.40        # Autre mois
                if HUMIDITE[i][j] > 50:
                    PARAMETRE = 1
                else:
                    PARAMETRE = (1+((50 - HUMIDITE[i][j])/70))

                ETP[i][j] = ((TEMPERATURE[i][j]) / (15 + (TEMPERATURE[i][j])) * t * ((Ig[i][j]) + 50)) * PARAMETRE
        return ETP
    else:
        for i in range(len(Année)):
            for j in range(12):
                if j == 1:
                    t = 0.37
                else:
                    t = 0.40

                ETP[i][j] = ((TEMPERATURE[i][j]) / (15 + (TEMPERATURE[i][j])) * t * ((Ig[i][j]) + 50))

        return ETP



# na TURC na THORNTWAITE, rehefa mi-retourne str dia misy erreur
# raha tsy misy erreur dia mi-retourne nd.array na liste

def ETRTHORNTWAITE(request, RFU):
    if "logged_user_id" in request.session:
        logged_User = Person.objects.get(id=request.session["logged_user_id"])
    else:
        return "erreur"

    Uploaded_data = takedata(request)
    ETPthorn=ETPTHORNTWAITE(request)
    données = Uploaded_data[0]  # je me rappel que c'est une liste
    name = Uploaded_data[1]
    année = Uploaded_data[2]
    Temperature = données[0]
    Pluie = données[1]

    ETR = np.zeros((len(année), 12))
    RUISS = np.zeros((len(année), 12))
    DEFICIT = np.zeros((len(année), 12))
    DeltaS = np.zeros((len(année), 12))
    RFUparmois = np.zeros((len(année), 12))

    for i in name:
        if type(i) == int or type(i) == float:
            RUA = i  # RFU du dernier mois precedant l'année de calcul (nampidirina avy any amin'ny excel)
        else:
            RUA = "ts cle"
            pass
    if type(RUA) is not str:
        if RFU < RUA:
            return ("La valeur de la RUA que vous avez mentionnée dans votre fichier Excel "
                    "ne doit pas depasser la valeur de {} mm.".format(RFU))
        else:
            print("NEtYYYYY")
            RFUcalcul = RUA  # rAHA NAMPIDITRA RUA TAO ANATY EXCEL NY UTILISATEUR
            print(RFUcalcul)
            for i in range(len(année)):
                for j in range(12):

# a-Pluie >= ETP :==================================================
                    if ETPthorn[i][j] <= Pluie[i][j]:
                        ETR[i][j] = ETPthorn[i][j]
                        DEFICIT[i][j] = 0

                # EFA HITA NY ETR DU MOIS SU DEFICIT DU MOIS, RFU SY RUISS ARY VARIATION STOCK SISA =====
                        Ambiny = Pluie[i][j] - ETPthorn[i][j]
                        if RFUcalcul == RFU:  # Sol Saturé
                            RUISS[i][j] = Ambiny
                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)
                        elif RFUcalcul < RFU:  # Sol non saturé
                            Rfubanga = RFU - RFUcalcul  # Ecart entre rfu max et rfu actuel
                            if Ambiny >= Rfubanga:
                                RUISS[i][j] = Ambiny - Rfubanga
                                RFUcalcul1 = RFUcalcul + Rfubanga
                            else:
                                RFUcalcul1 = RFUcalcul + Ambiny

                            if RFUcalcul1 >= RFU:
                                RFU_DU_MOIS = RFU
                            else:
                                RFU_DU_MOIS = RFUcalcul1

                            RFUparmois[i][j] = RFU_DU_MOIS

                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFU_DU_MOIS - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]
                            RFUcalcul = RFU_DU_MOIS # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                        else:
                            pass

    # b-Pluie < ETP: ===================================================
                    else:
                        # b1- (Pluie + RFU) >= ETP :
                        A = (Pluie[i][j] + RFUcalcul)
                        if A >= ETPthorn[i][j]:
                            ETR[i][j] = ETPthorn[i][j]
                            DEFICIT[i][j] = 0

                    # EFA HITA NY ETR DU MOIS SU DEFICIT DU MOIS, RFU SY RUISS ARY VARIATION STOCK SISA
                            RFUcalcul1 = A - ETR[i][j]
                            if RFUcalcul1 > RFU:
                                RFUcalcul = RFU
                                RUISS[i][j] = RFUcalcul1 - RFU

                            else:
                                RFUcalcul = RFUcalcul1
                                RUISS[i][j] = 0

                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                        # b1- (Pluie + RFU) <= ETP :
                        else:
                            ETR[i][j] = Pluie[i][j] + RFUcalcul
                            RUISS[i][j] = 0
                            DEFICIT[i][j] = ETPthorn[i][j] - ETR[i][j]
                            RFUcalcul = 0
                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

            return ETR, RUISS, DEFICIT, DeltaS, RFUparmois
    else:

        RFUcalcul = RFU  # ito ilay parametre ao anaty fonction ETRTHORNTWAITE (nampidirina avy any amin'ny view)
        for i in range(len(année)):
            for j in range(12):
    # a-Pluie >= ETP :==================================================

                if ETPthorn[i][j] <= Pluie[i][j]:
                    ETR[i][j] = ETPthorn[i][j]
                    DEFICIT[i][j] = 0
            # EFA HITA NY ETR DU MOIS SU DEFICIT DU MOIS, RFU SY RUISS ARY VARIATION STOCK SISA
                    Ambiny = Pluie[i][j] - ETPthorn[i][j]
                    if RFUcalcul == RFU:  # Sol Saturé
                        RUISS[i][j] = Ambiny
                        RFUparmois[i][j] = RFUcalcul
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0 :
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i-1][11]
                        else:
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i][j-1]
                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                    elif RFUcalcul < RFU:  # Sol non saturé
                        Rfubanga = RFU - RFUcalcul  # Ecart entre rfu max et rfu actuel
                        if Ambiny >= Rfubanga:
                            RUISS[i][j] = Ambiny - Rfubanga
                            RFUcalcul1 = RFUcalcul + Rfubanga
                        else:
                            RFUcalcul1 = RFUcalcul + Ambiny

                        if RFUcalcul1 >= RFU:
                            RFU_DU_MOIS = RFU
                        else:
                            RFU_DU_MOIS = RFUcalcul1

                        RFUparmois[i][j] = RFU_DU_MOIS

                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0 :
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i-1][11]
                        else:
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i][j-1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                    else:
                        pass


    # b-Pluie < ETP: ===================================================
                else:
                    # b1- (Pluie + RFU) >= ETP :
                    A = (Pluie[i][j] + RFUcalcul)
                    if A >= ETPthorn[i][j]:
                        ETR[i][j] = ETPthorn[i][j]
                        DEFICIT[i][j] = 0
            # EFA HITA NY ETR DU MOIS SU DEFICIT DU MOIS, RFU SY RUISS ARY VARIATION STOCK SISA
                        RFUcalcul1 = A - ETR[i][j]
                        if RFUcalcul1 > RFU:
                            RFU_DU_MOIS = RFU
                            RUISS[i][j] = RFUcalcul1 - RFU

                        else:
                            RFU_DU_MOIS = RFUcalcul1
                            RUISS[i][j] = 0

                        RFUparmois[i][j] = RFU_DU_MOIS
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                        else:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]
                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)


                    # b1- (Pluie + RFU) <= ETP :
                    else:
                        ETR[i][j] = Pluie[i][j] + RFUcalcul
                        RUISS[i][j] = 0
                        DEFICIT[i][j] = ETPthorn[i][j] - ETR[i][j]
                        RFU_DU_MOIS = 0
                        RFUparmois[i][j] = RFU_DU_MOIS
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                        else:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

        return ETR, RUISS, DEFICIT, DeltaS , RFUparmois

def ETRTURC(request, RFU):
    if "logged_user_id" in request.session:
        logged_User = Person.objects.get(id=request.session["logged_user_id"])
    else:
        return "erreur"

    Uploaded_data = takedata(request)
    ETPturc = ETPTURC(request)
    données = Uploaded_data[0]  # je me rappel que c'est une liste
    name = Uploaded_data[1]
    année = Uploaded_data[2]
    Temperature = données[0]
    Pluie = données[1]

    ETR = np.zeros((len(année), 12))
    RUISS = np.zeros((len(année), 12))
    DEFICIT = np.zeros((len(année), 12))
    DeltaS = np.zeros((len(année), 12))
    RFUparmois = np.zeros((len(année), 12))


    for i in name:
        if type(i) == int or type(i) == float:
            RUA = i  # RFU du dernier mois precedant l'année de calcul (nampidirina avy any amin'ny excel)
        else:
            RUA = "ts cle"
            pass
    if type(RUA) is not str:
        if RFU < RUA :
            return ("La valeur de la RUA que vous avez mentionnée dans votre fichier Excel "
                    "ne doit pas depasser la valeur de {} mm.".format(RFU))
        else:
            print("NEtYYYYY")
            print(RFU)
            RFUcalcul = RUA  # ito ilay parametre ao anaty fonction ETRTHORNTWAITE (nampidirina avy any amin'ny view)
            print(RFUcalcul)
            print(RFU+RUA)
            for i in range(len(année)):
                for j in range(12):
                    # a-Pluie >= ETP :==================================================

                    if ETPturc[i][j] <= Pluie[i][j]:
                        ETR[i][j] = ETPturc[i][j]
                        DEFICIT[i][j] = 0

                        Ambiny = Pluie[i][j] - ETPturc[i][j]
                        if RFUcalcul == RFU:  # Sol Saturé
                            RUISS[i][j] = Ambiny
                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)
                        elif RFUcalcul < RFU:  # Sol non saturé
                            Rfubanga = RFU - RFUcalcul  # Ecart entre rfu max et rfu actuel
                            if Ambiny >= Rfubanga:
                                RUISS[i][j] = Ambiny - Rfubanga
                                RFUcalcul1 = RFUcalcul + Rfubanga
                            else:
                                RFUcalcul1 = RFUcalcul + Ambiny

                            if RFUcalcul1 >= RFU:
                                RFU_DU_MOIS = RFU
                            else:
                                RFU_DU_MOIS = RFUcalcul1

                            RFUparmois[i][j] = RFU_DU_MOIS

                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFU_DU_MOIS - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]
                            RFUcalcul = RFU_DU_MOIS # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                        else:
                            pass

                    # b-Pluie < ETP: ===================================================
                    else:
                        # b1- (Pluie + RFU) >= ETP :
                        A = (Pluie[i][j] + RFUcalcul)
                        if A >= ETPturc[i][j]:
                            ETR[i][j] = ETPturc[i][j]
                            DEFICIT[i][j] = 0
                            RFUcalcul1 = A - ETR[i][j]
                            if RFUcalcul1 > RFU:
                                RFUcalcul = RFU
                                RUISS[i][j] = RFUcalcul1 - RFU

                            else:
                                RFUcalcul = RFUcalcul1
                                RUISS[i][j] = 0

                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                        # b1- (Pluie + RFU) <= ETP :
                        else:
                            ETR[i][j] = Pluie[i][j] + RFUcalcul
                            RUISS[i][j] = 0
                            DEFICIT[i][j] = ETPturc[i][j] - ETR[i][j]
                            RFUcalcul = 0
                            RFUparmois[i][j] = RFUcalcul
                            if i == 0 and j == 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                            elif j == 0 and i != 0:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                            else:
                                DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                            RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

            return ETR, RUISS, DEFICIT, DeltaS, RFUparmois
    else: # TSY MISY RESERVE INITIALE DU MOIS PRECEDENT
        RFUcalcul = RFU  # ito ilay parametre ao anaty fonction ETRTHORNTWAITE (nampidirina avy any amin'ny view)
        for i in range(len(année)):
            for j in range(12):
                # a-Pluie >= ETP :==================================================

                if ETPturc[i][j] <= Pluie[i][j]:
                    ETR[i][j] = ETPturc[i][j]
                    DEFICIT[i][j] = 0

                    Ambiny = Pluie[i][j] - ETPturc[i][j]
                    if RFUcalcul == RFU:  # Sol Saturé
                        RUISS[i][j] = Ambiny
                        RFUparmois[i][j] = RFUcalcul
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0 :
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i-1][11]
                        else:
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i][j-1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)


                    elif RFUcalcul < RFU:  # Sol non saturé
                        Rfubanga = RFU - RFUcalcul  # Ecart entre rfu max et rfu actuel
                        if Ambiny >= Rfubanga:
                            RUISS[i][j] = Ambiny - Rfubanga
                            RFUcalcul1 = RFUcalcul + Rfubanga
                        else:
                            RFUcalcul1 = RFUcalcul + Ambiny

                        if RFUcalcul1 >= RFU:
                            RFU_DU_MOIS = RFU
                        else:
                            RFU_DU_MOIS = RFUcalcul1

                        RFUparmois[i][j] = RFU_DU_MOIS

                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0 :
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i-1][11]
                        else:
                            DeltaS[i][j] =  RFUparmois[i][j] - RFUparmois[i][j-1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)
                    else:
                        pass


                # b-Pluie < ETP: ===================================================
                else:
                    # b1- (Pluie + RFU) >= ETP :
                    A = (Pluie[i][j] + RFUcalcul)
                    if A >= ETPturc[i][j]:
                        ETR[i][j] = ETPturc[i][j]
                        DEFICIT[i][j] = 0
                        RFUcalcul1 = A - ETR[i][j]
                        if RFUcalcul1 > RFU:
                            RFU_DU_MOIS = RFU
                            RUISS[i][j] = RFUcalcul1 - RFU

                        else:
                            RFU_DU_MOIS = RFUcalcul1
                            RUISS[i][j] = 0

                        RFUparmois[i][j] = RFU_DU_MOIS
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                        else:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)

                    # b1- (Pluie + RFU) <= ETP :
                    else:
                        ETR[i][j] = Pluie[i][j] + RFUcalcul
                        RUISS[i][j] = 0
                        DEFICIT[i][j] = ETPturc[i][j] - ETR[i][j]
                        RFU_DU_MOIS = 0
                        RFUparmois[i][j] = RFU_DU_MOIS
                        if i == 0 and j == 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUcalcul
                        elif j == 0 and i != 0:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i - 1][11]
                        else:
                            DeltaS[i][j] = RFUparmois[i][j] - RFUparmois[i][j - 1]

                        RFUcalcul = RFUparmois[i][j] # REINITIALISATION DE LA RFU DE CALCUL(RFU DU MOIS PRECEDENT)
        return ETR, RUISS, DEFICIT, DeltaS , RFUparmois
