# 8. Współczynniki funkcji kwadratowej

W **postaci ogólnej** funkcji kwadratowej $f(x) = ax^2 + bx + c$ ($a \neq 0$) każdy ze współczynników $a, b, c$ niesie konkretną informację geometryczną o położeniu i kształcie paraboli w kartezjańskim układzie współrzędnych.

> **Definicja: Interpretacja geometryczna parametrów $a, b, c$ i $\Delta$**
> - **Współczynnik $a$:** decyduje o zwrocie ramion paraboli ($a > 0$ w górę, $a < 0$ w dół) oraz o stopniu ich rozwarcia (im większa wartość $|a|$, tym parabola węższa).
> - **Współczynnik $c$:** punkt przecięcia paraboli z osią $OY$ to punkt $(0, c)$ (ponieważ $f(0) = c$).
> - **Współczynnik $b$:** decyduje wraz z $a$ o położeniu wierzchołka względem osi $OY$: $p = -\frac{b}{2a}$. Jeśli $a$ i $b$ mają ten sam znak, to $p < 0$ (wierzchołek na lewo od osi $OY$); jeśli mają różne znaki, to $p > 0$ (na prawo).
> - **Wyróżnik $\Delta$:** liczba punktów przecięcia z osią $OX$ ($\Delta > 0$: dwa; $\Delta = 0$: jeden styczny; $\Delta < 0$: brak przecięcia).

### Przykład 1: Odczytanie znaków $a, b, c, \Delta$ z wykresu paraboli

Parabola ma wierzchołek w I ćwiartce ($p > 0, q > 0$), jej ramiona skierowane są w dół, a oś $OY$ przecina w punkcie $(0, 2)$. Określ znaki liczb $a, b, c$ oraz $\Delta$.

**Krok 1: Analiza $a$, $c$ i $\Delta$**

Ramiona w dół $\implies a < 0$.
Punkt przecięcia z $OY$ to $(0, 2) \implies c = 2 > 0$.
Wierzchołek leży w I ćwiartce ($q > 0$), a ramiona idą w dół, więc parabola przecina oś $OX$ w dwóch punktach $\implies \Delta > 0$.

**Krok 2: Analiza współczynnika $b$ z pierwszej współrzędnej wierzchołka**

$$p = -\frac{b}{2a} > 0$$
Ponieważ $a < 0$, mianownik $2a < 0$. Zatem aby ułamek $-\frac{b}{2a}$ był dodatni, licznik $-b$ musi być ujemny, czyli $b > 0$.
**Odpowiedź:** $a < 0$, $b > 0$, $c > 0$, $\Delta > 0$.

### Przykład 2: Zastosowanie wzorów Viète'a

Nie obliczając pierwiastków równania $2x^2 - 8x - 5 = 0$, wyznacz ich sumę $x_1 + x_2$ oraz iloczyn $x_1 \cdot x_2$.

**Krok 1: Wzory Viète'a dla $\Delta \ge 0$**

$$x_1 + x_2 = -\frac{b}{a}, \qquad x_1 \cdot x_2 = \frac{c}{a}$$

**Krok 2: Obliczenie wartości**

Dla $a = 2, b = -8, c = -5$:
$$x_1 + x_2 = -\frac{-8}{2} = 4, \qquad x_1 \cdot x_2 = \frac{-5}{2} = -2{,}5$$
**Odpowiedź:** Suma pierwiastków wynosi $4$, a iloczyn $-2{,}5$.

> **Wskazówka egzaminacyjna:**
> Pamiętaj: punkt przecięcia paraboli z osią pionową $OY$ odczytujesz natychmiast z wyrazu wolnego $c$! Nie trzeba nic liczyć – współrzędne tego punktu to zawsze $(0, c)$.
