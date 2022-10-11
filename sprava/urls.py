"""sprava URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index.as_view(), name="index"),
    path('komentare/',views.ListKomentaru.as_view(), name="Komentare"),
    path("tvorba_uzivatele/",views.ZalozitUzivatele.as_view(),name="ZalozUzivatele"),
    path("<int:pk>/uprava_uzivatele/",views.EditUzivatele.as_view(),name="UpravitUzivatele"),
    path("<int:pk>/uprava_komentare/",views.EditKomentare.as_view(),name="UpravitKomentar"),
    path("<int:pk>/zalozeni_komentare/",views.ZalozitKomenar.as_view(),name="ZalozKomentar"),
    path("api/",views.API.as_view(),name="API"),
    path("<int:pk>/detail_uzivatele/",views.DetailUzivatel.as_view(),name="DetailUzivatele"),
    path("<int:pk>/detail_komentare/",views.DetailKomentar.as_view(),name="DetailKomentare")
]

