# 1. Pojęcie ciągu liczbowego i wzór ogólny

**Ciąg liczbowy** to funkcja, której dziedziną jest zbiór liczb naturalnych dodatnich $\mathbb{N}_+ = \{1, 2, 3, \dots\}$. Wartości tej funkcji dla kolejnych liczb naturalnych $n$ nazywamy **wyrazami ciągu** i oznaczamy symbolem $a_n$ (gdzie $a_1$ to wyraz pierwszy, $a_2$ – drugi, a $a_n$ – wyraz o numerze $n$, zwany wyrazem ogólnym).

> **Definicja: Wzór ogólny ciągu**
> Wzór ogólny $a_n = f(n)$ pozwala bezpośrednio wyznaczyć dowolny wyraz ciągu przez podstawienie w miejsce zmiennej $n$ numeru szukanego wyrazu ($n \in \mathbb{N}_+$).
>
> $$a_n = f(n), \quad \text{dla } n \in \{1, 2, 3, \dots\}$$

### Przykład 1: Obliczanie wyrazów ciągu

Dany jest ciąg o wyrazie ogólnym $a_n = \frac{3n - 1}{n + 2}$. Wyznacz wartości wyrazów $a_1$, $a_2$ oraz $a_4$.

**Dla $n = 1$:**

$$a_1 = \frac{3 \cdot 1 - 1}{1 + 2} = \frac{2}{3}$$

**Dla $n = 2$:**

$$a_2 = \frac{3 \cdot 2 - 1}{2 + 2} = \frac{5}{4}$$

**Dla $n = 4$:**

$$a_4 = \frac{3 \cdot 4 - 1}{4 + 2} = \frac{11}{6}$$

### Przykład 2: Sprawdzanie, czy liczba jest wyrazem ciągu

Czy liczba $11$ jest wyrazem ciągu określonego wzorem $a_n = n^2 - 2n - 4$?

**Krok 1: Przyrównanie wyrazu ogólnego do szukanej wartości**

$$n^2 - 2n - 4 = 11 \implies n^2 - 2n - 15 = 0$$

**Krok 2: Rozwiązanie równania kwadratowego**

$$\Delta = (-2)^2 - 4 \cdot 1 \cdot (-15) = 4 + 60 = 64, \quad \sqrt{\Delta} = 8$$
$$n_1 = \frac{2 - 8}{2} = -3, \qquad n_2 = \frac{2 + 8}{2} = 5$$

**Krok 3: Weryfikacja z dziedziną $n \in \mathbb{N}_+$**

Liczba $-3 \notin \mathbb{N}_+$, natomiast $5 \in \mathbb{N}_+$. Zatem $a_5 = 11$.
**Odpowiedź:** Tak, liczba $11$ jest piątym wyrazem tego ciągu.

> **Wskazówka egzaminacyjna:**
> Indeks $n$ w ciągach musi być **liczbą naturalną dodatnią** ($n \in \{1, 2, 3, \dots\}$). Jeśli rozwiązując równanie $a_n = k$ otrzymasz wynik ujemny lub ułamek (np. $n = 2{,}5$ lub $n = -4$), oznacza to, że dana liczba **nie występuje** w tym ciągu.
