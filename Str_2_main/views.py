import csv
import os
import urllib

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Nazwy_spółek, Dane_spółek


# Create your views here.

def menu(request):
    # pobieranie_gieldy()
    # Dodaj petle sprawdz czy jest

    all_Data = []
    # download_data_name(all_Data)

    # context = {'data': all_Data}

    for data in all_Data:
        if Nazwy_spółek.objects.filter(spolka_data_name=data['Nazwa'],
                                       spolka_data_skrot=data['Symbol']).exists() == False:
            Nazwy_spółek.objects.create(spolka_data_name=data['Nazwa'], spolka_data_skrot=data['Symbol'])
    baza = Nazwy_spółek.objects.all()
    baza = {'data': baza, }

    return render(request, "Strona_2.html", baza)


def odp2(request):
    name_spolka_do_analizy_ver1 = request.GET["spółka_do_analizy_ver1"]

    name_spolka_do_analizy_ver2 = request.GET["spółka_do_analizy_ver2"]



    print(str(name_spolka_do_analizy_ver1))
    print(str(name_spolka_do_analizy_ver2))

    name2 = str(szukanie(name_spolka_do_analizy_ver2))
    name1 = str(szukanie(name_spolka_do_analizy_ver1))

    print(name1)
    print(name2)

    www_ver1 = 'https://stooq.pl/q/d/l/?s=' + name1 + '&i=d'
    www_ver2 = 'https://stooq.pl/q/d/l/?s=' + name2 + '&i=d'

    odp1 = download(www_ver1, name1)
    odp2 = download(www_ver2, name2)

    dane1 = pd.read_csv(odp1, sep=',',
                        na_values=" ")
    dane2 = pd.read_csv(odp2, sep=',',
                        na_values=" ")

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

    if (name1 or name2 != 'None'):
        flaga = True
    else:
        flaga = False

    baza = Nazwy_spółek.objects.all()

    context = {
        'flaga': flaga,
        'data': baza,
        'name1': name1,
        'name2': name2,

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

        dane2 = {
            'dane_1': dane_1,
            'dane_2': dane_2,
            'nazwa_1': name1,
            'nazwa_2': name2,
        }

        # dane = Dane_spółek.objects.all()

        return render(request, "Strona_3_ver2.html", dane2)
    else:
        return render(request, "Strona_2.html", context=context)





def odp(request):
    name_spolka_do_analizy = request.GET["spółka_do_analizy"]
    name = str(szukanie(name_spolka_do_analizy))
    www = 'https://stooq.pl/q/d/l/?s=' + name + '&i=d'
    odp = download(www, name)
    dane = pd.read_csv(odp, sep=',',
                       na_values=" ")
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

    context = {
        'flaga': flaga,
        'data': baza,
        'name': name,

    }

    # Gdy nie ma pustej listy to tworzony jest do bazy danych nowy projekt
    if (flaga == True):
        del all_Data[-1]

        k = Nazwy_spółek.objects.get(spolka_data_skrot=name)

        for data in all_Data:
            if Dane_spółek.objects.filter(spolka_name=k,
                                          spolka_data=data["b'Data"]).exists() == False:
                Dane_spółek.objects.create(spolka_name=k,
                                           spolka_otwarcie=data['Otwarcie'],
                                           spolka_najwyzszy=data['Najwyzszy'],
                                           spolka_najnizszy=data['Najnizszy'],
                                           spolka_zamkniecie=data['Zamkniecie'],
                                           spolka_data=data["b'Data"])

        dane = Dane_spółek.objects.all().filter(spolka_name=k)

        dane2 = {
            'dane': dane,
            'nazwa': name,
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
