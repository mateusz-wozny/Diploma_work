import math
import os
import random
import time
from functools import reduce
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDSwitch
from edycja import Deletedot, part_document
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import kryptografia as zs
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
import primes as ps

tekst = []
styl = {True: "Dark", False: "Light"}


class Pierwszy(Screen):
    pass


class Drugi(Screen):
    pass


class Menedzer(ScreenManager):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Content(BoxLayout):
    pass


class Kryptografia(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('ekran.kv')

    def Zmien_ekran(self, da):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.manager.current = da.text

    def on_stop(self):
        """
        Funkcja usuwa pliki utworzone podczas pracy aplikacji.
        """
        if os.path.exists("pliki/bez_znakow.txt"):
            os.remove('pliki/bez_znakow.txt')
        if os.path.exists('pliki/podzielony.txt'):
            os.remove('pliki/podzielony.txt')
        if os.path.exists('pliki/zaszyfrowane.txt'):
            os.remove('pliki/zaszyfrowane.txt')
        if os.path.exists('pliki/wprowadzony_tekst.txt'):
            os.remove('pliki/wprowadzony_tekst.txt')
        if os.path.exists('pliki/odszyfrowane.txt'):
            os.remove('pliki/odszyfrowane.txt')

    def on_start(self):
        """
        Funkcja dodająca nawigację do głównego ekranu.
        """
        icons_item = {
            "lock": "RSA",
            "lock-outline": "Rabin",
            "slash-forward": "Faktoryzacja"
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name], on_release=self.Zmien_ekran)
            )

    def przelicz_granice(self, granica: str, b: bool) -> None:
        """
        Funkcja przelicza podaną granicę na wartość liczbową, wykrywa znak potęgowania.

        :param granica: Tekst zawierający wartość granicy górnej/dolnej
        :param b: Określenie, czy podana została granica górna czy dolna, b=True górna, b=False dolna

        """
        l = granica
        l = l.replace(',', '_')
        if '^' in l:
            u = l.split('^')
            u = [int(i) for i in u]
            if b:
                self.gorna = reduce(lambda x, y: x ** y, u)

            else:
                self.dolna = reduce(lambda x, y: x ** y, u)

        else:
            if b:

                self.gorna = int(l)

            else:
                self.dolna = int(l)

    def aktualizuj_gorna(self, tekst: str) -> None:
        """
        Funkcja aktualizująca wartość górnej granicy wykorzystywanej przez aplikację.

        :param tekst: Parametr określający aktywny ekran - "RSA", w przeciwnym wypadku ekran dla systemu Rabina

        """
        try:
            if tekst == "RSA":
                self.przelicz_granice(self.root.ids.g.text, True)
            else:
                self.przelicz_granice(self.root.ids.g2.text, True)
        except Exception as e:
            if tekst == "RSA":
                self.root.ids.g.text = "Błędna granica"
            else:
                self.root.ids.g2.text = "Błędna granica"

    def aktualizuj_dolna(self, tekst: str) -> None:
        """
        Funkcja aktualizująca wartość dolnej granicy wykorzystywanej przez aplikację.

        :param tekst: Parametr określający aktywny ekran - "RSA", w przeciwnym wypadku ekran dla systemu Rabina

        """
        try:
            if tekst == "RSA":
                self.przelicz_granice(self.root.ids.d.text, False)
            else:
                self.przelicz_granice(self.root.ids.d2.text, False)
        except Exception as e:
            if tekst == "RSA":
                self.root.ids.d.text = "Błędna granica"
            else:
                self.root.ids.d.text = "Błędna granica"

    def aktualizuj_podzial(self, tekst: str) -> None:
        """
        Funkcja aktualizująca podział wyrazów na bloki.

        :param tekst: Parametr określający aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

        """
        try:
            if tekst == "RSA":
                self.root.ids.p.text = ""
                self.ciag = int(self.root.ids.podzial.text)
            else:
                self.root.ids.p2.text = ""
                self.ciag = int(self.root.ids.podzial2.text)

        except Exception as e:
            if tekst == 'RSA':
                self.root.ids.p.text = str(e)
            else:
                self.root.ids.p2.text = str(e)

    def zapisz_tekst(self, tek: str) -> None:
        """
        Funkcja zapisuje wprowadzony tekst jawny do pliku txt w zależności od ekranu.

        :param tek: Parametr określający aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

        """
        tekst.clear()
        if tek == "RSA":
            tekst.append(self.root.ids.tekst.text)
        else:
            tekst.append(self.root.ids.tekst2.text)
        nazwa = 'pliki/wprowadzony_tekst'
        nazwa += ".txt"

        with open(f'{nazwa}', encoding='utf-8', mode='w') as file:
            for t in tekst:
                file.write(t)
        Deletedot('pliki/wprowadzony_tekst', 'chwil')

        os.remove('chwil.txt')

    def generuj_klucz_RSA(self) -> None:
        """
        Funkcja wyznacza losowo liczby pierwsze p oraz q, następnie oblicza pozostałe parametry funkcji szyfrującej (deszyfrującej) systemu RSA.
        """
        try:
            if int(self.gorna) > int(self.dolna) and int(self.gorna) > 0 and int(self.dolna) > 0:
                # Wyznaczenie liczb pierwszych do wskazanej liczby
                p = None
                while p is None:
                    t = 6 * random.randint(int(self.dolna) // 6, int(self.gorna) // 6) + 1
                    if ps.prim.test_Millera_Rabina(t, 10):
                        p = t
                q = p
                while q == p:
                    j = 6 * random.randint(int(self.dolna) // 6, int(self.gorna) // 6) + 1
                    if ps.prim.test_Millera_Rabina(j, 10):
                        q = j
                self.n = zs.Kryptografia(p, q)
                phi = self.n.phi()
                n = self.n
                a = None
                while a is None:
                    b = random.randint(2, phi - 1)
                    if n.NWD(phi, b) == 1:
                        a = n.RozszEuk(phi, b)
                self.a = a
                self.b = b
                if n.n > 10 ** 32:
                    self.root.ids.n.text = 'n= ' + format(n.n, '10.2e')
                else:
                    self.root.ids.n.text = f'n= {n.n:,}'
                if n.n > 10 ** 32:
                    self.root.ids.b.text = 'b= ' + format(b, '10.2e')
                else:
                    self.root.ids.b.text = f'b= {b:,}'
                self.root.ids.minimalna.text = str(int(math.log(n.n, 37)))
            else:
                MDDialog(text="Wprowadzono niepoprawne granice").open()
        except Exception as e:
            self.root.ids.odszyfrowane.text = str(e)

    def zaszyfruj_Rsa(self) -> None:
        """
        Funkcja edytuje wprowadzony tekst, usuwając wszystkie wartości niebędące literami lub spacją,
        następnie dzieli tekst na bloki o wprowadzonym podziale. Następnie szyfruje tekst jawny wykorzystując funkcję szyfrującą systemu RSA

        """

        try:

            if int(self.ciag) > 0:
                self.root.ids.odszyfrowane.text = ""

                # Usunięcie znaków interpunkcyjnych
                Deletedot('pliki/wprowadzony_tekst', 'pliki/bez_znakow')
                # Podzielenie dokumentu na bloki n-literowe
                part_document('pliki/bez_znakow', int(self.ciag), 'pliki/podzielony')

                self.n.zakoduj_RSA(self.b, 'pliki/zaszyfrowane', 'pliki/podzielony')
            else:
                MDDialog(text="Wprowadzono niepoprawny podział").open()

        except Exception as e:
            self.root.ids.odszyfrowane.text = str(e)

    def odszyfruj_Rsa(self) -> None:
        """
        Funkcja deszyfrująca wiadomość zaszyfrowaną za pomocą systemu RSA.

        """
        try:
            self.n.odkoduj_RSA('pliki/zaszyfrowane', self.a, 'pliki/odszyfrowane', self.ciag)
            with open('pliki/odszyfrowane.txt', encoding='utf-8', mode='r') as zak:
                self.root.ids.odszyfrowane.text = zak.read()
        except Exception as e:
            self.root.ids.odszyfrowane.text = str(e)

    def generuj_klucz_Rabin(self) -> None:
        """
        Funkcja wyznacza losowo liczby pierwsze p oraz q, następnie oblicza pozostałe parametry funkcji szyfrującej (deszyfrującej) systemu Rabina.

        """
        try:
            if int(self.gorna) > int(self.dolna) and int(self.gorna) > 0 and int(self.dolna) > 0:

                p = None
                while p is None:
                    t = 6 * random.randint(int(self.dolna) // 6, int(self.gorna) // 6) + 1
                    if ps.prim.test_Millera_Rabina(t, 10):
                        p = t
                q = p
                while q == p:
                    j = 6 * random.randint(int(self.dolna) // 6, int(self.gorna) // 6) + 1
                    if ps.prim.test_Millera_Rabina(j, 10):
                        q = j
                self.n = zs.Kryptografia(p, q)
                self.p = p
                self.q = q
                if self.n.n > 10 ** 32:
                    self.root.ids.n2.text = 'n= ' + format(self.n.n, '10.2e')

                else:
                    self.root.ids.n2.text = f'n= {self.n.n:,}'
                self.root.ids.minimalna2.text = str(int(math.log(self.n.n, 37)))
            else:
                MDDialog(text="Wprowadzono niepoprawne granice").open()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = str(e)

    def zaszyfruj_Rabin(self) -> None:
        """
        Funkcja szyfrująca wprowadzony tekst za pomocą funkcji szyfrującej zdefiniowanej dla systemu Rabina.
        Na początku edytowany zostaje wprowadzony tekst, później podzielony na bloki odpowiedniej długości i
        w ostatniej części w zależności od wybranej opcji (wybór poprawnego tekstu jawnego lub wyświetlanie czterech możliwych)
        następuje szyfrowanie za wykorzystując funkcję szyfrującą dla systemu Rabina.

        """

        try:
            if int(self.ciag) > 0:
                self.root.ids.odszyfrowane2.text = ""

                # Usunięcie znaków interpunkcyjnych, specjalnych
                Deletedot('pliki/wprowadzony_tekst', 'pliki/bez_znakow')
                # Podzielenie dokumentu na wyrazy n-literowe
                part_document('pliki/bez_znakow', int(self.ciag), 'pliki/podzielony')
                self.check = self.root.ids.check.active
                self.n.zakoduj_Rabin('pliki/zaszyfrowane', 'pliki/podzielony', self.check)
            else:
                MDDialog(text="Wprowadzono niepoprawny podział").open()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = "Nastąpił błąd szyfrowania"

    def odszyfruj_Rabin(self) -> None:
        """
        Funkcja deszyfrująca zaszyfrowaną wiadomość dla systemu Rabina. Zwrócony zostaje jeden tekst jawny
        lub wszystkie cztery w zależności od wybranej opcji.

        """
        try:
            self.n.odkoduj_Rabin('pliki/zaszyfrowane', self.p, self.q, 'pliki/odszyfrowane', self.check, self.ciag)
            with open('pliki/odszyfrowane.txt', encoding='utf-8', mode='r') as zak:
                self.root.ids.odszyfrowane2.text = zak.read()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = str(e)

    def czy_pierwsza(self) -> None:
        """
        Funkcja sprawdzająca pierwszość liczby za pomocu wybranego testu pierwszości (Millera-Rabina lub Fermata).

        """
        self.root.ids.pierwsza.text = ""
        if self.root.ids.Rabin.active:
            self.root.ids.pierwsza.text = str(ps.prim.test_Millera_Rabina(int(self.root.ids.liczba.text), 20))
        elif self.root.ids.Fermat.active:
            self.root.ids.pierwsza.text = str(ps.prim.test_Fermata(int(self.root.ids.liczba.text), 20))
        else:
            MDDialog(text='Nie wybrano żadnej z opcji').open()

    def faktoryzacja(self) -> None:
        """
        Funkcja dokonująca rozkładu wprowadzonej liczby na czynniki pierwsze w zależności od wybranego
        algorytmu (próbnych dzieleń, Fermata lub rho Pollarda).

        """
        self.root.ids.rozklad.text = ""
        if self.root.ids.probne.active:
            ps.prim.trial_divide2(int(self.root.ids.zlozona.text), self.root.ids.rozklad)
            self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        elif self.root.ids.fer.active:
            y = ps.prim.Fermat2(int(self.root.ids.zlozona.text), self.root.ids.rozklad, time.time())
            if not y:
                MDDialog(text="Przekroczono czas obliczeń", items='alert').open()
            else:
                self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        elif self.root.ids.Pollard.active:
            ps.prim.rho2(int(self.root.ids.zlozona.text), 1, 0, 3, 9000, 2, self.root.ids.rozklad)
            self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        else:
            MDDialog(text='Nie wybrano żadnej z opcji').open()

    def sprawdz(self) -> None:
        """
        Funkcja obliczająca iloczyn czynników pierwszych podanych przez wybrany algorytm faktoryzacji.

        """
        if self.root.ids.rozklad.text != "":
            t = self.root.ids.rozklad.text.split(',')
            self.root.ids.iloczyn.text = str(reduce(lambda x, y: x * y, [int(i) for i in t]))

    def pokaz_zaszyfrowany(self, tek: str) -> None:
        """
        Funkcja umożliwiająca wyświetlenie zaszyfrowanego tekstu jawnego, w zależności od aktywnego ekranu.

        :param tek: Parametr określający aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

        """
        if os.path.exists('pliki/zaszyfrowane.txt'):
            with open('pliki/zaszyfrowane.txt', mode='r', encoding='utf-8') as f:
                zakodow = f.read().split('\n')
            odk = []
            zakodow = [int(i) for i in zakodow]
            for y in zakodow:
                odk.append(zs.Kryptografia.odwproc2(y, self.ciag))
            odkslow = []
            for t in range(0, len(odk)):
                e = ""
                for w in odk[t]:
                    e += zs.slownik[w]
                odkslow.append(e)
            if tek == "RSA":
                self.root.ids.odszyfrowane.text = " ".join(odkslow)
            else:
                self.root.ids.odszyfrowane2.text = " ".join(odkslow)

    def pokaz(self, opcja: str) -> None:
        """
        Funkcja wyświetlająca pełną postać liczby będącej kluczem publicznym.

        :param opcja: Wybór wartości n lub b, opcja="n" lub opcja="b"

        """
        if opcja == "n":
            MDDialog(text=f'{self.n.n:,}').open()
        elif opcja == "b":
            MDDialog(text=f'{self.b:,}').open()

    def down(self, swit: MDSwitch, swit2: MDSwitch, swit3: MDSwitch, g: list) -> None:
        """
        Funkcja zmieniająca tryb jasności na wybranym ekranie.

        :param swit: Wartość boolean określająca, czy aktywny jest pierwszy ekran.
        :param swit2: Wartość boolean określająca, czy aktywny jest drugi ekran.
        :param swit3: Wartość boolean określająca, czy aktywny jest trzeci ekran.
        :param g: Lista zawierająca komórki, dla których należy zmienić kolor.

        """
        if swit.active:
            swit2.active = True
            swit3.active = True
            self.theme_cls.theme_style = "Light"
            for czek in g:
                czek.unselected_color = 0, 0, 0, 1
        else:
            swit2.active = False
            swit3.active = False
            self.theme_cls.theme_style = "Dark"
            for czek in g:
                czek.unselected_color = 1, 1, 1, 1


if __name__ == '__main__':
    Kryptografia().run()
    # help(Kryptografia().down)
