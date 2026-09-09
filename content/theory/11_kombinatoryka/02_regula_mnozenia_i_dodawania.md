# 2. Reguła mnożenia i reguła dodawania

Dwie fundamentalne zasady kombinatoryki pozwalają błyskawicznie zliczać miliony kombinacji bez konieczności ich fizycznego wypisywania.

> **Definicja: Reguła mnożenia (Iloczyn wyborów)**
> Stosujemy, gdy wykonujemy po kolei **sekwencję $k$ niezależnych czynności** (krok 1 ORAZ krok 2 ORAZ krok $k$):
>
> $$N = n_1 \cdot n_2 \cdot \dots \cdot n_k$$
>
> Gdzie $n_i$ to liczba możliwości wykonania $i$-tej czynności.

Reguła dodawania (Rozłączne przypadki)

Stosujemy, gdy cel można osiągnąć wybierając **jeden z wykluczających się wariantów** (przypadek 1 LUB przypadek 2):

$$N = n_1 + n_2 + \dots + n_m$$

Warunek: żaden element nie może należeć do dwóch przypadków jednocześnie.

### Przykład 1: Tworzenie czterocyfrowego kodu PIN

Ile jest czterocyfrowych kodów PIN utworzonych z cyfr ze zbioru $\{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$:

**a) Gdy cyfry mogą się powtarzać:**

Na każdej z czterech pozycji mamy do wyboru $10$ cyfr (od 0 do 9):
$$N = 10 \cdot 10 \cdot 10 \cdot 10 = 10^4 = 10\,000$$

**b) Gdy wszystkie cyfry kodu muszą być różne (bez powtórzeń):**

Na pierwszej pozycji $10$ opcji, na drugiej $9$ (odpada użyta), na trzeciej $8$, na czwartej $7$:
$$N = 10 \cdot 9 \cdot 8 \cdot 7 = 5040$$

### Przykład 2: Łączne stosowanie reguły mnożenia i dodawania

W menu restauracji są $4$ zupy, $5$ dań głównych i $3$ desery. Klient decyduje się na obiad złożony z: zupy i dania głównego **LUB** dania głównego i deseru. Ile różnych zestawów może skomponować?

**Przypadek A (Zupa i danie główne):**

Rozbijamy zadanie na dwa rozłączne przypadki (reguła dodawania):

$4 \cdot 5 = 20$ możliwości (reguła mnożenia)
**Przypadek B (Danie główne i deser):** $5 \cdot 3 = 15$ możliwości (reguła mnożenia)

Łączna liczba zestawów wynosi:
$$N = 20 + 15 = 35$$

> **Wskazówka egzaminacyjna (Reguła językowa):**
> Słowo **„I” (koniunkcja)** $\implies$ **mnożenie** ($n_1 \cdot n_2$);
>
> Słowo **„LUB” (alternatywa)** $\implies$ **dodawanie** ($n_1 + n_2$).
