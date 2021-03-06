import math
import os
import random
import time
from functools import reduce

import numpy
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDSwitch
from edition import Deletedot, part_document
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import crypto as zs
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
import prinum as ps
from kivy.core.window import Window

Window.size = (820, 550)
Window.minimum_width, Window.minimum_height = Window.size

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
        Funkcja dodaj??ca nawigacj?? do g????wnego ekranu.
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
        Funkcja przelicza podan?? granic?? na warto???? liczbow??, wykrywa znak pot??gowania.

        :param granica: Tekst zawieraj??cy warto???? granicy g??rnej/dolnej
        :param b: Okre??lenie, czy podana zosta??a granica g??rna czy dolna, b=True g??rna, b=False dolna

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
        Funkcja aktualizuj??ca warto???? g??rnej granicy wykorzystywanej przez aplikacj??.

        :param tekst: Parametr okre??laj??cy aktywny ekran - "RSA", w przeciwnym wypadku ekran dla systemu Rabina

        """
        try:
            if tekst == "RSA":
                self.przelicz_granice(self.root.ids.g.text, True)
            else:
                self.przelicz_granice(self.root.ids.g2.text, True)
        except Exception as e:
            if tekst == "RSA":
                self.root.ids.g.text = "B????dna granica"
            else:
                self.root.ids.g2.text = "B????dna granica"

    def aktualizuj_dolna(self, tekst: str) -> None:
        """
        Funkcja aktualizuj??ca warto???? dolnej granicy wykorzystywanej przez aplikacj??.

        :param tekst: Parametr okre??laj??cy aktywny ekran - "RSA", w przeciwnym wypadku ekran dla systemu Rabina

        """
        try:
            if tekst == "RSA":
                self.przelicz_granice(self.root.ids.d.text, False)
            else:
                self.przelicz_granice(self.root.ids.d2.text, False)
        except Exception as e:
            if tekst == "RSA":
                self.root.ids.d.text = "B????dna granica"
            else:
                self.root.ids.d.text = "B????dna granica"

    def aktualizuj_podzial(self, tekst: str) -> None:
        """
        Funkcja aktualizuj??ca podzia?? wyraz??w na bloki.

        :param tekst: Parametr okre??laj??cy aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

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
        Funkcja zapisuje wprowadzony tekst jawny do pliku txt w zale??no??ci od ekranu.

        :param tek: Parametr okre??laj??cy aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

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
        Funkcja wyznacza losowo liczby pierwsze p oraz q, nast??pnie oblicza pozosta??e parametry funkcji szyfruj??cej (deszyfruj??cej) systemu RSA.
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
        Funkcja edytuje wprowadzony tekst, usuwaj??c wszystkie warto??ci nieb??d??ce literami lub spacj??,
        nast??pnie dzieli tekst na bloki o wprowadzonym podziale. Nast??pnie szyfruje tekst jawny wykorzystuj??c funkcj?? szyfruj??c?? systemu RSA

        """

        try:

            if int(self.ciag) > 0:
                self.root.ids.odszyfrowane.text = ""

                # Usuni??cie znak??w interpunkcyjnych
                Deletedot('pliki/wprowadzony_tekst', 'pliki/bez_znakow')
                # Podzielenie dokumentu na bloki n-literowe
                part_document('pliki/bez_znakow', int(self.ciag), 'pliki/podzielony')

                self.n.zakoduj_RSA(self.b, 'pliki/zaszyfrowane', 'pliki/podzielony')
            else:
                MDDialog(text="Wprowadzono niepoprawny podzia??").open()

        except Exception as e:
            self.root.ids.odszyfrowane.text = str(e)

    def odszyfruj_Rsa(self) -> None:
        """
        Funkcja deszyfruj??ca wiadomo???? zaszyfrowan?? za pomoc?? systemu RSA.

        """
        try:
            self.n.odkoduj_RSA('pliki/zaszyfrowane', self.a, 'pliki/odszyfrowane', self.ciag)
            with open('pliki/odszyfrowane.txt', encoding='utf-8', mode='r') as zak:
                self.root.ids.odszyfrowane.text = zak.read()
        except Exception as e:
            self.root.ids.odszyfrowane.text = str(e)

    def generuj_klucz_Rabin(self) -> None:
        """
        Funkcja wyznacza losowo liczby pierwsze p oraz q, nast??pnie oblicza pozosta??e parametry funkcji szyfruj??cej (deszyfruj??cej) systemu Rabina.

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
                if self.root.ids.check.active:
                    new_n = int(bin(self.n.n)[:-8], 2)
                    self.root.ids.minimalna2.text = str(int(math.log(new_n, 37)))
                else:
                    self.root.ids.minimalna2.text = str(int(math.log(self.n.n, 37)))
            else:
                MDDialog(text="Wprowadzono niepoprawne granice").open()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = str(e)

    def zmien_minimalna(self) -> None:
        if self.root.ids.check.active:
            new_n = int(bin(self.n.n)[:-8], 2)
            self.root.ids.minimalna2.text = str(int(math.log(new_n, 37)))
        else:
            self.root.ids.minimalna2.text = str(int(math.log(self.n.n, 37)))

    def zaszyfruj_Rabin(self) -> None:
        """
        Funkcja szyfruj??ca wprowadzony tekst za pomoc?? funkcji szyfruj??cej zdefiniowanej dla systemu Rabina.
        Na pocz??tku edytowany zostaje wprowadzony tekst, p????niej podzielony na bloki odpowiedniej d??ugo??ci i
        w ostatniej cz????ci w zale??no??ci od wybranej opcji (wyb??r poprawnego tekstu jawnego lub wy??wietlanie czterech mo??liwych)
        nast??puje szyfrowanie za wykorzystuj??c funkcj?? szyfruj??c?? dla systemu Rabina.

        """

        try:
            if int(self.ciag) > 0:
                self.root.ids.odszyfrowane2.text = ""

                # Usuni??cie znak??w interpunkcyjnych, specjalnych
                Deletedot('pliki/wprowadzony_tekst', 'pliki/bez_znakow')
                # Podzielenie dokumentu na wyrazy n-literowe
                part_document('pliki/bez_znakow', int(self.ciag), 'pliki/podzielony')
                self.check = self.root.ids.check.active
                self.n.zakoduj_Rabin('pliki/zaszyfrowane', 'pliki/podzielony', self.check)
            else:
                MDDialog(text="Wprowadzono niepoprawny podzia??").open()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = "Nast??pi?? b????d szyfrowania"

    def odszyfruj_Rabin(self) -> None:
        """
        Funkcja deszyfruj??ca zaszyfrowan?? wiadomo???? dla systemu Rabina. Zwr??cony zostaje jeden tekst jawny
        lub wszystkie cztery w zale??no??ci od wybranej opcji.

        """
        try:
            self.n.odkoduj_Rabin('pliki/zaszyfrowane', self.p, self.q, 'pliki/odszyfrowane', self.check, self.ciag)
            with open('pliki/odszyfrowane.txt', encoding='utf-8', mode='r') as zak:
                self.root.ids.odszyfrowane2.text = zak.read()
        except Exception as e:
            self.root.ids.odszyfrowane2.text = str(e)

    def czy_pierwsza(self) -> None:
        """
        Funkcja sprawdzaj??ca pierwszo???? liczby za pomocu wybranego testu pierwszo??ci (Millera-Rabina lub Fermata).

        """
        slow = {True: "Prawda", False: "Fa??sz"}
        self.root.ids.pierwsza.text = ""
        if self.root.ids.Rabin.active:
            self.root.ids.pierwsza.text = slow[ps.prim.test_Millera_Rabina(int(self.root.ids.liczba.text), 20)]
        elif self.root.ids.Fermat.active:
            self.root.ids.pierwsza.text = slow[ps.prim.test_Fermata(int(self.root.ids.liczba.text), 20)]
        else:
            MDDialog(text='Nie wybrano ??adnej z opcji').open()

    def faktoryzacja(self) -> None:
        """
        Funkcja dokonuj??ca rozk??adu wprowadzonej liczby na czynniki pierwsze w zale??no??ci od wybranego
        algorytmu (pr??bnych dziele??, Fermata lub rho Pollarda).

        """
        self.root.ids.rozklad.text = ""
        if self.root.ids.probne.active:
            ps.prim.trial_divide2(int(self.root.ids.zlozona.text), self.root.ids.rozklad)
            self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        elif self.root.ids.fer.active:
            y = ps.prim.Fermat2(int(self.root.ids.zlozona.text), self.root.ids.rozklad, time.time())
            if True in (y, y):
                MDDialog(text="Przekroczono czas oblicze??", items='alert').open()
            else:
                self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        elif self.root.ids.Pollard.active:
            y = ps.prim.rho2(int(self.root.ids.zlozona.text), self.pollard_a, self.pollard_b, self.pollard_c,
                             50000, 2, self.root.ids.rozklad)
            if True in (y, y):
                MDDialog(text="Przekroczono liczb?? iteracji", items='alert').open()
            else:
                self.root.ids.rozklad.text = self.root.ids.rozklad.text[:-2]
        else:
            MDDialog(text='Nie wybrano ??adnej z opcji').open()

        text = self.root.ids.rozklad.text.split(',')
        if '' not in text:
            text = sorted(map(int, text))
            self.root.ids.rozklad.text = ", ".join(map(str, text))

    def domyslne_wspolczynniki(self):
        """
        Ustawienie domy??lnych wsp????czynnik??w funkcji kwadratowej dla metody rho Pollarda.
        """
        self.pollard_a = 1
        self.pollard_b = 0
        self.pollard_c = 5

    def zmien_Pollard(self) -> None:
        """
        Funkcja wy??wietlaj??ca okno dialogowe po naci??ni??ciu na przycisk dotycz??cy metody rho Pollarda.
        """
        self.content = Content()
        MDDialog(title="Wsp????czynniki funkcji kwadratowej:",
                 type="custom",
                 content_cls=self.content).open()

    def funkcja_Pollard(self, name: str) -> None:
        """
        Funkcja umo??liwiaja zmian?? wsp????czynnik??w dla funkcji kwadratowej wyst??puj??cej
        przy metodzie rho Pollarda.

        :param name: Okre??la, kt??ry wsp????czynnik ma zosta?? zmieniony

        """
        if name == "a":
            self.pollard_a = int(self.content.ids.pollard_a.text)
        elif name == "b":
            self.pollard_b = int(self.content.ids.pollard_b.text)
        elif name == "c":
            self.pollard_c = int(self.content.ids.pollard_c.text)

    def sprawdz(self) -> None:
        """
        Funkcja obliczaj??ca iloczyn czynnik??w pierwszych podanych przez wybrany algorytm faktoryzacji.

        """
        if self.root.ids.rozklad.text != "":
            t = self.root.ids.rozklad.text.split(',')
            self.root.ids.iloczyn.text = str(reduce(lambda x, y: x * y, [int(i) for i in t]))

    def pokaz_zaszyfrowany(self, tek: str) -> None:
        """
        Funkcja umo??liwiaj??ca wy??wietlenie zaszyfrowanego tekstu jawnego, w zale??no??ci od aktywnego ekranu.

        :param tek: Parametr okre??laj??cy aktywny ekran - tekst="RSA" system RSA, w przeciwnym razie ekran dla systemu Rabina

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
        Funkcja wy??wietlaj??ca pe??n?? posta?? liczby b??d??cej kluczem publicznym.

        :param opcja: Wyb??r warto??ci n lub b, opcja="n" lub opcja="b"

        """
        if opcja == "n":
            MDDialog(text=f'{self.n.n:,}').open()
        elif opcja == "b":
            MDDialog(text=f'{self.b:,}').open()

    def down(self, swit: MDSwitch, swit2: MDSwitch, swit3: MDSwitch, g: list) -> None:
        """
        Funkcja zmieniaj??ca tryb jasno??ci na wybranym ekranie.

        :param swit: Warto???? boolean okre??laj??ca, czy aktywny jest pierwszy ekran.
        :param swit2: Warto???? boolean okre??laj??ca, czy aktywny jest drugi ekran.
        :param swit3: Warto???? boolean okre??laj??ca, czy aktywny jest trzeci ekran.
        :param g: Lista zawieraj??ca kom??rki, dla kt??rych nale??y zmieni?? kolor.

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
