# 9. Wyznaczanie wzoru funkcji kwadratowej

W zależności od posiadanych informacji o funkcji kwadratowej (miejsca zerowe, współrzędne wierzchołka czy dowolne trzy punkty wykresu), dobieramy najwygodniejszą postać: **iloczynową**, **kanoniczną** lub **ogólną**.

> **Definicja: Trzy postacie funkcji kwadratowej**
> - **Gdy znamy miejsca zerowe $x_1, x_2$:** postać iloczynowa:
>
> $$f(x) = a(x - x_1)(x - x_2)$$
> - **Gdy znamy wierzchołek $W(p, q)$:** postać kanoniczna:
>
> $$f(x) = a(x - p)^2 + q$$
> - **Gdy znamy dowolne 3 punkty:** postać ogólna $f(x) = ax^2 + bx + c$ i układ 3 równań.

### Przykład 1: Wyznaczanie wzoru z wierzchołka i punktu

Wyznacz wzór ogólny funkcji kwadratowej, której wierzchołkiem jest punkt $W(2, -3)$, a wykres przechodzi przez punkt $A(0, 5)$.

**Krok 1: Zapisanie postaci kanonicznej dla $W(2, -3)$**

$$f(x) = a(x - 2)^2 - 3$$

**Krok 2: Wyznaczenie współczynnika $a$ z punktu $A(0, 5)$ i postać ogólna**

$$5 = a(0 - 2)^2 - 3 \implies 5 = 4a - 3 \implies 4a = 8 \implies a = 2$$
Rozwijamy do postaci ogólnej:
$$f(x) = 2(x^2 - 4x + 4) - 3 = 2x^2 - 8x + 8 - 3 = 2x^2 - 8x + 5$$
**Odpowiedź:** Wzór ogólny to $f(x) = 2x^2 - 8x + 5$.

### Przykład 2: Wyznaczanie wzoru z miejsc zerowych

Miejscami zerowymi funkcji kwadratowej są liczby $-1$ oraz $5$, a jej największa wartość wynosi $18$. Wyznacz wzór tej funkcji.

**Krok 1: Postać iloczynowa i pierwsza współrzędna wierzchołka $p$**

$$f(x) = a(x + 1)(x - 5)$$
Wierzchołek leży dokładnie w połowie między miejscami zerowymi:
$$p = \frac{x_1 + x_2}{2} = \frac{-1 + 5}{2} = 2$$

**Krok 2: Wyznaczenie $a$ z warunku największej wartości $q = 18$ w wierzchołku**

$$f(2) = 18 \implies a(2 + 1)(2 - 5) = 18 \implies a(3)(-3) = 18 \implies -9a = 18 \implies a = -2$$
$$f(x) = -2(x + 1)(x - 5) = -2(x^2 - 4x - 5) = -2x^2 + 8x + 10$$
**Odpowiedź:** $f(x) = -2x^2 + 8x + 10$.

> **Wskazówka egzaminacyjna:**
> Wykorzystuj symetrię paraboli! Pierwsza współrzędna wierzchołka to ZAWSZE średnia arytmetyczna miejsc zerowych: $p = \frac{x_1 + x_2}{2}$. Ta własność pozwala zaoszczędzić mnóstwo czasu w zadaniach zamkniętych i otwartych.
