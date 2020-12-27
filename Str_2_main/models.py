from django.db import models


# Create your models here.
class Spółka:
    spolka_id: int
    spolka_otwarcie: float
    spolka_najwyzszy: float
    spolka_najnizszy: float
    spolka_zamkniecie: float
