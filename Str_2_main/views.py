import csv
import os
import urllib

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .models import Nazwy_spółek, Dane_spółek, Popular
from math import sqrt
from datetime import date
from django.db.models import Sum


# Create your views here.
def likeDane(request):
    if request.method == "POST":
        name_spolka_do_analizy_ver1 = request.POST["title"]
        k = str(name_spolka_do_analizy_ver1)
        print("Tworzymy obiekt")
        w = Nazwy_spółek.objects.filter(spolka_data_skrot=k)
        h=w[0]
        print(h)

        vote_count = Popular.objects.count()
        if (vote_count <= 3):
            print("Przepełenienie brak ")
        else:
            k = 0

            for i in Popular.objects.all():
                if k == 0:
                    print("too")
                    print(i)
                    print(i)
                    i.delete();
                    k = k + 1
                    print("Obiket został usunięty")


        Popular.objects.create(popular_name=h, popular_skrot=k)
        # z=str(w)
        # print(z)
        # vote_count = Popular.objects.count()


        print(Popular.objects.all())

        # z = w['spolka_data_name']
        # str(z)
        # print(z)
        # nazwa=w.spolka_data_name
        # print(nazwa)
        # Popular.objects.create(popular_name="b", popular_skrot="d")

        return redirect(menu)
    else:
        return render(request, "result.html")


def menu(request):
    # pobieranie_gieldy()
    # Dodaj petle sprawdz czy jest
    # if request.method=="POST":
    #     print("dddd")

    all_Data = []
    # download_data_name(all_Data)

    # context = {'data': all_Data}

    for data in all_Data:
        if Nazwy_spółek.objects.filter(spolka_data_name=data['Nazwa'],
                                       spolka_data_skrot=data['Symbol']).exists() == False:
            Nazwy_spółek.objects.create(spolka_data_name=data['Nazwa'], spolka_data_skrot=data['Symbol'])
    baza = Nazwy_spółek.objects.all()
    popular = Popular.objects.all()

    listaPopular = []
    listaPopular.append(Popular.objects.all())
    # print(Popular.objects.all()[:1])



    top = Popular.objects.all()



    baza = {'data': baza,
            'top': top}
    print("ggg")

    return render(request, "Strona_2.html", baza)


def odp2(request):
    name_spolka_do_analizy_ver1 = request.GET["spółka_do_analizy_ver1"]

    name_spolka_do_analizy_ver2 = request.GET["spółka_do_analizy_ver2"]

    name2 = str(szukanie(name_spolka_do_analizy_ver2))
    name1 = str(szukanie(name_spolka_do_analizy_ver1))

    if (name1 != 'None'):
        flaga = True
    else:
        flaga = False
    if (name2 != 'None'):
        flaga = True
    else:
        flaga = False

    if flaga == True:

        www_ver1 = 'https://stooq.pl/q/d/l/?s=' + name1 + '&i=d'
        www_ver2 = 'https://stooq.pl/q/d/l/?s=' + name2 + '&i=d'

        odp1 = download(www_ver1, name1)
        odp2 = download(www_ver2, name2)

        dane1 = pd.read_csv(odp1, sep=',',
                            na_values=" ").dropna()
        dane2 = pd.read_csv(odp2, sep=',',
                            na_values=" ").dropna()

        a = dane1;
        b = dane2;

        all_Data1 = []
        all_Data2 = []

        for i in range(a.shape[0]):
            temp = a.iloc[i]
            all_Data1.append(dict(temp))

        for i in range(b.shape[0]):
            temp = b.iloc[i]
            all_Data2.append(dict(temp))

    baza = Nazwy_spółek.objects.all()
    top = Popular.objects.all()
    context = {
        'flaga': flaga,
        'data': baza,
        'name1': name1,
        'name2': name2,
        'top': top,

    }
    if (flaga == True):
        del all_Data1[-1]
        del all_Data2[-1]

        ver1 = Nazwy_spółek.objects.get(spolka_data_skrot=name1)
        ver2 = Nazwy_spółek.objects.get(spolka_data_skrot=name2)

        for data in all_Data1:
            if Dane_spółek.objects.filter(spolka_name=ver1,
                                          spolka_data=data["b'Data"]).exists() == False:
                Dane_spółek.objects.create(spolka_name=ver1,
                                           spolka_otwarcie=data['Otwarcie'],
                                           spolka_najwyzszy=data['Najwyzszy'],
                                           spolka_najnizszy=data['Najnizszy'],
                                           spolka_zamkniecie=data['Zamkniecie'],
                                           spolka_data=data["b'Data"])
        for data in all_Data2:
            if Dane_spółek.objects.filter(spolka_name=ver2,
                                          spolka_data=data["b'Data"]).exists() == False:
                Dane_spółek.objects.create(spolka_name=ver2,
                                           spolka_otwarcie=data['Otwarcie'],
                                           spolka_najwyzszy=data['Najwyzszy'],
                                           spolka_najnizszy=data['Najnizszy'],
                                           spolka_zamkniecie=data['Zamkniecie'],
                                           spolka_data=data["b'Data"])

        dane_1 = Dane_spółek.objects.all().filter(spolka_name=ver1)
        dane_2 = Dane_spółek.objects.all().filter(spolka_name=ver2)
        # /////////////////////
        Mx1 = srednia(dane1['Otwarcie'])
        My1 = timesrednia(len(dane1))

        # My1 = srednia(dane1)

        Mx2 = srednia(dane2['Otwarcie'])
        My2 = timesrednia(len(dane2))

        # My1 = srednia(dane1)

        Sx1 = odchylenie(dane1['Otwarcie'], Mx1)
        Sy1 = odchylenieczas(len(dane1), My1)
        Sx2 = odchylenie(dane2['Otwarcie'], Mx2)
        Sy2 = odchylenieczas(len(dane2), My2)

        # n = len(dane1['Otwarcie'])
        # vr = pd.DataFrame(dane1[:])
        # vry2 = sumowanie2(len(dane1))
        # vrxy = sumowanie(len(dane1), dane1['Otwarcie'])
        # vrx2 = dane1['Otwarcie'] * dane1['Otwarcie']
        # sumx = dane1['Otwarcie'].sum()

        today = date.today()





















        dane_akt_1 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year=today.year - 1)
        dane_akt_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year=today.year - 1)




        flaga20 = False
        flaga19 = False
        flaga18 = False

        if Dane_spółek.objects.filter(spolka_name=ver1,spolka_data__year='2020').exists() == True:
            dane_2020 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2020')
            flaga20=True
        if Dane_spółek.objects.filter(spolka_name=ver1, spolka_data__year='2019').exists() == True:
            dane_2019 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2019')
            flaga19 = True
        if Dane_spółek.objects.filter(spolka_name=ver1, spolka_data__year='2018').exists() == True:
            dane_2018 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2018')
            flaga18 = True


        flaga20s = False
        flaga19s = False
        flaga18s = False

        if Dane_spółek.objects.filter(spolka_name=ver2,spolka_data__year='2020').exists() == True:
            dane_2020_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2020')
            flaga20s=True
        if Dane_spółek.objects.filter(spolka_name=ver2, spolka_data__year='2019').exists() == True:
            dane_2019_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2019')
            flaga19s = True
        if Dane_spółek.objects.filter(spolka_name=ver2, spolka_data__year='2018').exists() == True:
            dane_2018_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2018')
            flaga18s = True






        # dane_2020 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2020')
        # dane_2019 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2019')
        # dane_2018 = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year='2018')





        if(flaga20==True):
            sum2020 = dane_2020.count()
            op2020 = dane_2020.aggregate(Sum('spolka_najwyzszy'))
            op20202 = dane_2020.aggregate(Sum('spolka_najnizszy'))
            ost = (op2020['spolka_najwyzszy__sum'] - op20202['spolka_najnizszy__sum']) / sum2020
        else:
            ost=0

        if (flaga19 == True):
            sum1 = dane_2019.count()
            op1 = dane_2019.aggregate(Sum('spolka_najwyzszy'))
            op2 = dane_2019.aggregate(Sum('spolka_najnizszy'))
            kk = (op1['spolka_najwyzszy__sum'] - op2['spolka_najnizszy__sum']) / sum1

        else:
            kk=0


        if (flaga18 == True):
            sum8 = dane_2018.count()
            op8 = dane_2018.aggregate(Sum('spolka_najwyzszy'))
            op81 = dane_2018.aggregate(Sum('spolka_najnizszy'))
            k8 = (op8['spolka_najwyzszy__sum'] - op81['spolka_najnizszy__sum']) / sum8

        else:
            k8=0






        # dane_2020_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2020')
        # dane_2019_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2019')
        # dane_2018_2 = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year='2018')







        if(flaga20s==True):
            sum20201 = dane_2020_2.count()
            op2020v = dane_2020_2.aggregate(Sum('spolka_najwyzszy'))
            op22020v = dane_2020_2.aggregate(Sum('spolka_najnizszy'))
            ost1 = (op2020v['spolka_najwyzszy__sum'] - op22020v['spolka_najnizszy__sum']) / sum20201

        else:
            ost1=0

        if (flaga19s == True):
            sum12 = dane_2019_2.count()
            op12 = dane_2019_2.aggregate(Sum('spolka_najwyzszy'))
            op22 = dane_2019_2.aggregate(Sum('spolka_najnizszy'))
            ws = (op12['spolka_najwyzszy__sum'] - op22['spolka_najnizszy__sum']) / sum12


        else:
            ws=0


        if (flaga18s == True):
            sum82 = dane_2018_2.count()
            op82 = dane_2018_2.aggregate(Sum('spolka_najwyzszy'))
            op821 = dane_2018_2.aggregate(Sum('spolka_najnizszy'))
            w8 = (op82['spolka_najwyzszy__sum'] - op821['spolka_najnizszy__sum']) / sum82

        else:
            w8=0







        #
        # k = 2020;
        # pusta_lista = []
        # for i in range(10):
        #     str(k)
        #     dane_x = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year=k)
        #     k = int(k - 1);
        #     sumx = dane_x.count()
        #     opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
        #     op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
        #     ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
        #     pusta_lista.append(ost)
        # print(pusta_lista)


        k = 2020;
        pusta_lista = []
        if ( flaga20 and flaga19 and flaga18 ==True):
            for i in range(10):
                str(k)
                if Dane_spółek.objects.filter(spolka_name=ver1, spolka_data__year=k).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year=k)
                    k = int(k - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista.append(ost)
                else:
                    k = int(k - 1);
                    ost=0
                    pusta_lista.append(ost)


        else:
            for i in range(10):


                str(k)
                if Dane_spółek.objects.filter(spolka_name=ver1, spolka_data__year=k).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=ver1, spolka_data__year=k)


                    k = int(k - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista.append(ost)
                else:
                    k = int(k - 1);
                    ost=0
                    pusta_lista.append(ost)







        w = 2020

        pusta_lista2 = []
        # for i in range(10):
        #     str(w)
        #     dane_x = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year=k)
        #     w = int(w - 1);
        #     sumx = dane_x.count()
        #     opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
        #     op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
        #     ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
        #     pusta_lista2.append(ost)
        if ( flaga20s and flaga19s and flaga18s ==True):
            for i in range(10):
                str(w)
                if Dane_spółek.objects.filter(spolka_name=ver2, spolka_data__year=w).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year=w)
                    w = int(w - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))

                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista2.append(ost)
                else:
                    w = int(w - 1);
                    ost=0
                    pusta_lista2.append(ost)


        else:
            for i in range(10):


                str(w)
                if Dane_spółek.objects.filter(spolka_name=ver2, spolka_data__year=w).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=ver2, spolka_data__year=w)


                    w = int(w - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista2.append(ost)
                else:
                    w = int(w - 1);
                    ost=0
                    pusta_lista2.append(ost)















        # sum2020 = dane_2020.count()
        # op2020 = dane_2020.aggregate(Sum('spolka_najwyzszy'))
        # op20202 = dane_2020.aggregate(Sum('spolka_najnizszy'))
        # ost = (op2020['spolka_najwyzszy__sum'] - op20202['spolka_najnizszy__sum']) / sum2020


        #
        # sum1 = dane_2019.count()
        # op1 = dane_2019.aggregate(Sum('spolka_najwyzszy'))
        # op2 = dane_2019.aggregate(Sum('spolka_najnizszy'))
        # k = (op1['spolka_najwyzszy__sum'] - op2['spolka_najnizszy__sum']) / sum1
        # print(k)

        # sum12 = dane_2019_2.count()
        # op12 = dane_2019_2.aggregate(Sum('spolka_najwyzszy'))
        # op22 = dane_2019_2.aggregate(Sum('spolka_najnizszy'))
        # w = (op12['spolka_najwyzszy__sum'] - op22['spolka_najnizszy__sum']) / sum12
        # print(w)

        # sum8 = dane_2018.count()
        # op8 = dane_2018.aggregate(Sum('spolka_najwyzszy'))
        # op81 = dane_2018.aggregate(Sum('spolka_najnizszy'))
        # k8 = (op8['spolka_najwyzszy__sum'] - op81['spolka_najnizszy__sum']) / sum8
        # print(k8)
        #
        # sum82 = dane_2018_2.count()
        # op82 = dane_2018_2.aggregate(Sum('spolka_najwyzszy'))
        # op821 = dane_2018_2.aggregate(Sum('spolka_najnizszy'))
        # w8 = (op82['spolka_najwyzszy__sum'] - op821['spolka_najnizszy__sum']) / sum82
        # print(w8)
        print(kk)
        print(ws)
        print(k8)
        print(w8)
        print(ost)
        print(ost1)



        dane2 = {
            'dane_1': dane_1,
            'dane_2': dane_2,
            'nazwa_1': name1,
            'nazwa_2': name2,
            'Mx1': Mx1,
            'Mx2': Mx2,
            'My1': My1,
            'My2': My2,
            'Sx1': Sx1,
            'Sx2': Sx2,
            'Sy1': Sy1,
            'Sy2': Sy2,
            'dane_2020': dane_2020,
            'dane_2019': dane_2019,
            'dane_2018': dane_2018,
            'dane_2020_2': dane_2020_2,
            'dane_2019_2': dane_2019_2,
            'dane_2018_2': dane_2018_2,
            'zm': kk,
            'zm2': ws,
            'zm8': k8,
            'zm28': w8,
            'ww': ost,
            'ww2': ost1,
            'lis1': pusta_lista,
            'lis2': pusta_lista2,

            'dane_akt_1': dane_akt_1,
            'dane_akt_2': dane_akt_2,

        }

        # dane = Dane_spółek.objects.all()

        return render(request, "Strona_3_ver2.html", dane2)
    else:
        return render(request, "Strona_2.html", context=context)


def odp(request):
    name_spolka_do_analizy = request.GET["spółka_do_analizy"]

    name = str(szukanie(name_spolka_do_analizy))
    ostatnie = name
    www = 'https://stooq.pl/q/d/l/?s=' + name + '&i=d'
    odp = download(www, name)

    dane = pd.read_csv(odp).dropna()
    dane.rename(columns={'Wolumen\\r': 'Wolumen'}, inplace=True)

    # for index, row in dane.iterrows():
    #     if row['Wolumen'].str.find(sub)==True:
    #         print(row['Wolumen'])
    #
    # print(dane.head(82))
    # return render(request, "Strona_2.html")
    zam = dane;

    a = dane;

    all_Data = []
    for i in range(a.shape[0]):
        temp = a.iloc[i]
        all_Data.append(dict(temp))

    if (name != 'None'):
        flaga = True
    else:
        flaga = False
    baza = Nazwy_spółek.objects.all()
    top = Popular.objects.all()
    context = {
        'flaga': flaga,
        'data': baza,
        'name': name,
        'top': top,
    }

    # Gdy nie ma pustej listy to tworzony jest do bazy danych nowy projekt
    if (flaga == True):
        del all_Data[-1]

        nazwa = Nazwy_spółek.objects.get(spolka_data_skrot=name)

        for data in all_Data:
            if Dane_spółek.objects.filter(spolka_name=nazwa,
                                          spolka_data=data["b'Data"]).exists() == False:
                Dane_spółek.objects.create(spolka_name=nazwa,
                                           spolka_otwarcie=data['Otwarcie'],
                                           spolka_najwyzszy=data['Najwyzszy'],
                                           spolka_najnizszy=data['Najnizszy'],
                                           spolka_zamkniecie=data['Zamkniecie'],
                                           spolka_data=data["b'Data"])

        dane = Dane_spółek.objects.all().filter(spolka_name=nazwa)
        flaga20=False
        flaga19=False
        flaga18=False

        if Dane_spółek.objects.filter(spolka_name=nazwa,spolka_data__year='2020').exists() == True:
            dane_2020 = Dane_spółek.objects.all().filter(spolka_name=nazwa, spolka_data__year='2020')
            flaga20=True
        if Dane_spółek.objects.filter(spolka_name=nazwa, spolka_data__year='2019').exists() == True:
            dane_2019 = Dane_spółek.objects.all().filter(spolka_name=nazwa, spolka_data__year='2019')
            flaga19 = True
        if Dane_spółek.objects.filter(spolka_name=nazwa, spolka_data__year='2018').exists() == True:
            dane_2018 = Dane_spółek.objects.all().filter(spolka_name=nazwa, spolka_data__year='2018')
            flaga18 = True









        k = 2020;
        pusta_lista = []
        if ( flaga20 and flaga19 and flaga18 ==True):
            for i in range(10):
                str(k)
                if Dane_spółek.objects.filter(spolka_name=nazwa, spolka_data__year=k).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=nazwa, spolka_data__year=k)
                    k = int(k - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista.append(ost)
                else:
                    k = int(k - 1);
                    ost=0
                    pusta_lista.append(ost)


        else:
            for i in range(10):


                str(k)
                if Dane_spółek.objects.filter(spolka_name=nazwa, spolka_data__year=k).exists() == True:
                    dane_x = Dane_spółek.objects.all().filter(spolka_name=nazwa, spolka_data__year=k)


                    k = int(k - 1);
                    sumx = dane_x.count()
                    opx = dane_x.aggregate(Sum('spolka_najwyzszy'))
                    op2x = dane_x.aggregate(Sum('spolka_najnizszy'))
                    ost = (opx['spolka_najwyzszy__sum'] - op2x['spolka_najnizszy__sum']) / sumx
                    pusta_lista.append(ost)
                else:
                    k = int(k - 1);
                    ost=0
                    pusta_lista.append(ost)












        print(pusta_lista)
        if(flaga20==True):
            sum2020 = dane_2020.count()
            op2020 = dane_2020.aggregate(Sum('spolka_najwyzszy'))
            op20202 = dane_2020.aggregate(Sum('spolka_najnizszy'))
            ost = (op2020['spolka_najwyzszy__sum'] - op20202['spolka_najnizszy__sum']) / sum2020
        else:
            ost=0

        if (flaga19 == True):
            sum1 = dane_2019.count()
            op1 = dane_2019.aggregate(Sum('spolka_najwyzszy'))
            op2 = dane_2019.aggregate(Sum('spolka_najnizszy'))
            k = (op1['spolka_najwyzszy__sum'] - op2['spolka_najnizszy__sum']) / sum1
            print(k)
        else:
            k=0


        if (flaga18 == True):
            sum8 = dane_2018.count()
            op8 = dane_2018.aggregate(Sum('spolka_najwyzszy'))
            op81 = dane_2018.aggregate(Sum('spolka_najnizszy'))
            k8 = (op8['spolka_najwyzszy__sum'] - op81['spolka_najnizszy__sum']) / sum8
            print(k8)
        else:
            k8=0







        Mx1 = srednia(zam['Otwarcie'])
        Sx1 = odchylenie(zam['Otwarcie'], Mx1)

        dane2 = {
            'dane': dane,
            'nazwa': name,
            'Mx1': Mx1,
            'Sx1': Sx1,
            'n1': ost,
            'n2': k,
            'n3': k8,
            'lista': pusta_lista,

        }

        # dane = Dane_spółek.objects.all()

        return render(request, "Strona_3.html", dane2)

    else:
        return render(request, "Strona_2.html", context=context)


def szukanie(name1):
    c = name1.upper()
    for i in range(8):
        k = i + 1
        dest_url = 'Spółki_' + str(k) + '.csv'
        save_path = r'C:\Users\kuba2\PycharmProjects\djangoProject2\Nazwy_spółek'
        url = os.path.join(save_path, dest_url)

        with open(url, 'r') as csvfile:
            # deklarujemy nasz *czytacz*
            # parametr *delimiter* jest opcjonalny i wskazuje jaki został w pliku użyty separator
            csvreader = csv.reader(csvfile, delimiter=',')
            for row in csvreader:

                if (row[1] == c):
                    # analogicznie - 2 kolumna
                    return row[0]


def download(csv_url, name):
    with urllib.request.urlopen(csv_url) as response:
        csv = response.read()  # czyta informacje z tekstu w danym pliku

        csv_str = str(csv)  # upewniamy się,że plik jest w stringu ( anie np binarne dane )
        # print(csv_str)

        lines = csv_str.split("\\n")

        dest_url = 'Dane_Giełdowe_' + name + '.csv'
        save_path = r'C:\Users\kuba2\PycharmProjects\djangoProject2\Dane_analiza'
        completeName = os.path.join(save_path, dest_url)

        fx = open(completeName, "w")

        for line in lines:
            fx.write(line + '\n')
        fx.close()
        return completeName


def download_data_name(all_Data):
    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_1.csv', sep=',',
                       na_values=" ")
    k = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_2.csv', sep=',',
                       na_values=" ")
    a = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_3.csv', sep=',',

                       na_values=" ")
    b = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_4.csv', sep=',',
                       na_values=" ")
    c = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_5.csv', sep=',',
                       na_values=" ")
    d = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_6.csv', sep=',',
                       na_values=" ")
    e = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_7.csv', sep=',',

                       na_values=" ")
    f = dane;

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_8.csv', sep=',',
                       na_values=" ")
    g = dane;

    for i in range(k.shape[0]):
        temp = k.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])

    for i in range(a.shape[0]):
        temp = a.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(b.shape[0]):
        temp = b.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(c.shape[0]):
        temp = c.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])

    for i in range(d.shape[0]):
        temp = d.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])

    for i in range(e.shape[0]):
        temp = e.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(f.shape[0]):
        temp = f.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(g.shape[0]):
        temp = g.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    return all_Data


def srednia(zbior):
    return float(zbior.sum()) / len(zbior)


def timesrednia(zbior):
    suma = 0
    index = 0
    for i in range(zbior):
        index += 1
        suma += index

    suma = suma / zbior
    return suma


def odchylenie(zbior, srednia):
    licznik = 0
    for elem in zbior:
        licznik += (elem - srednia) * (elem - srednia)
    return sqrt(licznik / (len(zbior) - 1))


def odchylenieczas(zbior, srednia):
    licznik = 0
    for elem in range(zbior):
        licznik += (elem - srednia) * (elem - srednia)
    return sqrt(licznik / (zbior - 1))


def sumowanie(ilosc, zbior):
    licznik = 0
    index = 0
    for elem in zbior:
        index += index + 1
        licznik += elem * index
        print(licznik)
    return int(licznik)


def sumowanie2(zbior):
    licznik = 0

    for elem in range(zbior):
        licznik += elem * elem
    return int(licznik)
