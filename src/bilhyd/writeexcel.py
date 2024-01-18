#code utf-8
from .calcul import *
from .models import Person
from .dataupload import takedata
import xlwt
def excelthorn(request):
    if "logged_user_id" in request.session:
        logged_User = Person.objects.get(id=request.session["logged_user_id"])
        RFU = logged_User.RFU
        globaldata1 = ETPTHORNTWAITE(request)  # ETP fotsiny ny ato
        globaldata2 = ETRTHORNTWAITE(request, RFU)
        Données = takedata(request)
        Dataname = Données[1]
        DATA = Données[0]
        Precipitation = DATA[1]

        for i in Dataname:
            if type(i) == float or type(i) == int:
                compteur = 1
            else:
                compteur = "ts cle"
                pass
        if type(compteur) is not str:
            Station_Name_Code = Dataname[-2]   # type str
        else:
            Station_Name_Code = Dataname[-1]
        print("STATION NAME CODE")
        print(Station_Name_Code)
        Années = Données[2]                 #liste ito
        ETP = globaldata1
        ETR = globaldata2[0]
        Ruissellement = globaldata2[1]
        Deficit = globaldata2[2]
        VariationStock = globaldata2[3]
        RFUmensuel = globaldata2[4]
        mois = ['Janvier', 'Fevrier', "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre",
                "Octobre", "Novembre", "Decembre"]

        book = xlwt.Workbook(encoding="utf-8") # creation d'un classeur(format xls) via xlwt
# ----- STYLE FONT ----------------------------
        Font = xlwt.Font()
        Font.name = "Times New Roman"
        Font.colour_index = 0
        Font.bold = True
        style = xlwt.XFStyle()
        style.font = Font

        Font1 = xlwt.Font()
        Font1.name = "Times New Roman"
        Font1.colour_index = 2
        Font1.bold = True
        style1 = xlwt.XFStyle()
        style1.font = Font1
# ----------------------------------------------
        # 1 - Feuille 1 BILAN ANNUEL ---------------------------
        sheet = book.add_sheet("Bilan annuel")
        sheet.write(0, 0, Station_Name_Code, style)
        t = 1
        for value in Années:
            sheet.write(0,t, value, style)
            t += 1
        sheet.write(1, 0, "ETP", style)
        sheet.write(2, 0, "ETR", style)
        sheet.write(3, 0, "Ruissellement", style)
        sheet.write(4, 0, "Deficit", style)
        sheet.write(5, 0, "Variation des stocks", style)
        sheet.write(6, 0, "RFU", style)
        sheet.write(7, 0, "RFUmax", style1)
        sheet.write(7, 1, logged_User.RFU, style1)

        # pour mettre les ETP annuel (les elements dans chaque liste sera au nombre des années de calcul)
        etpsum = []
        etrsum = []
        ruiss_sum = []
        deficit_sum = []
        Variat_stock_sum = []
        rfuannuel_sum = []

        for i in range(len(Années)):
            etp_i = sum(ETP[i].tolist())  # Sommation de chaque ETP mensuel pour avoir un ETP annuel
            etr_i = sum(ETR[i].tolist())  # (de meme pour les ETR, RUISS et autre)
            ruiss_i = sum(Ruissellement[i].tolist())
            deficit_i = sum(Deficit[i].tolist())
            Variat_stock_i = sum(VariationStock[i].tolist())
            rfuannuel_i = sum(RFUmensuel[i].tolist())

            sheet.write(1, i + 1, etp_i)
            sheet.write(2, i + 1, etr_i)
            sheet.write(3, i + 1, ruiss_i)
            sheet.write(4, i + 1, deficit_i)
            sheet.write(5, i + 1, Variat_stock_i)
            sheet.write(6, i + 1, rfuannuel_i)

            # Utile pour l'affichage des resultats annuel
            etpsum.append(etp_i)
            etrsum.append(etr_i)
            ruiss_sum.append(ruiss_i)
            deficit_sum.append(deficit_i)
            Variat_stock_sum.append(Variat_stock_i)
            rfuannuel_sum.append(rfuannuel_i)

        annual_result = [etpsum, etrsum, ruiss_sum, deficit_sum, Variat_stock_sum, rfuannuel_sum]

        for i in range(len(Années)):
            sheet = book.add_sheet("{}".format(Années[i]))

            # ligne 1
            sheet.write(0,0, Station_Name_Code, style)
            t = 1
            for value in mois:
                sheet.write(0, t, value , style)
                t += 1

            # ligne 2
            sheet.write(1, 0, "Précipitation", style)
            sheet.write(2, 0, "ETP", style)
            sheet.write(3, 0, "ETR", style)
            sheet.write(4, 0, "Ruissellement", style)
            sheet.write(5, 0, "Deficit", style)
            sheet.write(6, 0, "Variation des stocks", style)
            sheet.write(7, 0, "RFU", style)
            sheet.write(8, 0, "RFUmax", style1)
            sheet.write(8, 1, logged_User.RFU, style1)


            compteur = 0
            prec = Precipitation[i].tolist()
            etp = ETP[i].tolist()
            etr = ETR[i].tolist()
            ruiss = Ruissellement[i].tolist()
            deficit = Deficit[i].tolist()
            Variat_stock = VariationStock[i].tolist()
            rfuparmois = RFUmensuel[i].tolist()
            for j in range(12):

                compteur += 1
                sheet.write(1, compteur, prec[j])
                sheet.write(2, compteur , etp[j])
                sheet.write(3, compteur, etr[j])
                sheet.write(4, compteur, ruiss[j])
                sheet.write(5, compteur, deficit[j])
                sheet.write(6, compteur, Variat_stock[j])
                sheet.write(7, compteur, rfuparmois[j])

        book.save("User_data/User_data_download/Station{}--BILHYD-THORNTWAITE.xls".format(Station_Name_Code))
        logged_User.fichiercalculé ="User_data/User_data_download/Station{}--BILHYD-THORNTWAITE.xls".format(Station_Name_Code)
        logged_User.save()
        return annual_result

def excelturc(request):
    if "logged_user_id" in request.session:

        logged_User = Person.objects.get(id=request.session["logged_user_id"])
        RFU = logged_User.RFU
        globaldata1 = ETPTURC(request)  # ETP fotsiny ny ato
        globaldata2 = ETRTURC(request, RFU)
        Données = takedata(request)
        Dataname = Données[1]
        DATA = Données[0]
        Precipitation = DATA[1]

        for i in Dataname:
            if type(i) == float or type(i) == int:
                compteur = 1
            else:
                compteur = "ts cle"
                pass
        if type(compteur) is not str:
            Station_Name_Code = Dataname[-2]  # type str
        else:
            Station_Name_Code = Dataname[-1]
        print("STATION NAME CODE")
        print(Station_Name_Code)
        Années = Données[2]                 #liste ito
        ETP = globaldata1
        ETR = globaldata2[0]
        Ruissellement = globaldata2[1]
        Deficit = globaldata2[2]
        VariationStock = globaldata2[3]
        RFUmensuel = globaldata2[4]
        mois = ['Janvier', 'Fevrier', "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre",
                "Octobre", "Novembre", "Decembre"]

        book = xlwt.Workbook(encoding="utf-8")
# ----- STYLE FONT -------------------------
        Font = xlwt.Font()
        Font.name = "Times New Roman"
        Font.colour_index = 0
        Font.bold = True
        style = xlwt.XFStyle()
        style.font = Font

        Font1 = xlwt.Font()
        Font1.name = "Times New Roman"
        Font1.colour_index = 2
        Font1.bold = True
        style1 = xlwt.XFStyle()
        style1.font = Font1
# -------------------------------------------

        # 1 - Feuille 1 BILAN ANNUEL ---------------------------
        sheet = book.add_sheet("Bilan annuel")
        t = 1
        for value in Années:
            sheet.write(0, t, value, style)
            t += 1
        sheet.write(1, 0, "ETP", style)
        sheet.write(2, 0, "ETR", style)
        sheet.write(3, 0, "Ruissellement", style)
        sheet.write(4, 0, "Deficit", style)
        sheet.write(5, 0, "Variation des stocks", style)
        sheet.write(6, 0, "RFU", style)
        sheet.write(7, 0, "RFUmax", style1)
        sheet.write(7, 1, logged_User.RFU , style1)

        # pour mettre les ETP annuel (les elements dans chaque liste sera au nombre des années de calcul)
        etpsum = []
        etrsum = []
        ruiss_sum = []
        deficit_sum = []
        Variat_stock_sum = []
        rfuannuel_sum = []


        for i in range(len(Années)):
            etp_i = sum(ETP[i].tolist())    # Sommation de chaque ETP mensuel pour avoir un ETP annuel
            etr_i = sum(ETR[i].tolist())    # (de meme pour les ETR, RUISS et autre)
            ruiss_i = sum(Ruissellement[i].tolist())
            deficit_i = sum(Deficit[i].tolist())
            Variat_stock_i = sum(VariationStock[i].tolist())
            rfuannuel_i = sum(RFUmensuel[i].tolist())

            sheet.write(1, i+1, etp_i)
            sheet.write(2, i+1, etr_i)
            sheet.write(3, i+1, ruiss_i)
            sheet.write(4, i+1, deficit_i)
            sheet.write(5, i+1, Variat_stock_i)
            sheet.write(6, i+1, rfuannuel_i)

            # Utile pour l'affichage des resultats annuel
            etpsum.append(etp_i)
            etrsum.append(etr_i)
            ruiss_sum.append(ruiss_i)
            deficit_sum.append(deficit_i)
            Variat_stock_sum.append(Variat_stock_i)
            rfuannuel_sum.append(rfuannuel_i)

        annual_result = [etpsum, etrsum, ruiss_sum, deficit_sum, Variat_stock_sum, rfuannuel_sum]

        # 2 Autre feuilles, BILAN MENSUEL -----------------------------------
        for i in range(len(Années)):
            sheet = book.add_sheet("{}".format(Années[i]))

            # ligne 1
            sheet.write(0,0, Station_Name_Code)
            t = 1
            for value in mois:
                sheet.write(0, t, value , style)
                t += 1

            # ligne 2
            sheet.write(1, 0, "Précipitation", style)
            sheet.write(2, 0, "ETP", style)
            sheet.write(3, 0, "ETR", style)
            sheet.write(4, 0, "Ruissellement", style)
            sheet.write(5, 0, "Deficit", style)
            sheet.write(6, 0, "Variation des stocks", style)
            sheet.write(7, 0, "RFU", style)
            sheet.write(8, 0, "RFUmax", style1)
            sheet.write(8, 1, logged_User.RFU, style1)


            compteur = 0
            prec = Precipitation[i].tolist()
            etp = ETP[i].tolist()
            etr = ETR[i].tolist()
            ruiss = Ruissellement[i].tolist()
            deficit = Deficit[i].tolist()
            Variat_stock = VariationStock[i].tolist()
            rfuparmois = RFUmensuel[i].tolist()
            for j in range(12):

                compteur += 1
                sheet.write(1, compteur, prec[j])
                sheet.write(2, compteur, etp[j])
                sheet.write(3, compteur, etr[j])
                sheet.write(4, compteur, ruiss[j])
                sheet.write(5, compteur, deficit[j])
                sheet.write(6, compteur, Variat_stock[j])
                sheet.write(7, compteur, rfuparmois[j])


        book.save("User_data/User_data_download/Station{}--BILHYD-TURC.xls".format(Station_Name_Code))
        logged_User.fichiercalculé ="User_data/User_data_download/Station{}--BILHYD-TURC.xls".format(Station_Name_Code)
        logged_User.save()


        return annual_result