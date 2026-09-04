# 6. Wyznaczanie wzoru funkcji liniowej

Wzór funkcji liniowej $y = ax + b$ można jednoznacznie wyznaczyć, znając współrzędne **dwóch różnych punktów** należących do jej wykresu lub znając współczynnik kierunkowy oraz jeden punkt (np. z warunku równoległości lub prostopadłości do innej prostej).

> **Definicja: Warunki równoległości i prostopadłości prostych**
> Niech prosta $k: y = a_1 x + b_1$ oraz prosta $l: y = a_2 x + b_2$:
>
> $$k \parallel l \iff a_1 = a_2 \qquad (\text{proste równoległe – ten sam współczynnik})$$
> $$k \perp l \iff a_1 \cdot a_2 = -1 \iff a_2 = -\frac{1}{a_1} \quad (\text{proste prostopadłe})$$

### Przykład 1: Prosta przechodząca przez dwa punkty

Wyznacz wzór funkcji liniowej przechodzącej przez punkty $A(2, -1)$ oraz $B(-4, 8)$.

**Krok 1: Obliczenie współczynnika kierunkowego $a$**

$$a = \frac{y_B - y_A}{x_B - x_A} = \frac{8 - (-1)}{-4 - 2} = \frac{9}{-6} = -\frac{3}{2} = -1{,}5$$

**Krok 2: Wyznaczenie wyrazu wolnego $b$ z punktu $A(2, -1)$**

$$y = -\frac{3}{2}x + b \implies -1 = -\frac{3}{2}(2) + b \implies -1 = -3 + b \implies b = 2$$
**Odpowiedź:** Wzór funkcji to $y = -\frac{3}{2}x + 2$ (lub $f(x) = -1{,}5x + 2$).

### Przykład 2: Prosta prostopadła przechodząca przez dany punkt

Wyznacz równanie prostej prostopadłej do prostej $y = 2x - 7$, przechodzącej przez punkt $P(4, 1)$.

**Krok 1: Wyznaczenie współczynnika prostej prostopadłej**

$$a_1 = 2 \implies a_2 = -\frac{1}{a_1} = -\frac{1}{2}$$

**Krok 2: Podstawienie punktu $P(4, 1)$**

$$y = -\frac{1}{2}x + b \implies 1 = -\frac{1}{2}(4) + b \implies 1 = -2 + b \implies b = 3$$
**Odpowiedź:** Szukana prosta ma równanie $y = -\frac{1}{2}x + 3$.

> **Wskazówka egzaminacyjna:**
> Warunek prostopadłości $a_1 \cdot a_2 = -1$ to liczba przeciwna i odwrotna! Dla $a_1 = 2$ współczynnik wynosi $-\frac{1}{2}$; dla $a_1 = -\frac{3}{4}$ wynosi $\frac{4}{3}$. Sprawdź zawsze iloczyn: $a_1 \cdot a_2$ musi wynosić $-1$.
