# 3. Złożone zadania kombinatoryczne z warunkami na cyfry

Zadania sprawdzające umiejętność zliczania liczb wielocyfrowych o określonych cechach (parzystość, określona liczba powtórzeń wybranych cyfr) to standard na nowym egzaminie podstawowym.

> **Definicja: Metoda pozycji (okienkowa) i reguły tworzenia liczb**
> - **Pierwsza cyfra (cyfra najwyższego rzędu):** W liczbie $k$-cyfrowej pierwsza cyfra **nigdy nie może być zerem** ($c_1 \in \{1, 2, \dots, 9\}$ – $9$ możliwości).
> - **Parzystość / Nieparzystość:** O parzystości decyduje wyłącznie **ostatnia cyfra**:
>
> Liczba parzysta: ostatnia cyfra $\in \{0, 2, 4, 6, 8\}$ ($5$ możliwości).
> Liczba nieparzysta: ostatnia cyfra $\in \{1, 3, 5, 7, 9\}$ ($5$ możliwości).
> - **Zasada rozmieszczania:** Jeśli w liczbie ma wystąpić dokładnie jedna cyfra $A$ i dokładnie jedna $B$, najpierw wybieramy **pozycje** dla tych cyfr, a pozostałe miejsca wypełniamy pozostałymi cyframi ze zbioru $\{0, 1, \dots, 9\} \setminus \{A, B\}$ (8 możliwości).

### Przykład 1 (Wymaganie egzaminacyjne): Czterocyfrowe liczby nieparzyste z jedną cyfrą 1 i jedną 2

Oblicz, ile jest czterocyfrowych nieparzystych liczb całkowitych dodatnich takich, że w ich zapisie dziesiętnym występuje **dokładnie jedna cyfra 1** i **dokładnie jedna cyfra 2**.

**Przypadek 1: Cyfra 1 stoi na końcu (miejsce 4.)**

Liczba jest nieparzysta, więc na ostatnim (czwartym) miejscu musi stać cyfra nieparzysta. Cyfra $2$ nie może stać na końcu! Zastanawiamy się, gdzie stoi cyfra $1$:

Postać liczby: $\_ \_ \_ 1$

Cyfra $2$ musi zająć jedno z $3$ pozostałych miejsc ($3$ możliwości).

Pozostałe $2$ wolne miejsca wypełniamy cyframi ze zbioru $\{0, 3, 4, 5, 6, 7, 8, 9\}$ (jest ich $8$), ale na pierwszym miejscu nie może stać $0$ ($7$ możliwości), a na drugim dowolna z $8$ cyfr ($8$ możliwości).

• Jeśli cyfra $2$ stoi na 1. miejscu: $1 \cdot 8 \cdot 8 = 64$ możliwości.

• Jeśli cyfra $2$ stoi na 2. lub 3. miejscu ($2$ opcje): na 1. miejscu stoi cyfra ze zbioru bez $0, 1, 2$ ($7$ opcji), na wolnym miejscu dowolna z $8$ opcji: $2 \cdot (7 \cdot 8) = 112$ możliwości.

Łącznie w Przypadku 1: $64 + 112 = 176$ liczb.

**Przypadek 2: Cyfra 1 NIE stoi na końcu**

Na końcu musi stać cyfra nieparzysta inna niż $1$: $\{3, 5, 7, 9\}$ ($4$ możliwości).

Cyfry $1$ i $2$ muszą zająć dwa z pierwszych trzech miejsc. Liczba par pozycji to $3 \cdot 2 = 6$ możliwości.

Pozostałe jedno wolne miejsce wypełniamy cyfrą ze zbioru bez $1$ i $2$ ($8$ możliwości), pamiętając o zerze na początku:

• Gdy na 1. miejscu stoi $1$ lub $2$ ($2$ opcje): drugą z nich stawiamy na miejscu 2. lub 3. ($2$ opcje), a na wolnym miejscu dowolną z $8$ cyfr: $2 \cdot 2 \cdot 8 \cdot 4 = 128$ możliwości.

• Gdy na 1. miejscu stoi inna cyfra: nie może być zerem, ani $1$, ani $2$ ($7$ możliwości), a cyfry $1$ i $2$ zajmują miejsca 2. i 3. ($2$ opcje): $7 \cdot 2 \cdot 4 = 56$ możliwości.

Łącznie w Przypadku 2: $128 + 56 = 184$ liczby.

**Razem:** $176 + 184 = 360$ liczb.

> **Wskazówka egzaminacyjna (Wskazówka):**
> W zadaniach z cyframi zawsze zaczynaj analizę od **miejsc najbardziej ograniczonych**: najpierw ostatnie miejsce (warunek parzystości), potem pierwsze miejsce (zakaz zera), a na końcu pozostałe wolne pozycje.
