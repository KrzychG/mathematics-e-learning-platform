# 11. Zastosowania geometryczne i fizyczne

Funkcja kwadratowa jest podstawowym modelem matematycznym w fizyce (ruch jednostajnie przyspieszony, rzut pionowy i ukośny) oraz w geometrii (pola figur, maksymalizacja powierzchni przy ograniczonym obwodzie). Wierzchołek paraboli odpowiada wtedy stanowi optymalnemu (maksymalna wysokość, maksymalne pole).

> **Definicja: Równanie ruchu jednostajnie przyspieszonego**
> $$h(t) = h_0 + v_0 t - \frac{g t^2}{2}$$
>
> - Współczynnik przy $t^2$ wynosi $a = -\frac{g}{2} < 0$, co oznacza, że parabola ma ramiona skierowane w dół.
> - Czas osiągnięcia maksymalnej wysokości to $t_{\max} = p = -\frac{v_0}{2a} = \frac{v_0}{g}$.
> - Maksymalna wysokość to $h_{\max} = q = h(t_{\max})$.

### Przykład 1: Rzut pionowy w górę

Piłka rzucona pionowo w górę osiąga po $t$ sekundach wysokość opisaną wzorem $h(t) = 20t - 5t^2$ (dla $t \ge 0$, gdzie $h$ wyrażone jest w metrach). Po jakim czasie piłka osiągnie maksymalną wysokość i ile ta wysokość wynosi?

**Krok 1: Wyznaczenie współrzędnej $p$ (czas maksymalnej wysokości)**

Dla funkcji $h(t) = -5t^2 + 20t$: $a = -5, b = 20, c = 0$.
$$t_{\max} = p = -\frac{b}{2a} = -\frac{20}{2(-5)} = \frac{20}{10} = 2 \text{ s}$$

**Krok 2: Obliczenie maksymalnej wysokości $h_{\max} = q$**

$$h_{\max} = h(2) = 20(2) - 5(2)^2 = 40 - 20 = 20 \text{ m}$$
**Odpowiedź:** Piłka osiągnie maksymalną wysokość po $2$ sekundach i wyniesie ona $20$ metrów.

### Przykład 2: Maksymalne pole wybiegu przy rzece

Rolnik dysponuje siatką o długości $120$ m. Chce ogrodzić prostokątny wybieg przylegający jednym bokiem do prostoliniowego brzegu rzeki (brzegu nie grodzimy). Jakie wymiary powinien mieć wybieg, aby jego pole było jak największe?

**Krok 1: Wyprowadzenie funkcji pola**

Niech $x$ – długość boków prostopadłych do rzeki ($x > 0$), $y$ – długość boku równoległego do rzeki.
Suma długości płotu: $2x + y = 120 \implies y = 120 - 2x$.

Pole wybiegu: $P(x) = x \cdot y = x(120 - 2x) = -2x^2 + 120x$. Dziedzina: $x \in (0, 60)$.

**Krok 2: Wyznaczenie maksimum**

Współczynnik $a = -2 < 0$, więc pole osiąga maksimum w wierzchołku:
$$x_{\max} = -\frac{120}{2(-2)} = 30 \text{ m}$$
$$y = 120 - 2(30) = 60 \text{ m}$$
$$P_{\max} = 30 \cdot 60 = 1800 \text{ m}^2$$
**Odpowiedź:** Wymiary wybiegu to $30$ m na $60$ m, a maksymalne pole to $1800$ m$^2$.

> **Wskazówka egzaminacyjna:**
> Pamiętaj o wyznaczeniu dziedziny geometrycznej/fizycznej (np. boki muszą być dodatnie: $x > 0$ oraz $120 - 2x > 0 \implies x \in (0, 60)$). Na egzaminie brak określenia dziedziny w zadaniu optymalizacyjnym kosztuje 1 punkt!
