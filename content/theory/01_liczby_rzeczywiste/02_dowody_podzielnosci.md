# 2. Dowody podzielności i reszty z dzielenia

Liczba całkowita $a$ jest **podzielna** przez liczbę całkowitą $b \neq 0$, jeśli istnieje taka liczba całkowita $k$, że $a = k \cdot b$. Zapisujemy to symbolicznie $b \mid a$. Każda liczba całkowita $n$ przy dzieleniu przez $k$ daje resztę $r \in \{0, 1, \dots, k-1\}$, co wyraża wzór $n = q \cdot k + r$.

> **Definicja: Postaci liczb o danej parzystości i reszcie**
> - Liczba parzysta: $n = 2k$, gdzie $k \in \mathbb{Z}$
> - Liczba nieparzysta: $n = 2k + 1$ (lub $2k - 1$), gdzie $k \in \mathbb{Z}$
> - Liczba dająca resztę $r$ z dzielenia przez $m$: $n = m \cdot k + r$, gdzie $r \in \{0, 1, \dots, m-1\}$
> - Iloczyn dwóch kolejnych liczb całkowitych $n(n+1)$ jest zawsze podzielny przez $2$.
> - Iloczyn trzech kolejnych liczb całkowitych $(n-1)n(n+1)$ jest zawsze podzielny przez $6$ ($2 \cdot 3$).

### Przykład 1: Dowód podzielności przez wyłączanie wspólnego czynnika

Wykaż, że dla każdej liczby naturalnej $n \ge 1$ liczba $L = 5^{n+2} - 5^n$ jest podzielna przez $24$.

**Krok 1: Rozpisanie potęg i wyłączenie wspólnego czynnika**

$$L = 5^n \cdot 5^2 - 5^n = 5^n \cdot (5^2 - 1)$$

**Krok 2: Wykazanie podzielności przez $24$**

$$L = 5^n \cdot (25 - 1) = 5^n \cdot 24 = 24 \cdot 5^n$$
Ponieważ $n \ge 1$, to $5^n$ jest liczbą całkowitą dodatnią. Zatem liczba $L$ jest iloczynem liczby $24$ i liczby całkowitej $5^n$, co dowodzi, że $L$ jest podzielna przez $24$.

### Przykład 2: Dowód z wykorzystaniem kolejnych liczb całkowitych

Wykaż, że dla każdej liczby całkowitej $n$ liczba $W = n^3 - n$ jest podzielna przez $6$.

**Krok 1: Rozkład wyrażenia na czynniki**

$$W = n(n^2 - 1) = (n - 1) \cdot n \cdot (n + 1)$$

**Krok 2: Uzasadnienie podzielności**

Wyrażenie $(n - 1) \cdot n \cdot (n + 1)$ to iloczyn **trzech kolejnych liczb całkowitych**.
Wśród trzech kolejnych liczb całkowitych co najmniej jedna jest podzielna przez $2$ oraz dokładnie jedna jest podzielna przez $3$.

Ponieważ liczby $2$ i $3$ są względnie pierwsze ($\text{NWD}(2, 3) = 1$), iloczyn ten jest podzielny przez $2 \cdot 3 = 6$.

> **Wskazówka egzaminacyjna:**
> Zadania typu „Wykaż, że...” na egzaminie wymagają pełnego komentarza słownego! Sam zapis algebraiczny bez wniosku (np. „liczba stanowi iloczyn liczby 6 i liczby całkowitej, zatem jest podzielna przez 6”) może skutkować utratą punktu za brak uzasadnienia.
