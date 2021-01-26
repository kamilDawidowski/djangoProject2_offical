import csv
import os
import urllib

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
# Create your views here.
from Mainapp.Data_Spółki import pobieranie_gieldy


def index_old(request):
    return render(request, "homeToIndex.html")


def dowSp(request):
    # pobieranie_gieldy()
    # Dodaj petle sprawdz czy jest

    dane = pd.read_csv('C://Users//kuba2//PycharmProjects//djangoProject2//Nazwy_spółek//Spółki_1.csv', sep=',', na_values=" ")
    k=dane;

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

    all_Data= []
    for i in range(k.shape[0]):
        temp=k.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(a.shape[0]):
        temp=a.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(b.shape[0]):
        temp=b.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(c.shape[0]):
        temp=c.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])

    for i in range(d.shape[0]):
        temp=d.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])

    for i in range(e.shape[0]):
        temp=e.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(f.shape[0]):
        temp=f.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])
    for i in range(g.shape[0]):
        temp=g.iloc[i]
        all_Data.append(dict(temp))
        # all_Data.append(dict[temp])




    context={'data':all_Data}
    return render(request, "result.html",context)

def genWyk (request):
    name_spolka_do_analizy=request.GET["spółka_do_analizy"]
    name = str(szukanie(name_spolka_do_analizy))
    www = 'https://stooq.pl/q/d/l/?s=' + name + '&i=d'
    odp=download(www, name)
    dane = pd.read_csv(odp, sep=',',
                    na_values=" ")
    a = dane;






    all_Data= []
    for i in range(a.shape[0]):
        temp=a.iloc[i]
        all_Data.append(dict(temp))
        print(temp)

    return render(request, "Strona_3.html", {'nazwa':name})

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
                print("swss")
                if (row[1] == c):
                    print(row[0])  # analogicznie - 2 kolumna
                    return row[0]

def download(csv_url,name):
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

