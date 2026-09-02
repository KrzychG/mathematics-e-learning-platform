# 2. Działania na wielomianach

**Wielomianem** jednej zmiennej $x$ stopnia $n$ nazywamy funkcję postaci $W(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0$, gdzie współczynniki $a_i \in \mathbb{R}$ oraz $a_n \neq 0$. Dwa wielomiany są **równe** wtedy i tylko wtedy, gdy są tego samego stopnia i ich współczynniki przy odpowiednich potęgach zmiennej są identyczne.

> **Definicja: Własności wielomianów i stopień**
> - **Stopień wielomianu $\deg(W)$:** najwyższy wykładnik potęgi zmiennej przy współczynniku różnym od zera.
> - $\deg(P \cdot Q) = \deg(P) + \deg(Q)$ (stopień iloczynu to suma stopni wielomianów).
> - $\deg(P \pm Q) \le \max(\deg(P), \deg(Q))$ (stopień sumy nie przekracza wyższego ze stopni).
> - **Wyraz wolny:** wartość wielomianu dla argumentu zero: $W(0) = a_0$.

### Przykład 1: Mnożenie wielomianów i uporządkowanie

Dane są wielomiany $P(x) = 2x^2 - 3x + 1$ oraz $Q(x) = x^2 + 4$. Wyznacz iloczyn $W(x) = P(x) \cdot Q(x)$ i podaj jego stopień.

**Krok 1: Wymnożenie każdego wyrazu przez każdy**

$$W(x) = (2x^2 - 3x + 1)(x^2 + 4) = 2x^2(x^2 + 4) - 3x(x^2 + 4) + 1(x^2 + 4)$$
$$W(x) = 2x^4 + 8x^2 - 3x^3 - 12x + x^2 + 4$$

**Krok 2: Uporządkowanie według malejących potęg i redukcja**

$$W(x) = 2x^4 - 3x^3 + (8 + 1)x^2 - 12x + 4 = 2x^4 - 3x^3 + 9x^2 - 12x + 4$$
Najwyższa potęga to $x^4$, zatem $\deg(W) = 4$.

### Przykład 2: Równość wielomianów (wyznaczanie współczynników)

Wyznacz wartości parametrów $a$ i $b$, dla których wielomiany $F(x) = (ax + 2)(x^2 - 1)$ oraz $G(x) = 3x^3 + 2x^2 - 3x + b$ są równe.

**Krok 1: Rozwinięcie wielomianu $F(x)$**

$$F(x) = ax(x^2 - 1) + 2(x^2 - 1) = ax^3 - ax + 2x^2 - 2 = ax^3 + 2x^2 - ax - 2$$

**Krok 2: Przyrównanie współczynników przy odpowiednich potęgach**

Przy $x^3$: $a = 3$
Przy $x^2$: $2 = 2$ (zgadza się)

Przy $x^1$: $-a = -3 \implies a = 3$ (zgadza się)

Wyraz wolny: $-2 = b \implies b = -2$

**Odpowiedź:** Parametry wynoszą $a = 3$ oraz $b = -2$.

> **Wskazówka egzaminacyjna:**
> Zadania na równość wielomianów pojawiają się regularnie! Aby otrzymać komplet punktów, zawsze uporządkuj oba wielomiany do postaci kanonicznej (od najwyższej potęgi do najniższej), a następnie wyraźnie zapisz układ równań przyrównujący współczynniki przy tych samych potęgach.
