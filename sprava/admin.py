from django.contrib import admin
from .models import Uzivatel, Komentare

# Register your models here.

admin.site.register(Uzivatel)
admin.site.register(Komentare)