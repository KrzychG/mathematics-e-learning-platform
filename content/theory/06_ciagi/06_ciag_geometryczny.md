# 6. Ciąg geometryczny – wzór ogólny i suma wyrazów

W ciągu geometrycznym każdy kolejny wyraz powstaje przez pomnożenie wyrazu poprzedniego przez stałą liczbę $q \neq 0$, zwaną **ilorazem ciągu**. Jeśli $q < 0$, wyrazy ciągu mają naprzemienne znaki (ciąg oscyluje wokół zera i nie jest monotoniczny).

> **Definicja: Kluczowe wzory w ciągu geometrycznym**
> - **Wzór na $n$-ty wyraz:** $$a_n = a_1 \cdot q^{n - 1}$$
> - **Relacja między dowolnymi dwoma wyrazami:** $$a_k = a_m \cdot q^{k - m} \implies q^{k - m} = \frac{a_k}{a_m}$$
> - **Suma $n$ początkowych wyrazów:**
> $$S_n = a_1 \cdot \frac{1 - q^n}{1 - q} = a_1 \cdot \frac{q^n - 1}{q - 1} \quad (\text{dla } q \neq 1)$$
> (Dla $q = 1$ ciąg jest stały i suma wynosi $S_n = n \cdot a_1$)

### Przykład 1: Wyznaczanie parametrów ciągu z dwóch wyrazów

W ciągu geometrycznym o wyrazach dodatnich dane są $a_2 = 6$ oraz $a_5 = 48$. Wyznacz wyraz pierwszy $a_1$, iloraz $q$ oraz wartość $a_8$.

**Krok 1: Wyznaczenie ilorazu $q$**

$$a_5 = a_2 \cdot q^{5 - 2} \implies 48 = 6 \cdot q^3 \implies q^3 = \frac{48}{6} = 8 \implies q = 2$$

**Krok 2: Obliczenie wyrazu pierwszego $a_1$**

$$a_2 = a_1 \cdot q \implies 6 = a_1 \cdot 2 \implies a_1 = 3$$

**Krok 3: Wyznaczenie wyrazu $a_8$**

$$a_8 = a_1 \cdot q^7 = 3 \cdot 2^7 = 3 \cdot 128 = 384$$

### Przykład 2: Suma wyrazów o ujemnym ilorazie

Oblicz sumę sześciu początkowych wyrazów ciągu geometrycznego, w którym $a_1 = 3$ oraz $q = -2$.

**Krok 1: Podstawienie danych do wzoru na sumę $S_6$**

$$S_6 = a_1 \cdot \frac{1 - q^6}{1 - q} = 3 \cdot \frac{1 - (-2)^6}{1 - (-2)}$$

**Krok 2: Uważne wykonanie potęgowania z uwzględnieniem znaku**

$$(-2)^6 = 64 \implies S_6 = 3 \cdot \frac{1 - 64}{1 + 2} = 3 \cdot \frac{-63}{3} = -63$$
**Odpowiedź:** Suma wynosi $S_6 = -63$.

> **Wskazówka egzaminacyjna (Uwaga na nawiasy):**
> Podnosząc ujemny iloraz do potęgi, **bezwzględnie stosuj nawias**: $(-2)^4 = 16$, podczas gdy zapis bez nawiasu $-2^4 = -16$. Znak potęgi w mianowniku i liczniku wzoru na sumę to najczęstsze źródło błędów na egzaminie!
