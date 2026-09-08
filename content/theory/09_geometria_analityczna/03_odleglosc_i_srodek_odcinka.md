# 3. Odległość punktów i środek odcinka w układzie współrzędnych

Dwa podstawowe wzory geometrii analitycznej pozwalają obliczyć odległość między dowolnymi dwoma punktami na płaszczyźnie oraz znaleźć punkt leżący dokładnie pośrodku łączącego je odcinka.

> **Definicja: Długość odcinka $|AB|$**
> Dla punktów $A(x_A, y_A)$ i $B(x_B, y_B)$ wzór wynika bezpośrednio z twierdzenia Pitagorasa:
>
> $$|AB| = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}$$

Współrzędne środka odcinka $S$}

Środek odcinka to średnia arytmetyczna współrzędnych jego końców:

$$S = \left(\frac{x_A + x_B}{2}, \frac{y_A + y_B}{2}\right)$$

### Przykład 1: Obliczanie długości odcinka

Oblicz odległość między punktami $A(-3, 2)$ oraz $B(5, -4)$.

**Odpowiedź:**

Podstawiamy współrzędne do wzoru:
$$|AB| = \sqrt{(5 - (-3))^2 + (-4 - 2)^2} = \sqrt{(5 + 3)^2 + (-6)^2}$$
$$|AB| = \sqrt{8^2 + 36} = \sqrt{64 + 36} = \sqrt{100} = 10$$
Odległość wynosi $|AB| = 10$.

### Przykład 2: Wyznaczanie końca odcinka, gdy znany jest środek

Punkt $S(2, -1)$ jest środkiem odcinka $AB$. Jeden z końców tego odcinka to punkt $A(-4, 3)$. Wyznacz współrzędne drugiego końca $B(x_B, y_B)$.

**Krok 1: Wyznaczenie współrzędnej $x_B$**

$$x_S = \frac{x_A + x_B}{2} \implies 2 = \frac{-4 + x_B}{2} \implies 4 = -4 + x_B \implies x_B = 8$$

**Krok 2: Wyznaczenie współrzędnej $y_B$**

$$y_S = \frac{y_A + y_B}{2} \implies -1 = \frac{3 + y_B}{2} \implies -2 = 3 + y_B \implies y_B = -5$$
**Odpowiedź:** Współrzędne punktu to $B(8, -5)$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Różnice współrzędnych są podnoszone do kwadratu: $(x_B - x_A)^2 = (x_A - x_B)^2$. Nie ma więc znaczenia, od którego punktu zaczniesz odejmowanie – wynik pod pierwiastkiem zawsze będzie taki sam i nieujemny!
