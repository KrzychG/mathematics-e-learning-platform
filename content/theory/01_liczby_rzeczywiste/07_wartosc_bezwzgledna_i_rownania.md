# 7. Wartość bezwzględna i równania

**Wartość bezwzględna** liczby rzeczywistej $x$ to odległość tej liczby od zera na osi liczbowej. Geometrycznie wyrażenie $|x - a|$ oznacza odległość między liczbą $x$ a liczbą $a$ na osi liczbowej.

> **Definicja: Definicja i interpretacja geometryczna**
> $$|x| = \begin{cases} x & \text{dla } x \ge 0 \\ -x & \text{dla } x < 0 \end{cases}, \qquad |x - a| = r \iff x = a - r \quad \lor \quad x = a + r$$
>
> - $|x - a| \le r \iff x \in \langle a - r, a + r \rangle$ (przedział domknięty wokół środka $a$)
> - $|x - a| \ge r \iff x \in (-\infty, a - r\rangle \cup \langle a + r, +\infty)$ (suma przedziałów zewnętrznych)
> - Zawsze $|x| \ge 0$ dla każdego $x \in \mathbb{R}$.

### Przykład 1: Równanie z wartością bezwzględną

Rozwiąż równanie: $|2x - 6| = 8$.

**Krok 1: Rozbicie na dwa przypadki**

$$2x - 6 = 8 \qquad \lor \qquad 2x - 6 = -8$$

**Krok 2: Rozwiązanie równań liniowych**

$$2x = 14 \implies x = 7$$
$$2x = -2 \implies x = -1$$
**Odpowiedź:** Rozwiązaniami równania są liczby $x = -1$ oraz $x = 7$.

### Przykład 2: Nierówność i interpretacja geometryczna

Zapisz nierówność z wartością bezwzględną, której zbiorem rozwiązań jest przedział $\langle -2, 8 \rangle$.

**Krok 1: Wyznaczenie środka $a$ i promienia $r$**

$$a = \frac{-2 + 8}{2} = \frac{6}{2} = 3 \quad \text{(środek przedziału)}$$
$$r = \frac{8 - (-2)}{2} = \frac{10}{2} = 5 \quad \text{(promień / odległość)}$$

**Krok 2: Sformułowanie nierówności**

Punkty oddalone od liczby $3$ o nie więcej niż $5$:
$$|x - 3| \le 5$$
**Odpowiedź:** Szukana nierówność to $|x - 3| \le 5$.

> **Wskazówka egzaminacyjna:**
> Pamiętaj: równanie $|x - a| = -3$ jest **sprzeczne** (brak rozwiązań), ponieważ wartość bezwzględna nigdy nie może być ujemna! Podobnie nierówność $|x - a| < 0$ nie ma rozwiązań, a nierówność $|x - a| \ge 0$ jest spełniona dla wszystkich $x \in \mathbb{R}$.
