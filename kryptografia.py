import math
import random

slownik = {0: 'A', 1: 'Ą', 2: 'B', 3: 'C', 4: 'Ć', 5: 'D', 6: 'E', 7: 'Ę', 8: 'F', 9: 'G', 10: 'H',
           11: 'I', 12: 'J', 13: 'K', 14: 'L', 15: 'Ł', 16: 'M', 17: 'N', 18: 'Ń', 19: 'O', 20: 'Ó',
           21: 'P', 22: 'Q', 23: 'R', 24: 'S', 25: 'Ś', 26: 'T', 27: 'U', 28: 'V', 29: 'W', 30: 'X',
           31: 'Y', 32: 'Z', 33: 'Ż', 34: 'Ź', 35: ' '}

slownikodw = {'A': 0, 'Ą': 1, 'B': 2, 'C': 3, 'Ć': 4, 'D': 5, 'E': 6, 'Ę': 7, 'F': 8, 'G': 9, 'H': 10,
              'I': 11, 'J': 12, 'K': 13, 'L': 14, 'Ł': 15, 'M': 16, 'N': 17, 'Ń': 18, 'O': 19, 'Ó': 20,
              'P': 21, 'Q': 22, 'R': 23, 'S': 24, 'Ś': 25, 'T': 26, 'U': 27, 'V': 28, 'W': 29, 'X': 30,
              'Y': 31, 'Z': 32, 'Ż': 33, 'Ź': 34, ' ': 35}

N = 36


class Kryptografia():
    def __init__(self, p, q):
        self.n = p * q
        self.p = p
        self.q = q
        self.y = 8

    @staticmethod
    def NWD(a: int, b: int) -> int:
        """
        Funkcja oblicza największy wspólny dzielnik wprowadzonych wartości.

        :param a: Pierwsza liczba
        :param b: Druga liczba
        :return: Zwraca NWD dla podanych liczb
        """
        a = abs(a)
        b = abs(b)
        max1, min1 = max(a, b), min(a, b)
        if min1 == 0:
            return max1
        else:
            w = max1 % min1
            if w == 0:
                return min1
            else:
                return Kryptografia.NWD(min1, w)

    def fme(self, a: int, e: int) -> int:
        """
        Funkcja oblicza potęgowanie modularne wykorzystując algorytm "podnieś do kwadratu i wymnóż"
        dla modułu określonego podczas tworzenia obiektu klasy.

        :param a: Podstawa potęgi
        :param e: Wykładnik potęgi
        :return: Zwraca wynik potęgowania modularnego
        """
        x = 1
        y = a
        f = e
        while f > 0:
            if f % 2 == 0:
                y = (y ** 2) % self.n
                f = f // 2
            else:
                x = x * y % self.n
                f -= 1
        return x

    def phi(self) -> int:
        """
        Funkcja obliczająca liczbę liczb względnie pierwszych z n, mniejszych od n
        dla n będącego iloczynem dwóch liczb pierwszych

        :return: Zwraca wartość funkcji phi(n)
        """
        return (self.p - 1) * (self.q - 1)

    @staticmethod
    def RozszEuk(phi: int, a: int) -> int or None:
        """
        Funkcja wyznacza element odwrotny do podanego przy zadanym module
        za pomocą rozszerzonego algorytmu Euklidesa.

        :param phi: Moduł
        :param a: Liczba, dla której wyznaczany będzie element odwrotny
        :return: Zwraca element odwrotny do a mod phi
        """
        n0 = phi
        b0 = a
        t0 = 0
        t = 1
        q = math.floor(n0 / b0)
        r = n0 - q * b0
        while r > 0:
            temp = (t0 - q * t) % phi
            t0 = t
            t = temp
            n0 = b0
            b0 = r
            q = math.floor(n0 / b0)
            r = n0 - q * b0
        if b0 != 1:
            return None
        else:
            return t % phi

    def przelicz(self, tab: list) -> list:
        """
        Funkcja zamieniająca bloki k-wyrazowe na wartości liczbowe

        :param tab: Tablica zawierająca bloki, które należy zamienić na wartości liczbowe
        :return: Zwraca tablice z wartościami liczbowymi
        """
        przel = []
        for i in range(0, len(tab)):
            j = len(tab[i]) - 1
            suma = 0
            for x in tab[i]:
                suma += int(int(slownikodw[x]) * pow(N, j))
                j -= 1
            przel.append(suma)

        return przel

    # Zamiana slow na liczby
    def slowanaliczby(self, nazwa: str) -> list:
        """
        Funkcja otwiera plik zawierający bloki k-wyrazowe i wywołuje funkcję przelicz
        w celu zamiany ciągów liter na liczby

        :param nazwa: Nazwa pliku, w którym zapisane są bloki k-wyrazowe
        :return: Zwraca wartości liczbowe odpowiadające blokom
        """
        with open(f'{nazwa}.txt', encoding='utf-8', mode='r') as z:
            zak = z.read().upper()
            lines = zak.split('\n')
        przel = self.przelicz(lines)
        return przel

    @staticmethod
    def odwproc2(a: int, ciag: int) -> list:
        """
        Funkcja odwracająca proces zamiany ciągów literowych na wartość liczbową

        :param a: Wartość liczbowa, która ma zostać rozłożona na litery
        :param ciag: Podział wyrazów
        :return: Zwraca tablicę z wartościmi liczbowymi odpowiadającymi literom lub spacji
        """

        y = []
        ciag -= 1
        if a > 0:
            if int(math.log(a, N)) > ciag:
                ciag = int(math.log(a, N))
        while ciag != -1:
            u = a // N ** ciag
            y.append(u)
            a -= u * N ** ciag
            ciag -= 1

        return y

    def kodowanie(self, tab: list, b: int) -> list:
        """
        Funkcja szyfrująca wiadomości za pomocą systemu RSA

        :param tab: Tablica zawierająca wartości do zaszyfrowania
        :param b: Wykładnik potęgi funkcji szyfrującej
        :return: Zwraca tablicę z zaszyfrowanymi wartościami
        """
        zak = []
        for x in tab:
            zak.append(self.fme(x, b))
        return zak

    def kodowanie_Rabin(self, tab: list) -> list:
        """
        Funkcja szyfrująca tekst jawny za pomocą systemu Rabina nieumożliwiająca wyboru poprawnego tekstu
        spośród czterech możliwych

        :param tab: Tablica zawierająca wartości do zaszyfrowania
        :return: Zwraca tablicę z zaszyfrowanymi wartościami
        """
        zak = []
        for t in tab:
            zak.append((t ** 2) % self.n)
        return zak

    def kodowanie_Rabin2(self, tab: list, m: int) -> list:
        """
        Funkcja szyfrująca tekst jawny za pomocą systemu Rabina pozwalająca na wybór poprawnego tekstu
        spośród czterech możliwych wykorzystując powtórzenie m/2 początkowych bitów oraz m/2 końcowych bitów.

        :param tab: Tablica zawierająca wartości do zaszyfrowania
        :param m: Całkowita liczba bitów, które mają zostać powtórzone
        :return: Zwraca tablicę z zaszyfrowanymi wartościami


        """
        zak = []
        for t in tab:
            if t >= 2 ** (m - 1):
                n = bin(t)
                t = int(n + n[2:2 + m // 2] + n[-(m - m // 2):], 2)
            zak.append((t ** 2) % self.n)
        return zak

    @staticmethod
    def Tonelli_Shanks(p: int, a: int) -> tuple:
        """
        Funkcja obliczająca pierwiastki kwadratowe przy podanym module.

        :param p: Moduł
        :param a: Liczba, dla której mają zostać wyznaczone pierwiastki kwadratowe
        :return: Zwraca dwa pierwiastki kwadratowe mod p
        """
        n = Kryptografia(p, 1)
        s = 0
        p = p - 1
        while p % 2 == 0:
            s += 1
            p //= 2
        Q = p
        z = 2
        while n.fme(z, (n.n - 1) // 2) % n.n != -1 % n.n:
            z += 1
        M = s
        c = n.fme(z, Q)
        t = n.fme(a, Q)
        R = n.fme(a, (Q + 1) // 2)

        if t == 0:
            return 0, 0
        elif n.fme(a, (n.n - 1) // 2) != 1:
            return 0, 0
        else:
            while t != 1:
                for i in range(1, M):
                    if n.fme(t, 2 ** i) == 1:
                        b = n.fme(c, 2 ** (M - i - 1))
                        M = i
                        c = b ** 2 % n.n
                        t = t * b ** 2 % n.n
                        R = R * b % n.n

                        break
        return R, -R

    @staticmethod
    def oblicz_a(p: int, q: int) -> tuple:
        """
        Funkcja wyznaczająca liczby takie, że aq+bp=1

        :param p: Liczba pierwsza
        :param q: Liczba pierwsza
        :return: Zwraca wartości całkowite a i b
        """
        a = pow(q, -1, mod=p)
        b = a * q // p
        return a, -b

    def oblicz_x_y(self, p: int, q: int, c: int) -> tuple:
        """
        Funkcja wyznaczająca wszystkie cztery teksty jawne odpowiadające podanej wartości.

        :param p: Liczba pierwsza
        :param q: Liczba pierwsza
        :param c: Liczba dla której mają zostać wyznaczone cztery pierwiastki
        :return: Zwraca cztery teksty jawne odpowiadające zaszyfrowanej wiadomości c
        """
        r, _ = self.Tonelli_Shanks(p, c)
        s, _ = self.Tonelli_Shanks(q, c)
        a, b = self.oblicz_a(p, q)
        x = (r * a * q + s * p * b) % self.n
        y = (r * a * q - s * p * b) % self.n
        return x, y, -x % self.n, -y % self.n

    def odwroc_Rabin(self, p: int, q: int, y: int, m: int) -> int:
        """
        Funkcja wybierająca poprawny tekst jawny spośród czterech możliwych
        charakteryzujący się powtórzoną liczbą bitów.

        :param p: Liczba pierwsza
        :param q: Liczba pierwsza
        :param y: Zaszyfrowana wiadomość
        :param m: Całkowita liczba powtórzonych bitów
        :return: Zwraca wartość spełniającą zadane kryterium
        """
        t1, t2, t3, t4 = self.oblicz_x_y(p, q, y)
        t = min([t1, t2, t3, t4])
        if t < 2 ** (m - 1):
            return t
        if bin(t1)[2:2 + m // 2] == bin(t1)[-m:-m // 2] and bin(t1)[-m // 2:] == bin(t1)[-(2 * m - m // 2):-m]:
            return int(bin(t1)[0:-m], 2)
        if bin(t2)[2:2 + m // 2] == bin(t2)[-m:-m // 2] and bin(t2)[-m // 2:] == bin(t2)[-(2 * m - m // 2):-m]:
            return int(bin(t2)[0:-m], 2)
        if bin(t3)[2:2 + m // 2] == bin(t3)[-m:-m // 2] and bin(t3)[-m // 2:] == bin(t3)[-(2 * m - m // 2):-m]:
            return int(bin(t3)[0:-m], 2)
        if bin(t4)[2:2 + m // 2] == bin(t4)[-m:-m // 2] and bin(t4)[-m // 2:] == bin(t4)[-(2 * m - m // 2):-m]:
            return int(bin(t4)[0:-m], 2)

    def odwroc_Rabin3(self, p: int, q: int, y: int) -> tuple:
        """
        Funkcja zwracająca cztery możliwe teksty jawne

        :param p: Liczba pierwsza
        :param q: Liczba pierwsza
        :param y: Zaszyfrowana wiadomość
        :return: Zwraca cztery teksty jawne w postaci liczbowej odpowiadające y
        """
        return self.oblicz_x_y(p, q, y)

    def odszyfr_Rabin(self, plik, p: int, q: int, ciag: int) -> str:
        """
        Funkcja odszyfrowująca wiadomości dla systemu Rabina

        :param plik: Plik zawierający tekst zaszyfrowany
        :param p: Liczba pierwsza, czynnik liczby n
        :param q: Liczba pierwsza, czynnik liczby n
        :param ciag: Podział wyrazów
        :return: Zwraca dokładnie jeden tekst jawny
        """
        zak = plik.read()
        lines = zak.split('\n')
        linskr = []
        zakodow = []
        for x in lines:
            linskr.append(x.split(' '))
        for y in range(0, len(linskr)):
            for x in linskr[y]:
                zakodow.append(x)
        odk = []

        for y in zakodow:
            g = self.odwroc_Rabin(p, q, int(y), self.y)
            odk.append(self.odwproc2(g, ciag))
        odkslow = []

        for t in odk:
            e = ""
            for w in t:
                e += slownik[w]
            odkslow.append(e)
        return "".join(odkslow)

    ###########################################################
    def odszyfr_Rabin2(self, plik, p: int, q: int, ciag: int):
        """
        Funkcja odszyfrowująca wiadomość dla systemu Rabina bez wykorzystania powtarzania bitów.

        :param plik: Plik zawierający tekst zaszyfrowany
        :param p: Liczba pierwsza, czynnik liczby n
        :param q: Liczba pierwsza, czynnik liczby n
        :param ciag: Podział wyrazów
        :return: Dla każdego tekstu zaszyfrowanego zwraca cztery teksty jawne
        """
        zak = plik.read()
        lines = zak.split('\n')
        linskr = []
        zakodow = []
        for x in lines:
            linskr.append(x.split(' '))
        for y in range(0, len(linskr)):
            for x in linskr[y]:
                zakodow.append(x)
        odk = []
        for y in zakodow:
            g = self.odwroc_Rabin3(p, q, int(y))
            for m in g:
                odk.append(self.odwproc2(m, ciag))

        odkslow = []
        for t in odk:
            e = ""
            for w in t:
                e += slownik[w]
            odkslow.append(e)
        return odkslow

    def odszyfr_RSA(self, plik, a: int, ciag: int) -> str:
        """
        Funkcja deszyfrująca wiadomość dla systemu RSA.

        :param plik: Plik zawierająca tekst zaszyfrowany
        :param a: Wykładnik potęgi funkcji deszyfrującej
        :param ciag: Podział wyrazów
        :return: Zwraca odszyfrowany tekst jawny
        """
        zak = plik.read()
        lines = zak.split('\n')
        linskr = []
        zakodow = []

        for x in lines:
            linskr.append(x.split(' '))
        for y in range(0, len(linskr)):
            for x in linskr[y]:
                zakodow.append(x)
        odk = []
        k = 0

        for y in zakodow:
            g = self.fme(int(y), a)
            odk.append(self.odwproc2(g, ciag))
            k += 1
        odkslow = []
        for t in odk:
            e = ""
            for w in t:
                e += slownik[w]
            odkslow.append(e)
        return "".join(odkslow)

    @staticmethod
    def zapis(tab: list, plik):
        """
        Funkcja zapisująca zaszyfrowany tekst do pliku o formacie txt.

        :param tab: Tablica zawierająca zaszyfrowane wielkości
        :param plik: Plik, w którym zostanie zapisany zaszyfrowany tekst
        :return: Zwraca plik z zaszyfrowanym tekstem
        """
        file_content = "\n".join(str(t) for t in tab)
        plik.write(file_content)
        plik.close()
        return plik

    def zakoduj_RSA(self, b: int, nazwa: str, zakod: str) -> None:
        """
        Funkcja wywołująca wszystkie metody szyfrujące dla systemu RSA.

        :param b: Wykładnik potęgi funkcji szyfrującej
        :param nazwa: Nazwa pliku, w którym ma zostać zapisana zaszyfrowana wiadomość
        :param zakod: Tekst jawny, który ma zostać zaszyfrowany
        """
        nazwa += ".txt"
        plik = open(f'{nazwa}', 'w')
        przel = self.slowanaliczby(zakod)

        tab = self.kodowanie(przel, b)
        self.zapis(tab, plik)

    def zakoduj_Rabin(self, nazwa: str, zakod: str, check: bool) -> None:
        """
        Funkcja wywołująca wszystkie metody szyfrujące dla systemu Rabina w zależności od wyboru
        wyświetlanie tekstu jawnego

        :param nazwa: Nazwa pliku, w którym ma zostać zapisana zaszyfrowana wiadomość
        :param zakod: Tekst jawny, który ma zostać zaszyfrowany
        :param check: Wartość określająca, czy została wybrana opcja wyświetlania tylko poprawnego tekstu jawnego
        check=True wyświetlanie poprawnego tekstu, check= False wyświetlanie czterech możliwych tekstów
        """

        nazwa += ".txt"
        plik = open(f'{nazwa}', 'w')
        przel = self.slowanaliczby(zakod)

        if check:
            tab = self.kodowanie_Rabin2(przel, self.y)
        else:
            tab = self.kodowanie_Rabin(przel)
        self.zapis(tab, plik)

    def odkoduj_RSA(self, nazwa: str, a: int, name_file: str, ciag: int) -> None:
        """
        Funkcja wywołująca wszystkie metody deszyfrujące dla systemu RSA.

        :param nazwa: Nazwa pliku zawierającego zaszyfrowany tekst
        :param a: Wykładnik potęgi funkcji deszyfrującej
        :param name_file: Nazwa pliku, w którym zostanie zapisany odszyfrowany tekst jawny
        :param ciag: Podział wyrazów
        """
        nazwa += ".txt"
        plik = open(nazwa, 'r')
        odkodow = self.odszyfr_RSA(plik, a, ciag)
        odk = name_file
        odk += ".txt"
        with open(f'{odk}', encoding='utf-8', mode='w') as kod:
            file_content = odkodow
            kod.write(file_content)

    def odkoduj_Rabin(self, nazwa: str, p: int, q: int, name_file: str, check: bool, ciag: int) -> None:
        """
        Funkcja wywołująca wszystkie metody deszyfrujące dla systemu Rabina.

        :param nazwa: Nazwa pliku zawierającego zaszyfrowany tekst
        :param p: Liczba pierwsza, czynnik liczby n
        :param q: Liczba pierwsza, czynnik liczby n
        :param name_file: Nazwa pliku, w którym zostanie zapisany odszyfrowany tekst jawny
        :param check: Wartość określająca, czy została wybrana opcja wyświetlania tylko poprawnego tekstu jawnego
        :param ciag: Podział wyrazów
        check=True wyświetlanie poprawnego tekstu, check= False wyświetlanie czterech możliwych tekstów
        """
        nazwa += ".txt"
        plik = open(nazwa, 'r')
        if check:
            odkodow = self.odszyfr_Rabin(plik, p, q, ciag)
        else:
            odkodow = self.odszyfr_Rabin2(plik, p, q, ciag)
            odkodow = " ".join(odkodow)
        odk = name_file
        odk += ".txt"
        with open(f'{odk}', encoding='utf-8', mode='w') as kod:
            file_content = odkodow
            kod.write(file_content)


if __name__ == '__main__':
    print(Kryptografia.Tonelli_Shanks(65537, 7662))
