# 4. Równania wielomianowe

**Równaniem wielomianowym** nazywamy równanie postaci $W(x) = 0$, gdzie $W(x)$ jest wielomianem stopnia co najmniej $3$. Na poziomie podstawowym równania wielomianowe rozwiązujemy metodą **faktoryzacji** (rozkładu na czynniki), wykorzystując zasadę iloczynu zerowego.

> **Definicja: Zasada iloczynu zerowego**
> Iloczyn wyrażeń jest równy zero wtedy i tylko wtedy, gdy co najmniej jeden z czynników jest równy zero:
>
> $$A(x) \cdot B(x) \cdot C(x) = 0 \iff A(x) = 0 \quad \lor \quad B(x) = 0 \quad \lor \quad C(x) = 0$$

### Przykład 1: Równanie w postaci iloczynowej

Rozwiąż równanie: $(x^2 - 4)(2x + 6)(x^2 + 9) = 0$.

**Krok 1: Przyrównanie każdego nawiasu do zera**

$$x^2 - 4 = 0 \implies x = 2 \quad \lor \quad x = -2$$
$$2x + 6 = 0 \implies 2x = -6 \implies x = -3$$
$$x^2 + 9 = 0 \implies x^2 = -9 \implies \text{brak rozwiązań w } \mathbb{R}$$

**Krok 2: Zebranie wszystkich rozwiązań rzeczywistych**

Równanie posiada trzy rozwiązania: $x \in \{-3, -2, 2\}$.
**Odpowiedź:** Rozwiązaniami są liczby: $-3, -2, 2$.

### Przykład 2: Równanie rozwiązywane przez grupowanie wyrazów

Rozwiąż równanie: $x^3 - 3x^2 - 4x + 12 = 0$.

**Krok 1: Pogrupowanie wyrazów parami**

$$x^2(x - 3) - 4(x - 3) = 0$$
$$(x - 3)(x^2 - 4) = 0$$

**Krok 2: Rozkład czynnika kwadratowego i wyznaczenie pierwiastków**

$$(x - 3)(x - 2)(x + 2) = 0$$
$$x - 3 = 0 \implies x = 3$$
$$x - 2 = 0 \implies x = 2$$
$$x + 2 = 0 \implies x = -2$$
**Odpowiedź:** Zbiorem rozwiązań jest $\{-2, 2, 3\}$.

> **Wskazówka egzaminacyjna:**
> Czynnik typu $x^2 + 9 = 0$ lub $x^2 + 1 = 0$ jest zawsze dodatni dla każdego $x \in \mathbb{R}$ i **nie daje żadnych pierwiastków** rzeczywistych! Nie popełniaj błędu pisząc $x = \sqrt{-9} = -3$.
