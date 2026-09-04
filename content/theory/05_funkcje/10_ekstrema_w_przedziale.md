# 10. Ekstrema funkcji kwadratowej w przedziale

Wyznaczanie **wartości najmniejszej ($y_{\min}$) i największej ($y_{\max}$)** funkcji kwadratowej $f(x) = ax^2 + bx + c$ w przedziale domkniętym $\langle \alpha, \beta \rangle$ wymaga zbadania położenia wierzchołka paraboli $p = -\frac{b}{2a}$ względem tego przedziału.

> **Definicja: Procedura wyznaczania ekstremów w przedziale $\langle \alpha, \beta \rangle$**
> 1. Oblicz pierwszą współrzędną wierzchołka: $p = -\frac{b}{2a}$.
> 2. **Sprawdź, czy $p \in \langle \alpha, \beta \rangle$:**
>
> Jeśli **TAK**: oblicz wartość w wierzchołku $q = f(p)$ oraz wartości na krańcach przedziału $f(\alpha)$ i $f(\beta)$.
> Jeśli **NIE**: oblicz wyłącznie wartości na krańcach przedziału $f(\alpha)$ i $f(\beta)$.
> 3. Spośród obliczonych wartości wybierz liczbę najmniejszą ($y_{\min}$) oraz największą ($y_{\max}$).

### Przykład 1: Wierzchołek należy do przedziału

Wyznacz wartość najmniejszą i największą funkcji $f(x) = x^2 - 4x + 1$ w przedziale $\langle 1, 4 \rangle$.

**Krok 1: Sprawdzenie położenia wierzchołka**

$$p = -\frac{-4}{2 \cdot 1} = 2 \in \langle 1, 4 \rangle$$
Wierzchołek leży wewnątrz badanego przedziału.

**Krok 2: Obliczenie wartości w wierzchołku i na krańcach**

$$f(p) = f(2) = 2^2 - 4(2) + 1 = 4 - 8 + 1 = -3$$
$$f(1) = 1^2 - 4(1) + 1 = 1 - 4 + 1 = -2$$
$$f(4) = 4^2 - 4(4) + 1 = 16 - 16 + 1 = 1$$
Najmniejsza wartość to $-3$, największa to $1$.
**Odpowiedź:** $y_{\min} = -3$ (dla $x = 2$), $y_{\max} = 1$ (dla $x = 4$).

### Przykład 2: Wierzchołek leży poza przedziałem

Wyznacz wartość najmniejszą i największą funkcji $g(x) = -x^2 + 2x + 3$ w przedziale $\langle 3, 5 \rangle$.

**Krok 1: Sprawdzenie położenia wierzchołka**

$$p = -\frac{2}{2(-1)} = 1 \notin \langle 3, 5 \rangle$$
Wierzchołek leży na lewo od przedziału, funkcja jest w tym przedziale monotoniczna (ściśle malejąca).

**Krok 2: Obliczenie wartości na krańcach**

$$g(3) = -(3)^2 + 2(3) + 3 = -9 + 6 + 3 = 0$$
$$g(5) = -(5)^2 + 2(5) + 3 = -25 + 10 + 3 = -12$$
**Odpowiedź:** $y_{\max} = 0$ (dla $x = 3$), $y_{\min} = -12$ (dla $x = 5$).

> **Wskazówka egzaminacyjna:**
> Najczęstszym błędem jest automatyczne uznawanie wartości w wierzchołku za ekstremum bez sprawdzenia, czy $p$ mieści się w zadanym przedziale! Jeśli $p \notin \langle \alpha, \beta \rangle$, ekstremum w wierzchołku w ogóle nie jest osiągane w tym przedziale.
