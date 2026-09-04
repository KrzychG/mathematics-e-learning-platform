# 2. Obliczanie wartości funkcji ze wzoru

Mając dany wzór analityczny funkcji $y = f(x)$, obliczenie **wartości funkcji** dla zadanego argumentu $x_0$ polega na podstawieniu $x_0$ w miejsce zmiennej $x$ we wzorze. Z kolei wyznaczenie argumentu dla zadanej wartości $y_0$ sprowadza się do rozwiązania równania $f(x) = y_0$.

> **Definicja: Pojęcia kluczowe**
> - **Wartość funkcji dla argumentu $x_0$:** wynik $f(x_0)$ po podstawieniu $x_0$ do wzoru.
> - **Miejsce zerowe funkcji:** taki argument $x \in D$, dla którego wartość funkcji wynosi zero ($f(x) = 0$). Na wykresie jest to pierwsza współrzędna punktu przecięcia z osią $OX$: $(x, 0)$.
> - **Punkt przecięcia z osią $OY$:** punkt o współrzędnych $(0, f(0))$ (jeśli $0 \in D$).

### Przykład 1: Obliczanie wartości dla argumentu z pierwiastkiem

Dana jest funkcja $f(x) = 2x^2 - 3x + 1$. Oblicz wartość funkcji dla argumentu $x = \sqrt{3} - 1$.

**Krok 1: Podstawienie i zastosowanie wzoru skróconego mnożenia**

$$f(\sqrt{3} - 1) = 2(\sqrt{3} - 1)^2 - 3(\sqrt{3} - 1) + 1$$
$$(\sqrt{3} - 1)^2 = (\sqrt{3})^2 - 2\sqrt{3} + 1 = 3 - 2\sqrt{3} + 1 = 4 - 2\sqrt{3}$$

**Krok 2: Uproszczenie wyrażenia**

$$f(\sqrt{3} - 1) = 2(4 - 2\sqrt{3}) - 3\sqrt{3} + 3 + 1 = 8 - 4\sqrt{3} - 3\sqrt{3} + 4 = 12 - 7\sqrt{3}$$
**Odpowiedź:** Wartość wynosi $12 - 7\sqrt{3}$.

### Przykład 2: Wyznaczenie argumentu dla danej wartości

Dla jakiego argumentu funkcja $g(x) = \frac{3x - 5}{x + 2}$ przyjmuje wartość równą $2$?

**Krok 1: Dziedzina i ułożenie równania**

Dziedzina: $x + 2 \neq 0 \implies x \neq -2$, czyli $D = \mathbb{R} \setminus \{-2\}$.
$$g(x) = 2 \implies \frac{3x - 5}{x + 2} = 2$$

**Krok 2: Rozwiązanie równania**

$$3x - 5 = 2(x + 2) \implies 3x - 5 = 2x + 4 \implies 3x - 2x = 4 + 5 \implies x = 9$$
Ponieważ $9 \in D$, jest to rozwiązanie poprawne.
**Odpowiedź:** Funkcja przyjmuje wartość $2$ dla argumentu $x = 9$.

> **Wskazówka egzaminacyjna:**
> Rozróżniaj dwa polecenia: „Oblicz wartość funkcji dla argumentu $3$” (liczysz $f(3)$) oraz „Dla jakiego argumentu funkcja przyjmuje wartość $3$” (rozwiązujesz równanie $f(x) = 3$). Pomyłka w interpretacji to częsty błąd!
