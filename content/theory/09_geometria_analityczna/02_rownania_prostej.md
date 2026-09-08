# 2. Równania prostej (postać kierunkowa i ogólna)

Prostą na płaszczyźnie kartezjańskiej możemy opisać za pomocą równania w **postaci kierunkowej** lub **postaci ogólnej**. Każda z tych postaci ma swoje unikalne zastosowania w zadaniach geometrycznych.

> **Definicja: Postać kierunkowa: $y = ax + b$**
> - $a = \text{tg}\,\alpha$ – **współczynnik kierunkowy** (dla $a > 0$ prosta rośnie, dla $a = 0$ pozioma, dla $a < 0$ maleje).
> - $b$ – punkt przecięcia z osią $OY$: punkt $(0, b)$.
> - Uwaga: Prosta pionowa ma równanie $x = c$ i nie posiada postaci kierunkowej.

Postać ogólna: $Ax + By + C = 0$

- Opisuje **każdą** prostą na płaszczyźnie (w tym proste pionowe dla $B = 0$).
- Przekształcenie do postaci kierunkowej (gdy $B \neq 0$):
$$y = -\frac{A}{B}x - \frac{C}{B} \implies a = -\frac{A}{B}$$

Wzór na prostą przechodzącą przez dwa punkty $A(x_A, y_A)$ i $B(x_B, y_B)$:

$$a = \frac{y_B - y_A}{x_B - x_A}, \qquad y - y_A = a(x - x_A)$$

### Przykład 1: Równanie prostej przechodzącej przez dwa punkty

Wyznacz równanie prostej przechodzącej przez punkty $A(-2, 1)$ oraz $B(4, 4)$.

**Krok 1: Obliczenie współczynnika kierunkowego $a$**

$$a = \frac{y_B - y_A}{x_B - x_A} = \frac{4 - 1}{4 - (-2)} = \frac{3}{6} = \frac{1}{2}$$

**Krok 2: Wyznaczenie współczynnika $b$**

Podstawiamy współrzędne punktu $B(4, 4)$ do równania $y = \frac{1}{2}x + b$:
$$4 = \frac{1}{2} \cdot 4 + b \implies 4 = 2 + b \implies b = 2$$
**Odpowiedź:** Prosta ma równanie kierunkowe $y = \frac{1}{2}x + 2$ (lub ogólne $x - 2y + 4 = 0$).

### Przykład 2: Prosta prostopadła przechodząca przez punkt

Wyznacz równanie prostej $k$ prostopadłej do prostej $l: y = -3x + 7$ i przechodzącej przez punkt $P(6, -1)$.

**Krok 1: Wyznaczenie współczynnika prostej prostopadłej**

$$a_k = -\frac{1}{a_l} = -\frac{1}{-3} = \frac{1}{3}$$

**Krok 2: Podstawienie punktu $P(6, -1)$**

$$y = \frac{1}{3}x + b \implies -1 = \frac{1}{3} \cdot 6 + b \implies -1 = 2 + b \implies b = -3$$
**Odpowiedź:** Równanie szukanej prostej to $y = \frac{1}{3}x - 3$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Gdy równanie prostej podane jest w postaci ogólnej (np. $2x + 4y - 5 = 0$), najpierw wyznacz z niego $y$ ($4y = -2x + 5 \implies y = -\frac{1}{2}x + \frac{5}{4}$). Wtedy współczynnik kierunkowy $a = -\frac{1}{2}$ jest od razu widoczny!
