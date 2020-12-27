from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
# Create your views here.
from Mainapp.Data_Spółki import pobieranie_gieldy


def logo(request):
    return render(request, "Strona_1.html")

