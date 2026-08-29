# 3. Pierwiastki dowolnego stopnia

**Pierwiastkiem arytmetycznym** stopnia $n$ ($n \in \mathbb{N}, n \ge 2$) z liczby nieujemnej $a \ge 0$ nazywamy taką liczbę $b \ge 0$, że $b^n = a$. Oznaczamy go symbolem $\sqrt[n]{a}$. Dla stopni nieparzystych pierwiastek jest zdefiniowany także dla liczb ujemnych (np. $\sqrt[3]{-8} = -2$).

> **Definicja: Własności i prawa działań na pierwiastkach**
> Dla liczb $a, b \ge 0$ oraz $n, k \in \mathbb{N}, n, k \ge 2$:
>
> $$\sqrt[n]{a \cdot b} = \sqrt[n]{a} \cdot \sqrt[n]{b}, \qquad \sqrt[n]{\frac{a}{b}} = \frac{\sqrt[n]{a}}{\sqrt[n]{b}} \quad (b > 0)$$
> $$(\sqrt[n]{a})^n = a, \qquad \sqrt{a^2} = |a|$$

### Przykład 1: Wyłączanie czynnika przed pierwiastek i redukcja

Uprość wyrażenie: $W = \sqrt{72} - 3\sqrt{32} + 2\sqrt{50}$.

**Krok 1: Rozkład liczb pod pierwiastkami na czynniki z kwadratami**

$$\sqrt{72} = \sqrt{36 \cdot 2} = 6\sqrt{2}$$
$$\sqrt{32} = \sqrt{16 \cdot 2} = 4\sqrt{2} \implies 3\sqrt{32} = 3 \cdot 4\sqrt{2} = 12\sqrt{2}$$
$$\sqrt{50} = \sqrt{25 \cdot 2} = 5\sqrt{2} \implies 2\sqrt{50} = 2 \cdot 5\sqrt{2} = 10\sqrt{2}$$

**Krok 2: Redukcja wyrazów podobnych**

$$W = 6\sqrt{2} - 12\sqrt{2} + 10\sqrt{2} = (6 - 12 + 10)\sqrt{2} = 4\sqrt{2}$$
**Odpowiedź:** Wartość wyrażenia wynosi $4\sqrt{2}$.

### Przykład 2: Usuwanie niewymierności z mianownika

Usuń niewymierność z mianownika ułamka: $U = \frac{4}{\sqrt{5} - 1}$.

**Krok 1: Mnożenie licznika i mianownika przez sprzężenie**

Mnożymy przez $(\sqrt{5} + 1)$, korzystając ze wzoru $(a - b)(a + b) = a^2 - b^2$:
$$U = \frac{4(\sqrt{5} + 1)}{(\sqrt{5} - 1)(\sqrt{5} + 1)} = \frac{4(\sqrt{5} + 1)}{(\sqrt{5})^2 - 1^2}$$

**Krok 2: Obliczenie i redukcja**

$$U = \frac{4(\sqrt{5} + 1)}{5 - 1} = \frac{4(\sqrt{5} + 1)}{4} = \sqrt{5} + 1$$
**Odpowiedź:** Wynik to $\sqrt{5} + 1$.

> **Wskazówka egzaminacyjna:**
> Klasyczna pułapka: $\sqrt{a^2 + b^2} \neq a + b$ oraz $\sqrt{a + b} \neq \sqrt{a} + \sqrt{b}$! Pamiętaj również, że $\sqrt{x^2} = |x|$ – pierwiastek kwadratowy z definicji przyjmuje wyłącznie wartości nieujemne!
