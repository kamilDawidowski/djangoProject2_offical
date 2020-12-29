from django.db import models


# Create your models here.
class Nazwy_spółek (models.Model):
    spolka_data_name = models.CharField(max_length=15)
    spolka_data_skrot = models.CharField(max_length=15)

    def __str__(self):
        return self.spolka_data_name



class Dane_spółek(models.Model):
    spolka_name=models.ForeignKey(Nazwy_spółek,null=True,on_delete=models.SET_NULL)
    spolka_numer = models.IntegerField(default=0)
    spolka_otwarcie = models.DecimalField(decimal_places=10,max_digits=17)
    spolka_najwyzszy = models.DecimalField(decimal_places=10,max_digits=17)
    spolka_najnizszy = models.DecimalField(decimal_places=10,max_digits=17)
    spolka_zamkniecie = models.DecimalField(decimal_places=10,max_digits=17)
    spolka_data = models.DateTimeField(auto_now=False, auto_now_add=True)
