# 1. Układy równań liniowych z dwiema niewiadomymi

**Układem dwóch równań liniowych** z dwiema niewiadomymi $x$ i $y$ nazywamy koniunkcję dwóch równań pierwszego stopnia. Rozwiązaniem układu jest para liczb $(x, y)$, która spełnia jednocześnie oba równania. Geometrycznie każde równanie liniowe reprezentuje prostą w układzie współrzędnych.

> **Definicja: Klasyfikacja układów i interpretacja geometryczna**
> Układ oznaczony
>
> Dokładnie jedna para rozwiązań $(x_0, y_0)$.
>
> Proste przecinają się w 1 punkcie
>
> Układ nieoznaczony
>
> Nieskończenie wiele rozwiązań (tożsamościowy: $0=0$).
>
> Proste pokrywają się
>
> Układ sprzeczny
>
> Brak rozwiązań (sprzeczność: np. $0=7$).
>
> Proste równoległe rozłączne

### Przykład 1: Metoda przeciwnych współczynników

Rozwiąż układ równań metodą przeciwnych współczynników:
$$\begin{cases} 3x + 2y = 12 \\ 2x - 3y = -5 \end{cases}$$

**Krok 1: Przemnożenie równań, aby uzyskać przeciwne współczynniki przy $y$**

Mnożymy pierwsze równanie przez $3$, a drugie przez $2$:
$$\begin{cases} 9x + 6y = 36 \\ 4x - 6y = -10 \end{cases}$$

**Krok 2: Dodanie równań stronami i wyznaczenie $x$ oraz $y$**

$$(9x + 4x) + (6y - 6y) = 36 - 10 \implies 13x = 26 \implies x = 2$$
Podstawiamy $x = 2$ do pierwszego równania:
$$3(2) + 2y = 12 \implies 6 + 2y = 12 \implies 2y = 6 \implies y = 3$$
**Odpowiedź:** Rozwiązaniem jest para liczb $(x, y) = (2, 3)$.

### Przykład 2: Metoda podstawiania

Rozwiąż układ równań metodą podstawiania:
$$\begin{cases} x - 2y = 5 \\ 3x + 4y = 5 \end{cases}$$

**Krok 1: Wyznaczenie zmiennej $x$ z pierwszego równania**

$$x = 2y + 5$$

**Krok 2: Wstawienie do drugiego równania**

$$3(2y + 5) + 4y = 5 \implies 6y + 15 + 4y = 5 \implies 10y = -10 \implies y = -1$$
Obliczamy $x$:
$$x = 2(-1) + 5 = -2 + 5 = 3$$
**Odpowiedź:** Rozwiązaniem układu jest para $(x, y) = (3, -1)$.

> **Wskazówka egzaminacyjna:**
> Rozwiązaniem układu równań z dwiema niewiadomymi jest **para liczb** $(x, y)$, a nie jedna liczba! Pamiętaj, aby po wyliczeniu pierwszej niewiadomej (np. $x$) zawsze podstawić ją z powrotem i wyznaczyć drugą niewiadomą ($y$).
