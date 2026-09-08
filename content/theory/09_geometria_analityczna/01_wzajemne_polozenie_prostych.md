# 1. Wzajemne położenie prostych i punkt przecięcia

Dwie proste na płaszczyźnie kartezjańskiej $k: y = a_1 x + b_1$ oraz $l: y = a_2 x + b_2$ mogą przecinać się w jednym punkcie, być równoległe (brak punktów wspólnych) lub pokrywać się (nieskończenie wiele punktów wspólnych). Szczególnym przypadkiem prostych przecinających się są proste prostopadłe.

> **Definicja: Warunki analityczne położenia prostych**
> - **Proste równoległe ($k \parallel l$):** Mają identyczny współczynnik kierunkowy:
> $$a_1 = a_2 \quad (\text{dla } b_1 \neq b_2 \text{ brak punktów wspólnych; dla } b_1 = b_2 \text{ proste pokrywają się})$$
> - **Proste prostopadłe ($k \perp l$):** Iloczyn ich współczynników kierunkowych wynosi $-1$:
> $$a_1 \cdot a_2 = -1 \iff a_2 = -\frac{1}{a_1}$$
> - **Proste przecinające się:** Warunek $a_1 \neq a_2$. Współrzędne punktu przecięcia $P(x_0, y_0)$ wyznaczamy, rozwiązując układ równań złożony z równań tych prostych.

### Przykład 1: Badanie prostopadłości i równoległości

Określ wzajemne położenie prostej $k: y = \frac{2}{3}x - 4$ oraz prostych $l_1: y = \frac{2}{3}x + 1$ i $l_2: y = -\frac{3}{2}x + 5$.

**Prosta $k$ i prosta $l_1$:**

Współczynniki kierunkowe są równe: $a_k = \frac{2}{3}$ oraz $a_{l1} = \frac{2}{3}$. Ponieważ $b_k \neq b_{l1}$ ($-4 \neq 1$), proste $k$ i $l_1$ są **równoległe** ($k \parallel l_1$).

**Prosta $k$ i prosta $l_2$:**

Sprawdzamy iloczyn współczynników: $a_k \cdot a_{l2} = \frac{2}{3} \cdot \left(-\frac{3}{2}\right) = -1$.

Zatem proste $k$ i $l_2$ są **prostopadłe** ($k \perp l_2$).

### Przykład 2: Wyznaczanie punktu przecięcia dwóch prostych

Wyznacz współrzędne punktu przecięcia prostych $k: y = 2x - 3$ oraz $l: y = -x + 6$.

**Krok 1: Przyrównanie równań stronami**

$$2x - 3 = -x + 6 \implies 3x = 9 \implies x = 3$$

**Krok 2: Wyznaczenie współrzędnej $y$**

Podstawiamy $x = 3$ do dowolnego równania:
$$y = 2 \cdot 3 - 3 = 6 - 3 = 3$$
**Odpowiedź:** Proste przecinają się w punkcie $P(3, 3)$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Współczynnik prostej prostopadłej to tzw. *liczba przeciwna i odwrotna*. Dla $a = \frac{3}{4}$ prostopadła ma $a_\perp = -\frac{4}{3}$; dla $a = -2$ prostopadła ma $a_\perp = \frac{1}{2}$.
