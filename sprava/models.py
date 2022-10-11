from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models

#Uživatelský model
class Uzivatel(models.Model):

    #Pole jména a data narození
    jmeno = models.CharField(max_length=20,verbose_name = "Jméno")
    datum_narozeni = models.DateField(verbose_name = "Datum narození")

    #Pojmenování v databázi
    class Meta:
     verbose_name = "Uživatel"
     verbose_name_plural = "Uživatelé"

    #Navrácení stringové podoby v případě zavolání
    def __str__(self):
        return f"{self.jmeno}"

#Model komentářů
class Komentare(models.Model):

    """
    Pole uživale(klíč napojen a daného uživatele, v případě smazání uživatele se smaže i komentář),
    datumu vztvoření komentáře a obsahu komentáře
    """
    uzivatel = models.ForeignKey(Uzivatel, verbose_name = "Uživatel", on_delete = models.CASCADE)
    datum = models.DateTimeField(auto_now_add=True)
    obsah = models.TextField()

    #Pojmenování v databázi
    class Meta:
     verbose_name = "Komentář"
     verbose_name_plural = "Komentáře"

    #Navrácení stringové podoby v případě zavolání
    def __str__(self):
        return f"{self.uzivatel} {self.datum}"