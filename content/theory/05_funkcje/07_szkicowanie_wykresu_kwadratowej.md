# 7. Szkicowanie wykresu funkcji kwadratowej

Wykresem funkcji kwadratowej $f(x) = ax^2 + bx + c$ ($a \neq 0$) jest **parabola**. Kluczową rolę w szkicowaniu paraboli odgrywa **postać kanoniczna** $f(x) = a(x - p)^2 + q$, z której bezpośrednio odczytujemy współrzędne jej wierzchołka $W(p, q)$.

> **Definicja: Postać kanoniczna i współrzędne wierzchołka**
> $$f(x) = a(x - p)^2 + q, \qquad W = (p, q) = \left(-\frac{b}{2a}, -\frac{\Delta}{4a}\right)$$
>
> - **Oś symetrii paraboli:** pionowa prosta o równaniu $x = p$.
> - **Kierunek ramion:** $a > 0$ – ramiona w górę ($ZW = \langle q, +\infty)$); $a < 0$ – ramiona w dół ($ZW = (-\infty, q\rangle$).
> - Wierzchołek realizuje wartość ekstremalną: najmniejszą dla $a > 0$ ($y_{\min} = q$) lub największą dla $a < 0$ ($y_{\max} = q$).

### Przykład 1: Przekształcenie do postaci kanonicznej

Sprowadź funkcję $f(x) = x^2 - 6x + 5$ do postaci kanonicznej i wyznacz współrzędne wierzchołka.

**Krok 1: Obliczenie współrzędnych $p$ i $q$**

$$a = 1, \quad b = -6, \quad c = 5$$
$$p = -\frac{b}{2a} = -\frac{-6}{2 \cdot 1} = 3$$
$$q = f(p) = f(3) = 3^2 - 6(3) + 5 = 9 - 18 + 5 = -4$$

**Krok 2: Zapisanie postaci kanonicznej**

$$f(x) = 1 \cdot (x - 3)^2 + (-4) = (x - 3)^2 - 4$$
Wierzchołek: $W = (3, -4)$.

### Przykład 2: Odczytanie własności z postaci kanonicznej

Dana jest funkcja $g(x) = -2(x + 1)^2 + 8$. Podaj zbiór wartości oraz maksymalne przedziały monotoniczności.

**Krok 1: Odczytanie wierzchołka i kierunku ramion**

Postać $a(x - p)^2 + q$: $a = -2 < 0$, $p = -1$, $q = 8$. Wierzchołek $W(-1, 8)$.
Ramiona paraboli skierowane są **w dół**.

**Krok 2: Zbiór wartości i monotoniczność**

$$ZW_g = (-\infty, 8\rangle$$
Funkcja rośnie w przedziale $(-\infty, -1\rangle$, a maleje w przedziale $\langle -1, +\infty)$.

> **Wskazówka egzaminacyjna:**
> Uważaj na znak we wzorze kanonicznym: $a(x - p)^2 + q$. Jeśli we wzorze występuje $(x + 3)^2$, to $p = -3$! Jeśli $(x - 4)^2$, to $p = 4$. Drugą współrzędną $q$ najszybciej obliczyć licząc wartość funkcji dla $p$: $q = f(p)$.
