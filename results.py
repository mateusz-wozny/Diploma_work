import crypto as zs
import math
from time import time
import pandas as pd
from prinum import prim
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os


def Pollard(n: int, czas: float, a=1, b=0, c=3, B=1000000, pocz=2):
    """
    Funkcja rozkłada wprowadzoną liczbę na dwa czynniki, niekoniecznie pierwsze
    za pomocą metody rho Pollarda

    :param n: Liczba, która ma zostać rozłożona
    :param czas: float
    :param a: Współczynnik stojący przy kwadracie x
    :param b: Współczynnik stojący przy x
    :param c: Wyraz wolny
    :param B: Maksymalna liczba iteracji
    :param pocz: Punkt początkowy
    :return: Zwraca czynniki liczby oraz czas obliczeń
    """
    x = pocz
    y = pocz
    i = 0
    m = n
    d = 1

    while i < B:
        x = (a * x ** 2 + b * x + c) % m
        y = (a * y ** 2 + b * y + c) % m
        y = (a * y ** 2 + b * y + c) % m
        d = zs.Kryptografia.NWD(abs(y - x), m)
        if 1 < d < m:
            break
        if d == m:
            break
        if time() - czas > 20:
            return 0, 0, time() - czas
        i += 1
    if i == B:
        print('Przekroczono liczbę iteracji')
    else:
        if d == 1:
            return m
        elif m // d == 1:
            return d
        else:
            return d, m // d, time() - czas


def trial_divide(n: int, czas: float):
    """
    Funkcja rozkłada wprowadzoną liczbę na dwa czynniki, niekoniecznie pierwsze
    za pomocą algorytmu próbnych dzieleń

    :param n: Liczba, która ma zostać rozłożona
    :param czas: float
    :return: Zwraca czynniki liczby oraz czas obliczeń
    """
    tab = range(2, int(n ** (1 / 2)))
    q = 1
    for y in tab:
        if n % y == 0:
            q = y
            break
        if time() - czas > 20:
            # print("Przekroczono czas obliczeń")
            return 0, 0, time() - czas
    if n // q == 1:
        return q
    elif q == 1:
        return n
    else:
        return q, n // q, time() - czas


def Fermat(n: int, czas: float):
    """
    Funkcja rozkłada wprowadzoną liczbę na dwa czynniki, niekoniecznie pierwsze
    za pomocą algorytmu Fermata

    :param n: Liczba, która ma zostać rozłożona
    :param czas: float
    :return: Zwraca czynniki liczby oraz czas obliczeń
    """
    x = math.ceil(n ** (1 / 2))
    p = n
    q = 1
    while x <= (n + 1) // 2:
        y = int((x ** 2 - n) ** (1 / 2))
        if x ** 2 - y ** 2 == n:
            break
        if time() - czas > 20:
            return 0, 0, time() - czas
        x += 1
    if x != (n + 1) // 2:
        p = x + y
        q = x - y
    q, p = int(q), int(p)
    if q == 1:
        return p
    else:
        return q, n // q, time() - czas


def porownanie(alg: str) -> None:
    """
    Wyznaczanie czasu obliczeń dla wybranego algorytmu faktoryzacji
    dla p i q określonych w podanym pliku xlsx.

    :param alg: Wybór algorytmu faktoryzacji alg="P" metoda Pollarda, alg="F" algorytm Fermata, alg="T" algorytm próbnych dzieleń
    """

    slow = {'P': 'Pollard', 'F':'Fermat', 'T':'Próbne'}
    df = pd.read_excel('Faktoryzacja/Faktoryzacjav2.xlsx')
    wyn = []
    for p, q in zip(df['p'], df['q']):
        if alg == 'P':
            x = Pollard(p * q, time())
        elif alg == 'F':
            x = Fermat(p * q, time())
        elif alg == 'T':
            x = trial_divide(p * q, time())
        wyn.append([p * q, round(p / q, 5), x[2]])
    wynik = pd.DataFrame(data=wyn, columns=['n', 'p/q', 'Czas obliczeń'])
    wynik.to_json(f'Faktoryzacja/{slow[alg]}.json')


def wykres_faktoryzacja(dane: pd.DataFrame, nazwa: str) -> None:
    """
    Funkcja tworzy wykres punktowy wraz ze skalą kolorów dla wprowadzonych danych
    Utworzony wykres jest zapisywany w folderze Faktoryzacja pod podaną nazwą.

    :param dane: Tablica zawierająca dane
    :param nazwa: Nazwa pliku

    """
    sns.relplot(
        data=dane,
        x="n [-]", y="p/q [-]", hue="Czas [s]", palette="viridis",
        hue_norm=(0, 20), height=3.6
    )

    plt.xscale("log")
    plt.yscale("log")
    plt.savefig(f'Faktoryzacja/{nazwa}.png')


def generuj_wykres() -> None:
    """
    Funkcja generuje wykresy dla każdego algorytmu faktoryzacji przedstawionego w pracy
    Wykorzystuje bezpośrednio funkcję wykres_faktoryzacja.

    """
    path = os.listdir('Faktoryzacja')
    for p in path:
        if 'json' in p:
            with open(f'Faktoryzacja/{p}', 'r') as f:
                df = pd.DataFrame(json.load(f))
            df = df.rename(columns={"n": "n [-]", "p/q": "p/q [-]", "Czas obliczeń": "Czas [s]"})
            wykres_faktoryzacja(df, p[:-5])


def porownanie_algorytmow(sito_Sundarama: bool, nazwa: str) -> None:
    """
    Funkcja umożliwia wyznaczanie czasu obliczeń dla sito Sundarama
    lub dla sita Eratostenesa
    Uzyskany wynik jest zapisywany w pliku o formacie xlsx.

    :param sito_Sundarama: Wybór sita liczbowe True- Sundarama, False- Eratostenes
    :param nazwa: Nazwa pliku, do którego ma zostać zapisany wynik

    """
    n = range(1, 10)
    p = [i * 10 ** j for j in range(4, 7) for i in n]
    p.append(10 ** 7)
    wynik = []
    for i in p:
        t = prim(i)
        start = time()
        if sito_Sundarama:
            t.SitoSund()
        else:
            t.Sito_Erastotenesa()
        stop = time()
        if stop - start > 90:
            break
        wynik.append([i, stop - start])

    df = pd.DataFrame(data=wynik, columns=['Wartość', 'Czas'])
    df.to_excel(f'{nazwa}.xlsx', index=False)


def wykres_generowanie() -> None:
    """
    Funkcja generuje wykresy dla porównania sita Eratostenesa oraz Sundarama
    Tworzy 3 wykresy punktowe i automatycznie zapisuje je w folderze Generowanie.

    """
    df1 = pd.read_excel('Generowanie/Sundarama.xlsx')
    df2 = pd.read_excel('Generowanie/Eratostenes.xlsx')
    # Wykres porównawczy
    fig = plt.scatter(df1['Wartość'], df1['Czas'])
    fig2 = plt.scatter(df2['Wartość'], df2['Czas'])
    plt.legend((fig, fig2), ("Sito Sundarama", "Sito Eratostenesa"))
    plt.xscale("log")
    plt.xlabel("Granica [-]")
    plt.ylabel("Czas obliczeń [s]")
    plt.savefig('Generowanie/porównanie.png')

    opis = {"Sundarama": df1, "Eratostenes": df2}
    # Pojedyncze wykresy
    for i in opis.keys():
        df = opis[i]
        plt.figure()
        plt.scatter(df["Wartość"], df["Czas"])
        plt.xscale("log")
        plt.xlabel("Granica [-]")
        plt.ylabel("Czas obliczeń [s]")
        plt.savefig(f"Generowanie/Sito{i}.png")


if __name__ == "__main__":
    generuj_wykres()
