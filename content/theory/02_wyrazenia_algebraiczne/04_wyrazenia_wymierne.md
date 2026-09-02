# 4. Wyrażenia wymierne

**Wyrażeniem wymiernym** nazywamy iloraz dwóch wielomianów $\frac{P(x)}{Q(x)}$, gdzie $Q(x)$ nie jest wielomianem zerowym. Fundamentalnym warunkiem przy pracy z wyrażeniami wymiernymi jest określenie ich **dziedziny** – mianownik nie może być równy zero ($Q(x) \neq 0$).

> **Definicja: Działania na wyrażeniach wymiernych**
> - **Dziedzina $D$:** $D = \mathbb{R} \setminus \{x: Q(x) = 0\}$.
> - **Skracanie:** rozkładamy licznik i mianownik na czynniki, po czym redukujemy wspólne nawiasy (tylko w dziedzinie $D$!).
> - **Dodawanie/Odejmowanie:** sprowadzamy ułamki do wspólnego mianownika (najczęściej iloczynu nieskracalnych czynników).
> - **Mnożenie/Dzielenie:** mnożymy liczniki i mianowniki, a dzielenie zastępujemy mnożeniem przez odwrotność drugiego ułamka.

### Przykład 1: Dziedzina i skracanie ułamka algebraicznego

Wyznacz dziedzinę i uprość wyrażenie: $W(x) = \frac{x^2 - 9}{2x^2 + 6x}$.

**Krok 1: Wyznaczenie dziedziny (założenie mianownik $\neq 0$)**

$$2x^2 + 6x = 0 \implies 2x(x + 3) = 0 \implies x = 0 \quad \lor \quad x = -3$$
$$D = \mathbb{R} \setminus \{-3, 0\}$$

**Krok 2: Rozkład licznika i skracanie**

Licznik: $x^2 - 9 = (x - 3)(x + 3)$
Mianownik: $2x(x + 3)$

$$W(x) = \frac{(x - 3)(x + 3)}{2x(x + 3)} = \frac{x - 3}{2x} \quad \text{dla } x \in D$$
**Odpowiedź:** Dziedzina to $\mathbb{R} \setminus \{-3, 0\}$, a uproszczona postać to $\frac{x - 3}{2x}$.

### Przykład 2: Dodawanie ułamków o różnych mianownikach

Wykonaj działanie: $A(x) = \frac{2}{x - 1} - \frac{1}{x + 2}$.

**Krok 1: Dziedzina i wspólny mianownik**

Dziedzina: $x \neq 1$ oraz $x \neq -2$, czyli $D = \mathbb{R} \setminus \{-2, 1\}$.
Wspólny mianownik to $(x - 1)(x + 2)$.

**Krok 2: Rozszerzenie ułamków i odjęcie liczników**

$$A(x) = \frac{2(x + 2)}{(x - 1)(x + 2)} - \frac{1(x - 1)}{(x - 1)(x + 2)} = \frac{2x + 4 - (x - 1)}{(x - 1)(x + 2)}$$
$$A(x) = \frac{2x + 4 - x + 1}{(x - 1)(x + 2)} = \frac{x + 5}{(x - 1)(x + 2)}$$
**Odpowiedź:** Wynik to $\frac{x + 5}{(x - 1)(x + 2)}$ dla $x \in \mathbb{R} \setminus \{-2, 1\}$.

> **Wskazówka egzaminacyjna:**
> NIGDY nie skracaj pojedynczych wyrazów sumy (np. $\frac{x^2 - 9}{2x^2} \neq -\frac{9}{2}$)! Skracać wolno WYŁĄCZNIE całe czynniki (nawiasy) będące w relacji mnożenia. Ponadto za brak podania dziedziny w zadaniu otwartym tracisz punkty!
