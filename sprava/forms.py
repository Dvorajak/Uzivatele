from dataclasses import Field
from django import forms
from .models import Uzivatel, Komentare
from django.db import models

#Formulář pro vytvoření a úpravu uživatele
class UzivatelForm(forms.ModelForm):

  class Meta:
    model = Uzivatel
    fields =["jmeno","datum_narozeni"]

#Formulář pro vytvoření a úpravu komentáře
class KomentarForm(forms.ModelForm):

  class Meta:
    model = Komentare
    fields =["uzivatel","obsah"]  

datum_narozeni = forms.DateField(
  widget=forms.DateInput(format='%d%m%Y'),
  input_formats=('%d%m%Y', )
)