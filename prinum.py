import math
import random
import time
import numpy as np
import crypto as zs



class prim():
    def __init__(self, n: int):
        self.n = n


    def Sito_Erastotenesa(self) -> np.ndarray:
        """
        Funkcja generuje wszystkie liczby pierwsze do granicy utworzonej podczas tworzenia obiektu

        :return: Zwraca tablicę złożoną z liczb pierwszych
        """
        primes = [True] * (self.n - 1)
        primes = np.bool8(primes)
        war = np.arange(2, self.n + 1, 1)
        j = 2
        while j <= math.sqrt(self.n):
            if (primes[j - 2] == True):
                primes[war % j == 0] = False
                primes[j - 2] = True
            j += 1
        return war[primes == True]

    def SitoSund(self) -> np.ndarray:
        """
        Funkcja wyznacza wszystkie liczby pierwsze do podanej granicy

        :return: Zwraca tablicę liczb pierwszych
        """

        k = int(np.ceil((self.n - 2) / 2))
        x = np.arange(1, k + 1, 1)
        primes = [True] * k
        primes = np.bool8(primes)
        i = 1
        j = 1
        while i + j + 2 * i * j <= k:
            while i + j + 2 * i * j <= k:
                primes[i + j + 2 * i * j - 1] = False
                j += 1
            i += 1
            j = i
        x = x[primes == True]
        x = 2 * x + 1
        x = np.insert(x, 0, 2)
        return x

    @staticmethod
    def trial_divide2(n: int, t):
        """
        Funkcja rozkłada wprowadzoną liczbę na czynniki pierwsze za pomocą algorytmu próbnych dzieleń

        :param n: Liczba do rozkładu
        :param t: Komórka tekstowa, do której będzie wprowadzony rozkład
        :return: Zwraca wszystkie czynniki pierwsze podanej liczby
        """
        x = prim(int(math.sqrt(n)))
        tab = x.SitoSund()
        q = 1
        for y in tab:
            if n % y == 0:
                q = y
                break
        if n // q == 1:

            t.text += str(q)
            t.text += ', '
        elif q == 1:

            t.text += str(n // q)
            t.text += ', '
        else:
            return x.trial_divide2(q, t), x.trial_divide2(n // q, t)

    @staticmethod
    def rho2(n: int, a: int, b: int, c: int, B: int, pocz: int, t):
        """
        Funkcja rozkłada liczbę na czynniki pierwsze za pomocą metody rho Pollarda

        :param n: Liczba do rozkładu
        :param a: Współczynnik stojący przy kwadracie x
        :param b: Współczynnik stojący przy x
        :param c: Wyraz wolny
        :param B: Maksymalna liczba iteracji
        :param pocz: Punkt początkowy
        :param t: Komórka tekstowa, do której będzie wprowadzony rozkład
        :return: Zwraca wszystkie czynniki pierwsze podanej liczby
        """
        x = pocz
        y = pocz
        i = 0
        m = n
        d = 1
        if m % 2 == 0:
            t.text += str(2)
            t.text += ', '
            if m != 2:
                return prim.rho2(m // 2, a, b, c, B, pocz, t)
            else:
                return
        if m % 3 == 0:

            t.text += str(3)
            t.text += ', '
            if m != 3:
                return prim.rho2(m // 3, a, b, c, B, pocz, t)
            else:
                return
        while i < B:
            x = (a * x ** 2 + b * x + c) % m
            y = (a * y ** 2 + b * y + c) % m
            y = (a * y ** 2 + b * y + c) % m
            d = zs.Kryptografia.NWD(abs(y - x), m)
            if 1 < d < m:
                break
            if d == m:
                break
            i += 1
        if i == B:
            t.text = 'Przekroczono liczbę iteracji'
        else:
            if d == 1:
                t.text += str(m // d)
                t.text += ', '
            elif m // d == 1:
                t.text += str(d)
                t.text += ', '
            else:
                return prim.rho2(d, a, b, c, B, pocz, t), prim.rho2(m // d, a, b, c, B, pocz, t)


    @staticmethod
    def Fermat2(n: int, t, czas: float):
        """
        Funkcja rozkłada liczbę na czynniki pierwsze. Występuje ograniczenie czasowe, aby
        ograniczyć zbyt długie działanie metody.

        :param n: Liczba do rozkładu
        :param t: Komórka tekstowa, do której będzie wprowadzony rozkład
        :param czas: Ograniczenie czasowe
        :return: Zwraca wszystkie czynniki pierwsze liczby
        """

        x = math.ceil(math.sqrt(n))
        p = n
        q = 1
        if n % 2 == 0:
            t.text += str(2)
            t.text += ', '
            if n != 2:
                return prim.Fermat2(n // 2, t, czas)
            else:
                return

        while x <= (n + 1) // 2:
            y = int((x ** 2 - n) ** (1 / 2))
            if x ** 2 - y ** 2 == n:
                break
            if time.time() - czas > 10:
                return False
            x += 1
        if x != (n + 1) // 2:
            p = x + y
            q = x - y
        q, p = int(q), int(p)

        if q == 1:
            t.text += str(p) + ', '
        else:
            return prim.Fermat2(p, t, czas), prim.Fermat2(q, t, czas)


    @staticmethod
    def test_Millera_Rabina(x: int, liczba_testow: int) -> bool:
        """
        Funkcja wykonuje test pierwszości dla wprowadzonej liczby
        bazującu na teście Millera-Rabina.

        :param x: Liczba, która ma zostać sprawdzona
        :param liczba_testow: Liczba testów, które mają zostać przeprowadzone
        :return: Zwraca wartość True lub False, True oznacza, że liczba prawdopodobnie jest pierwsza False oznacza, że liczba jest złożona
        """
        n = zs.Kryptografia(x, 1)
        s = 0
        x = x - 1
        if liczba_testow >= x:
            liczba_testow = x - 1
        while x % 2 == 0:
            s += 1
            x //= 2
        d = x
        tab = [False] * liczba_testow
        a = []

        for i in range(0, liczba_testow):
            t = random.randint(1, n.n - 1)
            while t in a:
                t = random.randint(1, n.n - 1)
            a.append(t)
            for r in range(0, s):
                if r == 0:
                    if int(n.fme(a[i], 2 ** r * d)) == 1:
                        tab[i] = True
                    if int(n.fme(a[i], 2 ** r * d)) == -1 % n.n:
                        tab[i] = True
                else:
                    if int(n.fme(a[i], 2 ** r * d)) == -1 % n.n:
                        tab[i] = True

        return tab == [True] * liczba_testow

    @staticmethod
    def test_Fermata(x: int, testy: int):
        """
        Funkcja wykonuje test pierwszości dla podanej liczby bazujący na teście Fermata.

        :param x: Liczba, która ma zostać sprawdzona
        :param liczba_testow: Liczba testów, które mają zostać przeprowadzone
        :return: Zwraca wartość True lub False, True oznacza, że liczba prawdopodobnie jest pierwsza False oznacza, że liczba jest złożona
        """
        n = zs.Kryptografia(x, 1)
        pierwsza = True
        pop = []
        if testy >= x:
            testy = x - 1
        for _ in range(testy):
            a = random.randint(1, x - 1)
            while a in pop:
                a = random.randint(1, x - 1)
            pop.append(a)
            # print(n.fme(a, x - 1))
            if n.fme(a, x - 1) != 1:
                pierwsza = False
                break
        return pierwsza


if __name__ == '__main__':
    help(prim.test_Fermata)