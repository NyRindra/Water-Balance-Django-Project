import numpy as np
from .models import Person
from openpyxl import *


def takedata(request):
    if "logged_user_id" in request.session:
        File = Person.objects.get(id=request.session['logged_user_id']).fichier # Je prends le fichier excel du visiteur
        try:
            Fileopen = load_workbook(File) # module openpyxl
        except:
            return "bad file" # Sao misy manondrana mi-renommer fichier #type str
        else:
            Sheet_names = Fileopen.sheetnames
            Sheet_working = Fileopen[Sheet_names[0]]

            année = []
            temperature = np.zeros((10, 12))
            humidité = np.zeros((10, 12))
            insolation = np.zeros((10, 12))
            precipitation = np.zeros((10, 12))



            # Prise des années de calcul
            temp_name = ["TEMPERATURE", "Température", "température", "temperature", "Temperature"]
            prec_name = ["PRECIPITATION","Précipitation", "précipitation", "precipitation", "Precipitation"]
            Station = ["Station", "STATION", "station"]
            Latitude_name = ["Latitude", "LATITUDE", "latitude"]
            Message_station =[]
            Message = []
            Latitude = []



            for i in range(1,46):
                if Sheet_working["A"+ str(i)].value in Station and (type(Sheet_working["B"+str(i)].value) is str or type(Sheet_working["B"+str(i+1)].value) is int):
                    Latitude.append(Sheet_working["B"+ str(i+2)].value)
                    #-----------------------------------------------------
                    RFUexcel = Sheet_working["B"+ str(i+3)].value
                    try :
                        t = int(RFUexcel)
                    except TypeError:
                        RUA = "tsy cle"
                        pass
                    except ValueError:
                        RUA = "tsy cle"
                        pass
                    else:
                        RUA = RFUexcel
                    #------------------------------------------------------
                    if type(Sheet_working["B"+str(i)].value) is str :
                        station = Sheet_working["B"+str(i)].value
                    elif type(Sheet_working["B"+str(i+1)].value) is int :
                        station = Sheet_working["B" + str(i)].value

                    break # Mamaly ilay condition if Sheet_working (izany hoe raha tanteraka io condition if io izay vao break)
                else:
                    pass
            if not Latitude:
                Message_station.append("Veuillez mentionner le nom ou le code de la station")
            if len(Latitude)>0:
                try:
                    x = int(Latitude[0])
                except TypeError: # Case vide
                    Message_station.append("La latitude est obligatoire")
                except ValueError:
                    Message_station.append("La latitude doit être un nombre")
            if len(Message_station) > 0:
                return Message_station
            else:
                pass

            compteur_de_ligne = 0
            for i in range(1,46):

                getyear = Sheet_working["A"+ str(i)].value
                if type(getyear) is not int:
                    pass
                    i += 1

                else:
                    if Sheet_working["B"+str(i)].value not in temp_name:
                        Message_d_erreur = "Veuillez mettre les années de calculs dans la" \
                                           " colonne A, directement à gauche des noms TEMPERATURE "
                        Message.append(Message_d_erreur)
                    else:
                        année.append(getyear)
                        try:
                            T1 = Sheet_working["C" + str(i)].value
                            T2 = Sheet_working["D" + str(i)].value
                            T3 = Sheet_working["E" + str(i)].value
                            T4 = Sheet_working["F" + str(i)].value
                            T5 = Sheet_working["G" + str(i)].value
                            T6 = Sheet_working["H" + str(i)].value
                            T7 = Sheet_working["I" + str(i)].value
                            T8 = Sheet_working["J" + str(i)].value
                            T9 = Sheet_working["K" + str(i)].value
                            T10 = Sheet_working["L" + str(i)].value
                            T11 = Sheet_working["M" + str(i)].value
                            T12 = Sheet_working["N" + str(i)].value

                            temperature[compteur_de_ligne] = [T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11,T12]

                            P1 = Sheet_working["C" + str(i + 1)].value
                            P2 = Sheet_working["D" + str(i + 1)].value
                            P3 = Sheet_working["E" + str(i + 1)].value
                            P4 = Sheet_working["F" + str(i + 1)].value
                            P5 = Sheet_working["G" + str(i + 1)].value
                            P6 = Sheet_working["H" + str(i + 1)].value
                            P7 = Sheet_working["I" + str(i + 1)].value
                            P8 = Sheet_working["J" + str(i + 1)].value
                            P9 = Sheet_working["K" + str(i + 1)].value
                            P10 = Sheet_working["L" + str(i + 1)].value
                            P11 = Sheet_working["M" + str(i + 1)].value
                            P12 = Sheet_working["N" + str(i + 1)].value

                            precipitation[compteur_de_ligne] = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12]

                            I1 = Sheet_working["C" + str(i + 2)].value
                            I2 = Sheet_working["D" + str(i + 2)].value
                            I3 = Sheet_working["E" + str(i + 2)].value
                            I4 = Sheet_working["F" + str(i + 2)].value
                            I5 = Sheet_working["G" + str(i + 2)].value
                            I6 = Sheet_working["H" + str(i + 2)].value
                            I7 = Sheet_working["I" + str(i + 2)].value
                            I8 = Sheet_working["J" + str(i + 2)].value
                            I9 = Sheet_working["K" + str(i + 2)].value
                            I10 = Sheet_working["L" + str(i + 2)].value
                            I11 = Sheet_working["M" + str(i + 2)].value
                            I12 = Sheet_working["N" + str(i + 2)].value

                            insolation[compteur_de_ligne] = [I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11, I12]

                            H1 = Sheet_working["C" + str(i + 3)].value
                            H2 = Sheet_working["D" + str(i + 3)].value
                            H3 = Sheet_working["E" + str(i + 3)].value
                            H4 = Sheet_working["F" + str(i + 3)].value
                            H5 = Sheet_working["G" + str(i + 3)].value
                            H6 = Sheet_working["H" + str(i + 3)].value
                            H7 = Sheet_working["I" + str(i + 3)].value
                            H8 = Sheet_working["J" + str(i + 3)].value
                            H9 = Sheet_working["K" + str(i + 3)].value
                            H10 = Sheet_working["L" + str(i + 3)].value
                            H11 = Sheet_working["M" + str(i + 3)].value
                            H12 = Sheet_working["N" + str(i + 3)].value

                            humidité[compteur_de_ligne] = [H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12]

                        except ValueError: # Erreur de saisie ( caractères spéciaux au lieu d'un float )
                            Message_d_erreur="Erreur de saisie dans les données : année {}".format(getyear)
                            Message.append(Message_d_erreur)
                        else:
                            compteur_de_ligne += 1
                            i += 1
            if len(année) == 0 :
                Message1 = ["Aucune date trouvée(s) dans votre fichier excel"]
                return Message1

            elif len(Message)>0:
                return Message
            else:

                temp_nan = np.argwhere(np.isnan(temperature))       # retourne un array indiquant l'indice [i][j]
                prec_nan = np.argwhere(np.isnan(precipitation))     # des NAN value
                ins_nan = np.argwhere(np.isnan(insolation))         # ex : ( temp_nan = array [[0,1], [1,4]] )
                hum_nan = np.argwhere(np.isnan(humidité))

                Nan = [temp_nan, prec_nan, ins_nan, hum_nan]
                data_list = [temperature, precipitation,  insolation, humidité]
                data_name = ["Température", "Précipitation", "Insolation", "Humidité"]

                full_data = []

                for i in range(4):

                    Données = (Nan[i], data_list[i], data_name[i])
                    full_data.append(Données)
                    # full_data = [(temp_nan, temperature), (prec_nan, temperature), ...]

                # TEST CELLULE VIDE
                Message2 = []
                for nan_list in Nan:
                    if (len(nan_list)>0) and (len(nan_list) != 12*len(année)):
                        Message2.append("Cellule(s) vide(s) trouvées : Année {}".format(année[nan_list[0][0]]))
                if Message2:
                    return Message2
                else:
                    indice = []
                    for i in range(len(full_data)):
                        tuple = full_data[i]
                        if len(tuple[0]) == 12 * len(année): # mIDIKA FA VIDE DAHOLO
                            indice.append(i)

                    retour_data = []
                    retour_data_name = []
                    if len(indice) != 0 :
                        index_des_données = [0,1,2,3]
                        for element in index_des_données:
                            if element in indice: # raha vide daholo dia tsy raisina
                                pass
                            else:
                                retour_data.append(data_list[element])
                                retour_data_name.append(data_name[element])

                    else:
                        for i in range(4):
                            retour_data.append(data_list[i])
                            retour_data_name.append(data_name[i])

                    retour_data_name.append(station)
                    if type(RUA) is not str:
                        retour_data_name.append(RUA)
                    else:
                        pass
                    return retour_data, retour_data_name, année, Latitude

    else:
        return None
# RESUME
# Raha tsy misy année ao am excel dia tsy mahita donnée:
    # return ["Aucune date trouvé"] ... ligne 138

# Raha misy années fa tsy mifanitsy @ colonne Temperature: ... ligne 65
    # return ["Veuillez mettre les années de calculs dans la colonne A, directement à gauche des noms TEMPERATURE"

# Raha misy années fa nanao erreur de saisie
    # return ["Erreur de saisie dans les données : année ... "] ligne 111, appelé à la ligne 121

# Raha misy années fa misy case vide (adino ny nameno azy ohatra)
    # return ["Cellule(s) vide(s) trouvées : Année ... "] ligne 148

    # Raha case vide = 12* len(années)
        # tonga dia tsy ajouté ao anaty retour ilay donnée
        # ohatra hoe len(temperature) = 12*len(année) : tsy misy liste-na temperature miverina any rehefa miantso
        # fonction dataupload

# raha mi retourne list na str ito fonction ito dia misy erreur
# raha tsy misy erreur dia mi-retourner tuple ()