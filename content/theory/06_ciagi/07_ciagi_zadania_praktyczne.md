# 7. Własności ciągów w zadaniach praktycznych i tekstowych

Zadania z kontekstem realistycznym na egzaminie weryfikują umiejętność rozpoznania odpowiedniego modelu matematycznego:

- **Ciąg arytmetyczny:** stosujemy, gdy wielkość zmienia się **o stałą wartość** (np. o 20 zł więcej w każdym miesiącu, 2 miejsca więcej w każdym kolejnym rzędzie).
- **Ciąg geometryczny:** stosujemy, gdy wielkość zmienia się **o stały procent** lub **stały czynnik mnożący** (np. podwajanie liczby komórek co godzinę, spadek wartości sprzętu o 15% rocznie, amortyzacja).

### Przykład 1: Model arytmetyczny (Miejsca w amfiteatrze)

W amfiteatrze w pierwszym rzędzie znajduje się $16$ miejsc siedzących, a w każdym kolejnym o $3$ miejsca więcej niż w poprzednim. W amfiteatrze jest $18$ rzędów. Oblicz:

- Ile miejsc znajduje się w ostatnim rzędzie?
- Ile łącznie miejsc jest w całym amfiteatrze?

**Krok 1: Wypisanie danych modelu**

$a_1 = 16$, różnica $r = 3$, liczba rzędów $n = 18$.

**Krok 2: Obliczenie liczby miejsc w 18. rzędzie ($a_{18}$)**

$$a_{18} = a_1 + 17r = 16 + 17 \cdot 3 = 16 + 51 = 67 \text{ miejsc}$$

**Krok 3: Obliczenie łącznej liczby miejsc ($S_{18}$)**

$$S_{18} = \frac{a_1 + a_{18}}{2} \cdot 18 = \frac{16 + 67}{2} \cdot 18 = 83 \cdot 9 = 747 \text{ miejsc}$$

### Przykład 2: Model geometryczny (Spadek wartości sprzętu)

Firma zakupiła maszynę za $50\,000\text{ zł}$. Z powodu eksploatacji wartość maszyny pod koniec każdego kolejnego roku spada o $20\%$ w stosunku do wartości z początku tego roku. Jaka będzie wartość maszyny po $3$ latach?

**Krok 1: Wyznaczenie ilorazu $q$**

Spadek o $20\%$ oznacza, że na koniec każdego roku maszyna zachowuje $100\% - 20\% = 80\% = 0{,}8$ swojej wartości. Zatem $q = 0{,}8$.

**Krok 2: Obliczenie wartości końcowej**

Wartość początkowa to $W_0 = 50\,000\text{ zł}$. Po $3$ latach wartość wyniesie:
$$W_3 = W_0 \cdot q^3 = 50\,000 \cdot (0{,}8)^3 = 50\,000 \cdot 0{,}512 = 25\,600\text{ zł}$$
**Odpowiedź:** Po 3 latach maszyna będzie warta $25\,600\text{ zł}$.

> **Wskazówka egzaminacyjna (Wskazówka językowa):**
> Sformułowanie *„zwiększa się o X”* $\implies$ ciąg arytmetyczny ($r = X$).
>
> Sformułowanie *„zwiększa się o P%”* $\implies$ ciąg geometryczny ($q = 1 + \frac{P}{100}$).
>
> Sformułowanie *„zmniejsza się o P%”* $\implies$ ciąg geometryczny ($q = 1 - \frac{P}{100}$).
