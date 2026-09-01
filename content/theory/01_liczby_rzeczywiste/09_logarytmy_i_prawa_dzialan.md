# 9. Logarytmy i prawa działań

**Logarytmem** liczby dodatniej $b$ przy dodatniej i różnej od $1$ podstawie $a$ nazywamy wykładnik potęgi $c$, do której należy podnieść podstawę $a$, aby otrzymać liczbę logarytmowaną $b$. Logarytm o podstawie $10$ nazywamy dziesiętnym i zapisujemy $\log b$.

> **Definicja: Definicja i założenia logarytmu**
> $$\log_a b = c \iff a^c = b \qquad (a > 0, \; a \neq 1, \; b > 0)$$
>
> Szczególne wartości: $\log_a 1 = 0$, $\log_a a = 1$, $a^{\log_a b} = b$.

> **Definicja: Prawa działań na logarytmach**
> Dla $a > 0, a \neq 1$ oraz $x, y > 0, p \in \mathbb{R}$:
>
> $$\log_a(x \cdot y) = \log_a x + \log_a y, \qquad \log_a\left(\frac{x}{y}\right) = \log_a x - \log_a y, \qquad \log_a(x^p) = p \cdot \log_a x$$

### Przykład 1: Obliczanie wartości wyrażenia z praw działań

Oblicz wartość wyrażenia: $W = 2\log_3 6 - \log_3 4$.

**Krok 1: Wciągnięcie współczynnika do wykładnika potęgi**

$$2\log_3 6 = \log_3(6^2) = \log_3 36$$

**Krok 2: Zastosowanie wzoru na różnicę logarytmów**

$$W = \log_3 36 - \log_3 4 = \log_3\left(\frac{36}{4}\right) = \log_3 9$$
Ponieważ $3^2 = 9$, to $\log_3 9 = 2$.
**Odpowiedź:** Wartość wyrażenia wynosi $2$.

### Przykład 2: Logarytm z pierwiastkiem i ułamkiem

Oblicz wartość liczby: $L = \log_{\sqrt{2}} 8$.

**Krok 1: Zapisanie z definicji logarytmu**

Niech $\log_{\sqrt{2}} 8 = c$. Wtedy:
$$(\sqrt{2})^c = 8$$

**Krok 2: Sprowadzenie do wspólnej podstawy $2$**

$$(2^{\frac{1}{2}})^c = 2^3 \implies 2^{\frac{c}{2}} = 2^3$$
$$\frac{c}{2} = 3 \implies c = 6$$
**Odpowiedź:** $\log_{\sqrt{2}} 8 = 6$.

> **Wskazówka egzaminacyjna:**
> Pamiętaj: $\log_a(x + y) \neq \log_a x + \log_a y$! Suma logarytmów daje logarytm iloczynu $\log_a(x \cdot y)$, a nie sumy. Ponadto przed zastosowaniem wzoru na sumę lub różnicę logarytmów należy najpierw usunąć współczynniki stojące przed logarytmem (np. $2\log x = \log x^2$).
