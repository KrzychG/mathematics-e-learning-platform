# 14. Funkcja wykładnicza i logarytmiczna

**Funkcją wykładniczą** nazywamy funkcję $f(x) = a^x$ dla $a > 0$ i $a \neq 1$. Jej funkcją odwrotną jest **funkcja logarytmiczna** $g(x) = \log_a x$. Wykresy tych dwóch funkcji są symetryczne względem prostej $y = x$.

> **Definicja: Zestawienie własności obu funkcji**
> Funkcja wykładnicza $f(x) = a^x$:
>
> - Dziedzina: $D = \mathbb{R}$
> - Zbiór wartości: $ZW = (0, +\infty)$
> - Punkt wspólny każdego wykresu: $(0, 1)$
> - Asymptota pozioma: oś $OX$ ($y = 0$)
> - Rosnąca dla $a > 1$, malejąca dla $0 < a < 1$
>
> Funkcja logarytmiczna $g(x) = \log_a x$:
>
> - Dziedzina: $D = (0, +\infty)$ (warunek $x > 0$!)
> - Zbiór wartości: $ZW = \mathbb{R}$
> - Miejsce zerowe: $(1, 0)$ (bo $\log_a 1 = 0$)
> - Asymptota pionowa: oś $OY$ ($x = 0$)
> - Rosnąca dla $a > 1$, malejąca dla $0 < a < 1$

### Przykład 1: Wyznaczanie podstawy $a$ z punktu wykresu

Do wykresu funkcji wykładniczej $f(x) = a^x$ należy punkt $P\left(-2, \frac{1}{9}\right)$. Wyznacz $a$ oraz oblicz wartość $f(3)$.

**Krok 1: Wyznaczenie podstawy $a$**

$$a^{-2} = \frac{1}{9} \implies \frac{1}{a^2} = \frac{1}{9} \implies a^2 = 9$$
Ponieważ z definicji $a > 0$, to $a = 3$. Wzór funkcji to $f(x) = 3^x$.

**Krok 2: Obliczenie wartości dla $x = 3$**

$$f(3) = 3^3 = 27$$
**Odpowiedź:** Podstawa wynosi $a = 3$, a wartość $f(3) = 27$.

### Przykład 2: Dziedzina złożonej funkcji logarytmicznej

Wyznacz dziedzinę funkcji $h(x) = \log_2(6 - 2x)$.

**Krok 1: Warunek liczby logarytmowanej ($> 0$)**

Liczba logarytmowana musi być ściśle dodatnia:
$$6 - 2x > 0$$

**Krok 2: Rozwiązanie nierówności**

$$-2x > -6 \implies x < \frac{-6}{-2} \implies x < 3$$
**Odpowiedź:** Dziedziną funkcji jest przedział $D = (-\infty, 3)$.

> **Wskazówka egzaminacyjna:**
> Pamiętaj o asymetrii dziedziny i zbioru wartości między funkcją wykładniczą a logarytmiczną! W funkcji wykładniczej $y = a^x$ wynik jest ZAWSZE ściśle dodatni ($a^x > 0$). W funkcji logarytmicznej $y = \log_a x$ to argument pod logarytmem musi być ściśle dodatni ($x > 0$).
