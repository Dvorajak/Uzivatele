from email import message
from django.shortcuts import redirect, reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from .models import Uzivatel, Komentare
from .forms import UzivatelForm, KomentarForm
import requests
import datetime

#Třída pro index stránky, kde vypíše list uživatelů
class index(generic.ListView):

    template_name = "sprava/index.html"
    context_object_name = "uzivatele"

    def get_queryset(self):

        #Jestliže v databázi nejsou žádní uživatelé navrátí None
        if len(Uzivatel.objects.all().order_by("-id")) == 0:
            return None

        #Získání uživatelů z databáze
        return Uzivatel.objects.all().order_by("-id") 

#Třída pro vypsání listu komentářů
class ListKomentaru(generic.ListView):

    template_name = "sprava/komentare.html"
    context_object_name = "komentare"

    

    def get_queryset(self):

        #Získání komentářů z databáze
        komentare = Komentare.objects.all().order_by("-id")

        #Jestliže v databázi nejsou žádné komentáře navrátí None
        if len(komentare) == 0:
            return None

        #Pro každý komentář
        for i in komentare:
            #Jestliže je komentář delší než 15 znaků, získá prvních 15 znaků a přidá ... pro náhled
            if len(i.obsah) > 15:
                i.obsah = i.obsah[:15] + "..."
        return komentare

#Třída pro získání externího API
class API(generic.edit.CreateView):

    template_name = "sprava/API.html"
   
    def get(self,request):
        #načtení externího api do proměnné
        r = requests.get('https://zoo-animal-api.herokuapp.com/animals/rand')

        #Získání 'name' a 'latin_name' z externího api
        name = r.json()['name']
        latinName = r.json()['latin_name']
        #print(r.json())
        return render(request,self.template_name,{"name":name,"latin":latinName})

#Třída pro založení uživatele
class ZalozitUzivatele(generic.edit.CreateView):
    
    form_class = UzivatelForm
    template_name = "sprava/form_uzivatele.html"
    nadpis = "Založení uživatele"


    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name,{"form":form,"nadpis":self.nadpis})

    def post(self,request):

        form = self.form_class(request.POST)

        #Jesliže je formulář validní, uloží a navrátí zprávu s informací o úspěšném uložení, navrátí index
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Uživatel uložen")
            return redirect("index")

        #Jinak vypíše zprávu o špatném zadání formátu data
        else:
            messages.error(request," Zadejte prosím datum ve správném formátu ")
        
        return render(request,self.template_name,{"form":form})

#Třída pro založení komentáře
class ZalozitKomenar(generic.edit.CreateView):
    
    form_class = KomentarForm
    template_name = "sprava/form_komentare.html"
    nadpis = "Nový komentář"


    def get(self, request,pk):

        uzivatel = Uzivatel.objects.get(pk=pk)

        #Naváže uživatele na komentář
        form = self.form_class(initial={'uzivatel':uzivatel})

        return render(request,self.template_name,{"form":form,"nadpis":self.nadpis,"uzivatel":uzivatel})

    def post(self,request,pk):


        
        #Získá objekt uživatele
        uzivatel = Uzivatel.objects.get(pk=pk)

        # načte do requestu uživatele
        # zapamatuje si starý status
        _mutable = request.POST._mutable

        # změní na měnný
        request.POST._mutable = True

        #uloží do reqestu uživatele
        request.POST['uzivatel'] = uzivatel.id 

        # změní zpět na neměnný
        request.POST._mutable = _mutable
        
        form = self.form_class(request.POST)

        #jesliže je formulář validní
        if form.is_valid():
            form.save(commit=True)
            messages.info(request,"Komentář uložen")

            #Navrátí detail uživatele
            return redirect("DetailUzivatele",pk=uzivatel.id)
        
        return render(request,self.template_name,{"form":form})

#Třída na detail uživatele
class DetailUzivatel(generic.DetailView,generic.ListView):
    
    model = Uzivatel
    template_name = "sprava/detail_uzivatele.html"

    def get(self,request,pk):

        #Pokusí se získat objekt uživatele
        try:
            uzivatel = self.get_object()
        except:
            return redirect("index")

        #Získá list komentářů z databáze
        list_komentaru = Komentare.objects.all().order_by("-id")

        #Vytvoří prázný list
        muj_list = []

        #pro každý komentář 
        for komentar in list_komentaru:

            #Jesliže komentář přidružen aktuálnímu uživateli
            if uzivatel.id == komentar.uzivatel.id:
                #Upraví datum komenáře
                komentar.datum = komentar.datum.strftime("%d.%m.%Y - %H:%M")

                #Jestliže je komentář delší než 15 znaků, získá prvních 15 znaků a přidá ... pro náhled
                if len(komentar.obsah) > 15:
                    komentar.obsah = komentar.obsah[:15] + "..."

                #Připojí do listu
                muj_list.append(komentar)


        # Jesliže je list prázný nastaví se mu hodnota None
        if len(muj_list) == 0:
            muj_list = None

        #Upraví datum narození uživatele
        datum_narozeni = uzivatel.datum_narozeni.strftime("%d.%m.%Y")
        return render(request,self.template_name,{"uzivatel":uzivatel,"datum":datum_narozeni,"list":muj_list})

    def post(self,request,pk):

        #Jesliže stránka zašle požadavek na úpravu
        if "upravit" in request.POST:
            #Přesměruje na stránku s úpravou
            return redirect("UpravitUzivatele",pk=self.get_object().pk)

        #Jesliže stránka zašle požadavek na smazání
        elif "smazat" in request.POST:
            messages.info(request,"Uživatel smazán")
            #Smaže uživtale
            self.get_object().delete()

        #Jesliže stránka zašle požadavek na přidání komentáře
        elif "pridat_komentar" in request.POST:
            #Přesměruje na stránku s přidáním komentáře 
            return redirect("ZalozKomentar",pk=self.get_object().pk)
        
        return redirect("index")

#Třída na zobrazení detailu komentáře
class DetailKomentar(generic.DetailView):
    model = Komentare
    template_name = "sprava/detail_komentare.html"

    def get(self,request,pk):

        #Pokusí se získat objekt komentáře
        try:
            komentar = self.get_object()
        except:
            return redirect("index")

        return render(request,self.template_name,{"komentar":komentar})

    def post(self,request,pk):

        komentar = self.get_object()

        #Jesliže stránka zašle požadavek na úpravu
        if "upravit" in request.POST:
            return redirect("UpravitKomentar",pk=self.get_object().pk)

        #Jesliže stránka zašle požadavek na smazání
        elif "smazat" in request.POST:
            messages.info(request,"Komentář smazán")
            self.get_object().delete()
            return redirect("DetailUzivatele",pk=komentar.uzivatel.id)

        #Jesliže stránka zašle požadavek na navrácení do detailu uživatele
        elif "zpet" in request.POST:
            return redirect("DetailUzivatele",pk=komentar.uzivatel.id)

        return redirect("index")

#Třáda pro editaci uživatele
class EditUzivatele(generic.edit.CreateView):
    form_class = UzivatelForm
    template_name = "sprava/form_uzivatele.html"
    nadpis = "Úprava uživatele"

    def get(self,request,pk):

        #Získá obejkt uživatele
        uzivatel = Uzivatel.objects.get(pk=pk)

        #Načte do formuláře instanci upravovaného uživatele
        form = self.form_class(instance = uzivatel)

        return render(request,self.template_name,{"form":form,'uzivatel':uzivatel,'nadpis':self.nadpis})
    
    def post(self,request,pk):

        form = self.form_class(request.POST)    

        if form.is_valid():

            #Získá data z upravovaného formuláře
            jmeno = form.cleaned_data["jmeno"]
            datum_narozeni = form.cleaned_data["datum_narozeni"]

            #Pokusí se získat objekt uživatele
            try:
                uzivatel = Uzivatel.objects.get(pk=pk)
            except:
                return redirect("index")
            
            #Načte data do upravovaného uživatele
            uzivatel.jmeno = jmeno
            uzivatel.datum_narozeni = datum_narozeni
            messages.info(request,"Uživatel upraven")

            #Následně změny uloží
            uzivatel.save()

            return redirect("DetailUzivatele",pk=uzivatel.id)

        else:
            messages.error(request," Zadej správné datum ")
            return render(request,self.template_name,{"form":form})

#Třída pro úpravu komentáře
class EditKomentare(generic.edit.CreateView):
    form_class = KomentarForm
    template_name = "sprava/form_komentare.html"
    nadpis = "Úprava komentáře"

    def get(self,request,pk):
        
        #Získá obejkt komentáře
        komentar = Komentare.objects.get(pk=pk)

        #Načte do formuláře instanci upravovaného uživatele
        form = self.form_class(instance = komentar)

        return render(request,self.template_name,{"form":form,'komentar':komentar,'nadpis':self.nadpis})

    def post(self,request,pk):
        komentar = Komentare.objects.get(pk=pk)

        #Jesliže strána zašle v požadavku "zpět" navrátí detail komentáře
        if "zpet" in request.POST:
            return redirect("DetailKomentare",pk=komentar.id)

        # načte do requestu uživatele
        # zapamatuje si starý status
        _mutable = request.POST._mutable

        # změní na měnný
        request.POST._mutable = True

        #uloží do reqestu uživatele
        request.POST['uzivatel'] = komentar.uzivatel.id 

        # změní zpět na neměnný
        request.POST._mutable = _mutable

        form = self.form_class(request.POST)   

        if form.is_valid():

             #Získá data z upravovaného formuláře
            obsah = form.cleaned_data["obsah"]

            #Pokusí se získat objekt komentáře
            try:
                komentar = Komentare.objects.get(pk=pk)
            except:
                return redirect("index")
            
            #Načte data do upravovaného komentáře
            komentar.obsah = obsah
            messages.info(request,"Komentář upraven")

            #Následně změny uloží
            komentar.save()

        return redirect("DetailKomentare",pk=komentar.id)
