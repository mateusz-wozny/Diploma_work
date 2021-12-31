from kryptografia import slownikodw



def part_document(file: str, step: int, new_file: str) -> None:
    """
    Funkcja dzieląca wprowadzony plik na bloki o określonej długości

    :param file: Nazwa pliku, który ma zostać poddany edycji
    :param step: Wielkość podziału wyrazu
    :param new_file: Nazwa nowego pliku

    """
    with open(file + ".txt", encoding='utf-8', mode='r') as zak:
        lines = zak.read().split('\n')

    u="".join(lines)
    oddz2=[]
    krok=len(u)//step
    for i in range(krok):
        oddz2.append(u[i*step:(i+1)*step])
    oddz2.append(u[krok*step:]+" "*(step-len(u)+krok*step))
    new_file += ".txt"
    with open(new_file, encoding='utf-8', mode='w') as file:
        file_content = "\n".join(oddz2)
        file.write(file_content)



def Deletedot(file, new_file) -> None:
    """
    Funkcja z podanego pliku usuwa wszystkie znaki interpunkcyjne, cyfry, znaki specjalne.
    Pozostawia jedynie litery oraz spacje.

    :param file: Nazwa pliku, który ma zostać poddany edycji
    :param new_file: Nazwa nowego pliku
    """
    file += ".txt"
    keys = list(slownikodw.keys())


    with open(file, encoding='utf-8', mode='r') as zak:
        znak = zak.read(1).upper()
        odk = new_file
        odk += ".txt"
        with open(odk, encoding='utf-8', mode='w') as kod:
            while znak:
                if znak in keys:
                    kod.write(znak)
                znak = zak.read(1).upper()


if __name__ == '__main__':
    help(Deletedot)