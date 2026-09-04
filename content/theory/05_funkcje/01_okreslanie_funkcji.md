# 1. Określanie funkcji (słownie, tabela, wykres, wzór)

**Funkcją** $f$ ze zbioru $X$ w zbiór $Y$ nazywamy przyporządkowanie, które **każdemu** elementowi $x \in X$ przyporządkowuje **dokładnie jeden** element $y \in Y$. Zbiór $X$ nazywamy **dziedziną funkcji** i oznaczamy $D$ (lub $D_f$), a zbiór wszystkich wartości przyjmowanych przez funkcję nazywamy **zbiorem wartości** ($ZW$ lub $ZW_f$).

> **Definicja: Sposoby reprezentacji funkcji**
> - **Wzór algebraiczny:** np. $f(x) = 2x^2 - 1$ dla $x \in \mathbb{R}$.
> - **Tabela wartości:** zestawienie par argument-wartość $(x, y)$.
> - **Wykres w układzie współrzędnych:** zbiór punktów $(x, f(x))$. Zbiór punktów na płaszczyźnie jest wykresem funkcji, jeśli każda prosta pionowa $x = c$ przecina go w **co najwyżej jednym punkcie**.
> - **Opis słowny i graf:** przyporządkowanie opisane regułą słowną lub strzałkami między zbiorami.

### Przykład 1: Wyznaczanie dziedziny naturalnej funkcji ze wzoru

Wyznacz dziedzinę funkcji $f(x) = \frac{\sqrt{2x + 6}}{x - 1}$.

**Krok 1: Warunek na wyrażenie pod pierwiastkiem kwadratowym (nieujemne)**

$$2x + 6 \ge 0 \implies 2x \ge -6 \implies x \ge -3$$

**Krok 2: Warunek na mianownik (różny od zera) i część wspólna**

$$x - 1 \neq 0 \implies x \neq 1$$
Część wspólna obu warunków: $x \ge -3$ oraz $x \neq 1$.
**Odpowiedź:** Dziedziną funkcji jest zbiór $D = \langle -3, 1) \cup (1, +\infty)$.

### Przykład 2: Sprawdzanie, czy przyporządkowanie jest funkcją

Czy przyporządkowanie przypisujące każdej liczbie rzeczywistej $x$ liczbę $y$ spełniającą równanie $x^2 + y^2 = 9$ jest funkcją $y = f(x)$?

**Krok 1: Weryfikacja jednoznaczności wartości**

Dla $x = 0$ otrzymujemy: $0^2 + y^2 = 9 \implies y^2 = 9 \implies y = 3 \quad \lor \quad y = -3$.

**Krok 2: Wniosek z definicji funkcji**

Jednemu argumentowi $x = 0$ przyporządkowane zostały **dwie różne wartości** ($3$ oraz $-3$).
Geometrycznie równanie $x^2 + y^2 = 9$ opisuje okrąg o środku $(0, 0)$ i promieniu $3$, który pionowa prosta $x = 0$ przecina w dwóch punktach $(0, 3)$ i $(0, -3)$.

**Odpowiedź:** To przyporządkowanie **nie jest funkcją**.

> **Wskazówka egzaminacyjna:**
> Dwa najważniejsze ograniczenia dziedziny w szkole średniej to: **mianownik nie może być zerem** ($Q(x) \neq 0$) oraz **wyrażenie pod pierwiastkiem parzystego stopnia musi być nieujemne** ($g(x) \ge 0$). Zawsze zapisz te warunki w układzie nierówności!
