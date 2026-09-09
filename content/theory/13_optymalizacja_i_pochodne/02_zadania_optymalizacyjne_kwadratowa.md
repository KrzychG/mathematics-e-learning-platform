# 2. Zagadnienia optymalizacyjne z funkcją kwadratową

Kluczem do rozwiązania zadania optymalizacyjnego w zakresie podstawowym jest wykorzystanie własności wierzchołka paraboli $W(p, q)$.

> **Definicja: Ekstremum funkcji kwadratowej $f(x) = ax^2 + bx + c$**
> - **Wartość największa (maksimum dla $a < 0$):** Ramiona paraboli są skierowane w dół. Funkcja przyjmuje wartość największą w wierzchołku:
> $$x_{\text{opt}} = p = -\frac{b}{2a}, \qquad y_{\text{max}} = q = f(p) = -\frac{\Delta}{4a}$$
> - **Wartość najmniejsza (minimum dla $a > 0$):** Ramiona paraboli są skierowane w górę. Funkcja przyjmuje wartość najmniejszą w wierzchołku:
> $$x_{\text{opt}} = p = -\frac{b}{2a}, \qquad y_{\text{min}} = q = f(p)$$
> - **Weryfikacja:** Zawsze należy sprawdzić, czy wyznaczony punkt $p$ należy do dziedziny $D_f$ ($p \in D_f$).

### Przykład 1: Maksymalne pole wybiegu przy rzece

Dla wybiegu o polu $P(x) = -2x^2 + 120x$ określonego dla $x \in (0, 60)$ wyznacz wymiary prostokąta, dla których pole jest największe, oraz oblicz to maksymalne pole.

**Krok 1: Identyfikacja współczynników funkcji kwadratowej**

Współczynniki to: $a = -2$, $b = 120$, $c = 0$.
Ponieważ $a = -2 < 0$, parabola ma ramiona skierowane w dół, a funkcja osiąga wartość **największą** w wierzchołku.

**Krok 2: Obliczenie współrzędnej $p$ wierzchołka**

$$p = -\frac{b}{2a} = -\frac{120}{2 \cdot (-2)} = -\frac{120}{-4} = 30$$
Punkt $p = 30 \in (0, 60)$ należy do dziedziny geometrycznej.

**Krok 3: Wyznaczenie drugiego boku $y$ oraz maksymalnego pola**

Bok prostopadły: $x = 30\text{ m}$.
Bok równoległy do rzeki: $y = 120 - 2x = 120 - 2 \cdot 30 = 60\text{ m}$.

Pole maksymalne:
$$P_{\text{max}} = P(30) = 30 \cdot 60 = 1800\text{ m}^2$$
**Odpowiedź:** Największe pole wynosi $1800\text{ m}^2$ dla wybiegu o wymiarach $30\text{ m} \times 60\text{ m}$.

### Przykład 2: Minimalizacja sumy kwadratów dwóch liczb

Przedstaw liczbę $20$ w postaci sumy dwóch liczb dodatnich tak, aby suma ich kwadratów była jak najmniejsza.

**Krok 1: Budowa funkcji**

Niech szukane liczby to $x$ oraz $20 - x$, gdzie $x \in (0, 20)$.
Suma ich kwadratów wynosi:
$$S(x) = x^2 + (20 - x)^2 = x^2 + 400 - 40x + x^2 = 2x^2 - 40x + 400$$

**Krok 2: Wyznaczenie minimum funkcji**

Współczynnik $a = 2 > 0$ (ramiona w górę $\implies$ minimum w wierzchołku):
$$x_{\text{min}} = p = -\frac{b}{2a} = -\frac{-40}{2 \cdot 2} = \frac{40}{4} = 10 \in (0, 20)$$
Druga liczba to $20 - x = 20 - 10 = 10$.
**Odpowiedź:** Szukane liczby to $10$ i $10$.

> **Wskazówka egzaminacyjna (Uważnie czytaj polecenie):**
> Sprawdź, o co pyta autor zadania: czy o **argument** (np. wymiary działki, cenę biletu $p$), czy o samą **wartość optymalną** (np. maksymalne pole, maksymalny dochód $q$).
