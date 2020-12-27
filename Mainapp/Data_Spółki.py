import os

from bs4 import BeautifulSoup
import urllib.request
import csv



def pobieranie_gieldy():
    print("dsdsdsdfd")
    for i in range(8):
        #
        k = i + 1;
        if (k == 1):
            stronawww = 'https://stooq.pl/t/?i=523&v=' + str(k)
        else:
            stronawww = 'https://stooq.pl/t/?i=523&v=0&l=' + str(k)



        # zapytanie do strony internetowej i zwrocenie wyniku w postaci kodu html oraz przypisanie do zmiennej "obiekt"
        obiekt = urllib.request.urlopen(stronawww)
        # parsowanie html z uzyciem BeautifulSoup i przypisanie do zmiennej "soup"
        soup = BeautifulSoup(obiekt, "html5lib")  # Parsowanie strony


        # sprawdzanie czy istnieja dane w tabeli
        tabela = soup.find('table', attrs={'class': 'fth1'})
        ilosc_wierszy = tabela.find_all('tr')
        # zliczenie liczby wierszy w tabeli, ale pominiecie pierwszego jako naglowka, wynikiem powinno byc 20

        wiersze = []
        wiersze.append(['Symbol', 'Nazwa'])


        for wiersz in ilosc_wierszy:
            data = wiersz.find_all('td')
            # sprawdz czy kolumny posiadaja dane
            if len(data) == 0:
                continue

            # pisz zawartosc kolumny do zmiennej
            symbol = data[0].getText()
            nazwa = data[1].getText()


            # dolacz wynik do wiersza
            wiersze.append([symbol, nazwa])

            dest_url = 'Spółki_' + str(k) + '.csv'
            save_path = r'C:\Users\kuba2\PycharmProjects\djangoProject2\Nazwy_spółek'
            url = os.path.join(save_path, dest_url)

        with open(url, 'w', newline='') as plik_wynikowy:
            csv_output = csv.writer(plik_wynikowy)
            csv_output.writerows(wiersze)


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
        save_path = r'C:\Users\kuba2\PycharmProjects\pythonProject2\Dane'
        completeName = os.path.join(save_path, dest_url)

        fx = open(completeName, "w")

        for line in lines:
            fx.write(line + '\n')
        fx.close()


