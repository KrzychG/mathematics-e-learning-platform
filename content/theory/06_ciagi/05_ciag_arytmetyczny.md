# 5. Ciąg arytmetyczny – wzór ogólny i suma wyrazów

W ciągu arytmetycznym każdy kolejny wyraz powstaje przez dodanie do poprzedniego stałej liczby $r$ zwanej **różnicą ciągu**. Monotoniczność ciągu arytmetycznego zależy wyłącznie od znaku różnicy: dla $r > 0$ ciąg jest rosnący, dla $r < 0$ malejący, a dla $r = 0$ stały.

> **Definicja: Kluczowe wzory w ciągu arytmetycznym**
> - **Wzór na $n$-ty wyraz:** $$a_n = a_1 + (n - 1) \cdot r$$
> - **Związek między dowolnymi dwoma wyrazami:** $$a_k - a_m = (k - m) \cdot r \implies a_k = a_m + (k - m) \cdot r$$
> - **Suma $n$ początkowych wyrazów:**
> $$S_n = \frac{a_1 + a_n}{2} \cdot n = \frac{2a_1 + (n - 1)r}{2} \cdot n$$

### Przykład 1: Wyznaczanie parametrów ciągu z dwóch wyrazów

W ciągu arytmetycznym $(a_n)$ dane są $a_4 = 11$ oraz $a_9 = 26$. Wyznacz wyraz pierwszy $a_1$, różnicę $r$ oraz wartość wyrazu $a_{20}$.

**Krok 1: Wyznaczenie różnicy $r$ za pomocą relacji $a_9 - a_4$**

$$a_9 - a_4 = (9 - 4) \cdot r \implies 26 - 11 = 5r \implies 15 = 5r \implies r = 3$$

**Krok 2: Obliczenie wyrazu pierwszego $a_1$**

$$a_4 = a_1 + 3r \implies 11 = a_1 + 3 \cdot 3 \implies 11 = a_1 + 9 \implies a_1 = 2$$

**Krok 3: Obliczenie wyrazu $a_{20}$**

$$a_{20} = a_1 + 19r = 2 + 19 \cdot 3 = 2 + 57 = 59$$

### Przykład 2: Obliczanie sumy skończonej liczby wyrazów

Oblicz sumę wszystkich liczb dwucyfrowych podzielnych przez $4$.

**Krok 1: Identyfikacja pierwszego i ostatniego wyrazu oraz różnicy**

Liczby dwucyfrowe podzielne przez $4$ tworzą ciąg arytmetyczny:
$a_1 = 12$ (najmniejsza dwucyfrowa podzielna przez 4),

$r = 4$,

$a_n = 96$ (największa dwucyfrowa podzielna przez 4).

**Krok 2: Wyznaczenie liczby wyrazów $n$**

$$a_n = a_1 + (n - 1)r \implies 96 = 12 + (n - 1) \cdot 4$$
$$84 = 4(n - 1) \implies n - 1 = 21 \implies n = 22$$

**Krok 3: Zastosowanie wzoru na sumę $S_{22}$**

$$S_{22} = \frac{a_1 + a_n}{2} \cdot n = \frac{12 + 96}{2} \cdot 22 = \frac{108}{2} \cdot 22 = 54 \cdot 22 = 1188$$

> **Wskazówka egzaminacyjna (Praktyczna sztuczka egzaminacyjna):**
> Zamiast zawsze wracać do $a_1$ i układać układ równań, korzystaj ze wzoru $a_k - a_m = (k - m) \cdot r$. Na przykład: $a_{10} - a_3 = 7r$. Pozwala to zaoszczędzić cenny czas na egzaminie!
