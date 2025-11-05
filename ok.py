def licz_sume_srednia_i_braki(plik):
    with open(plik, 'r', encoding='utf-8') as f:
        for nr_linii, linia in enumerate(f, start=1):
            wartosci = linia.strip().split(',')
            liczby = []
            brakujace = []  # indeksy brakujących lub nieliczbowych wartości

            for i, val in enumerate(wartosci):
                try:
                    liczby.append(float(val))
                except ValueError:
                    brakujace.append(i)

            if liczby:
                suma = sum(liczby)
                srednia = suma / len(liczby)
                print(
                    f"Linia {nr_linii}: suma = {suma:.2f}, średnia = {srednia:.2f}, "
                    f"brakujące indeksy = {brakujace}"
                )
            else:
                print(f"Linia {nr_linii}: brak liczb, brakujące indeksy = {brakujace}")

# użycie:
licz_sume_srednia_i_braki('latest.txt')
