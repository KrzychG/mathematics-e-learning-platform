# 3. Równania i nierówności kwadratowe

**Równaniem kwadratowym** nazywamy równanie postaci $ax^2 + bx + c = 0$, gdzie $a, b, c \in \mathbb{R}$ oraz $a \neq 0$. O liczbie rozwiązań rzeczywistych decyduje znak **wyróżnika równania kwadratowego** $\Delta = b^2 - 4ac$.

> **Definicja: Wyróżnik $\Delta$ i wzory na pierwiastki**
> $$\Delta = b^2 - 4ac$$
>
> - **$\Delta > 0$:** dwa różne pierwiastki rzeczywiste: $$x_1 = \frac{-b - \sqrt{\Delta}}{2a}, \qquad x_2 = \frac{-b + \sqrt{\Delta}}{2a}$$
> - **$\Delta = 0$:** jeden pierwiastek podwójny: $$x_0 = \frac{-b}{2a}$$
> - **$\Delta < 0$:** brak rozwiązań w zbiorze liczb rzeczywistych ($x \in \emptyset$).

### Przykład 1: Równanie kwadratowe niepełne

Rozwiąż równania kwadratowe bez używania $\Delta$: a) $3x^2 - 12 = 0$, b) $2x^2 - 5x = 0$.

**Przypadek a) brak współczynnika $b$ ($b = 0$):**

$$3x^2 = 12 \implies x^2 = 4 \implies x = -2 \quad \lor \quad x = 2$$

**Przypadek b) brak wyrazu wolnego ($c = 0$): wyłączenie $x$ przed nawias**

$$x(2x - 5) = 0 \implies x = 0 \quad \lor \quad 2x - 5 = 0 \implies x = \frac{5}{2} = 2{,}5$$
**Odpowiedź:** a) $x \in \{-2, 2\}$, b) $x \in \{0; 2{,}5\}$.

### Przykład 2: Nierówność kwadratowa (szkic paraboli)

Rozwiąż nierówność kwadratową: $-x^2 + 2x + 8 \ge 0$.

**Krok 1: Wyznaczenie miejsc zerowych**

$$a = -1, \quad b = 2, \quad c = 8$$
$$\Delta = 2^2 - 4 \cdot (-1) \cdot 8 = 4 + 32 = 36, \quad \sqrt{\Delta} = 6$$
$$x_1 = \frac{-2 - 6}{2 \cdot (-1)} = \frac{-8}{-2} = 4, \qquad x_2 = \frac{-2 + 6}{-2} = \frac{4}{-2} = -2$$

**Krok 2: Szkic paraboli i odczytanie przedziału**

Współczynnik $a = -1 < 0$, więc ramiona paraboli skierowane są **w dół**.
Wartości $\ge 0$ (nad osią i na osi) funkcja przyjmuje pomiędzy miejscami zerowymi:
$$x \in \langle -2, 4 \rangle$$
**Odpowiedź:** Zbiorem rozwiązań jest przedział $\langle -2, 4 \rangle$.

> **Wskazówka egzaminacyjna:**
> Nierówność kwadratowa za 2 punkty pojawia się niemal na KAŻDYM egzaminie! Pamiętaj: samo wyliczenie $x_1$ i $x_2$ daje tylko 1 punkt. Drugi punkt otrzymujesz za prawidłowy zapis zbioru rozwiązań w postaci przedziału na podstawie szkicu paraboli (kierunek ramion zależy od znaku $a$!).
