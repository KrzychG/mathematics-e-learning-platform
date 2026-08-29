# 4. Związek pierwiastkowania z potęgowaniem

Każdy pierwiastek arytmetyczny można zapisać w postaci potęgi o wykładniku ułamkowym (wymiernym). Pozwala to stosować jednolite prawa działań na potęgach do przekształcania skomplikowanych wyrażeń pierwiastkowych.

> **Definicja: Definicja potęgi o wykładniku wymiernym**
> Dla $a > 0$, $m \in \mathbb{Z}$ oraz $n \in \mathbb{N}, n \ge 2$:
>
> $$a^{\frac{1}{n}} = \sqrt[n]{a}, \qquad a^{\frac{m}{n}} = \sqrt[n]{a^m} = (\sqrt[n]{a})^m, \qquad a^{-r} = \frac{1}{a^r}$$

> **Definicja: Prawa działań na potęgach**
> Dla $a, b > 0$ oraz $r, s \in \mathbb{R}$:
>
> $$a^r \cdot a^s = a^{r+s}, \qquad \frac{a^r}{a^s} = a^{r-s}, \qquad (a^r)^s = a^{r \cdot s}, \qquad (a \cdot b)^r = a^r \cdot b^r$$

### Przykład 1: Obliczanie wartości potęgi o wykładniku ułamkowym

Oblicz wartość liczbową: $A = 27^{-\frac{4}{3}} \cdot 81^{\frac{3}{4}}$.

**Krok 1: Zamiana podstaw na potęgi liczby $3$**

$$27 = 3^3 \implies 27^{-\frac{4}{3}} = (3^3)^{-\frac{4}{3}} = 3^{3 \cdot \left(-\frac{4}{3}\right)} = 3^{-4}$$
$$81 = 3^4 \implies 81^{\frac{3}{4}} = (3^4)^{\frac{3}{4}} = 3^{4 \cdot \frac{3}{4}} = 3^3$$

**Krok 2: Mnożenie potęg o tej samej podstawie**

$$A = 3^{-4} \cdot 3^3 = 3^{-4 + 3} = 3^{-1} = \frac{1}{3}$$
**Odpowiedź:** Wartość wyrażenia wynosi $\frac{1}{3}$.

### Przykład 2: Zapisywanie iloczynu pierwiastków jako jednej potęgi

Zapisz wyrażenie $W = \sqrt{x \cdot \sqrt[3]{x}}$ w postaci potęgi $x^k$ dla $x > 0$.

**Krok 1: Przekształcenie wyrażenia pod pierwiastkiem zewnętrznym**

$$x \cdot \sqrt[3]{x} = x^1 \cdot x^{\frac{1}{3}} = x^{1 + \frac{1}{3}} = x^{\frac{4}{3}}$$

**Krok 2: Zastosowanie pierwiastka kwadratowego**

$$W = \sqrt{x^{\frac{4}{3}}} = \left(x^{\frac{4}{3}}\right)^{\frac{1}{2}} = x^{\frac{4}{3} \cdot \frac{1}{2}} = x^{\frac{2}{3}}$$
**Odpowiedź:** Wyrażenie jest równe $x^{\frac{2}{3}}$.

> **Wskazówka egzaminacyjna:**
> Przy działaniach na potęgach o różnych podstawach (np. $2, 4, 8, 16, 27, 81$) zawsze pierwszym krokiem powinno być sprowadzenie wszystkich liczb do wspólnej podstawy będącej liczbą pierwszą!
