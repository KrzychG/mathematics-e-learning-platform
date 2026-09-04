# 4. Sprawdzanie rodzaju ciągu (arytmetyczny czy geometryczny)

Dwa fundamentalne typy ciągów w matematyce szkolnej to **ciąg arytmetyczny** oraz **ciąg geometryczny**. Rozpoznajemy je badając stałość odpowiednio *różnicy* lub *ilorazu* kolejnych wyrazów.

> **Definicja: Ciąg arytmetyczny**
> Różnica każdych dwóch kolejnych wyrazów jest **stała** i niezależna od $n$:
>
> $$a_{n+1} - a_n = r = \text{const}$$
>
> **Własność 3 kolejnych wyrazów $(x, y, z)$:**
> $$y = \frac{x + z}{2} \iff 2y = x + z$$

Ciąg geometryczny

Iloraz każdego wyrazu (dla $n \ge 2$) przez wyraz poprzedni jest **stały** ($a_n \neq 0$):

$$\frac{a_{n+1}}{a_n} = q = \text{const}$$

**Własność 3 kolejnych wyrazów $(x, y, z)$:**
$$y^2 = x \cdot z$$

### Przykład 1: Weryfikacja ze wzoru ogólnego

Sprawdź, czy ciągi $(a_n)$ i $(b_n)$ są arytmetyczne lub geometryczne:

**a) Ciąg $a_n = 5n - 2$:**

$$a_{n+1} - a_n = [5(n + 1) - 2] - [5n - 2] = 5n + 5 - 2 - 5n + 2 = 5$$
Różnica wynosi stale $5$ (liczba niezależna od $n$). Zatem ciąg $(a_n)$ jest **arytmetyczny** o różnicy $r = 5$.

**b) Ciąg $b_n = 4 \cdot 3^n$:**

$$\frac{b_{n+1}}{b_n} = \frac{4 \cdot 3^{n+1}}{4 \cdot 3^n} = \frac{4 \cdot 3^n \cdot 3}{4 \cdot 3^n} = 3$$
Iloraz wynosi stale $3$ (liczba niezależna od $n$). Zatem ciąg $(b_n)$ jest **geometryczny** o ilorazie $q = 3$.

### Przykład 2: Zastosowanie własności trzech kolejnych wyrazów

Dla jakiej wartości parametru $x$ liczby $x + 1$, $2x - 3$, $4x - 5$ tworzą w podanej kolejności ciąg arytmetyczny?

**Krok 1: Zastosowanie warunku $2y = x + z$**

$$2(2x - 3) = (x + 1) + (4x - 5)$$

**Krok 2: Rozwiązanie równania liniowego**

$$4x - 6 = 5x - 4 \implies -x = 2 \implies x = -2$$
**Odpowiedź:** Dla $x = -2$ liczby te wynoszą odpowiednio: $-1, -7, -13$ i tworzą ciąg arytmetyczny o różnicy $r = -6$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Wzór ogólny ciągu arytmetycznego jest zawsze funkcją **liniową** zmiennej $n$ ($a_n = An + B$, gdzie współczynnik $A$ to różnica $r$). Wzór ciągu geometrycznego to zawsze funkcja **wykładnicza** ($b_n = c \cdot q^n$).
