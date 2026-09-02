# 3. Wyłączanie wspólnego czynnika poza nawias

**Rozkład wielomianu na czynniki** (faktoryzacja) polega na przedstawieniu sumy algebraicznej w postaci iloczynu wielomianów możliwie najniższych stopni. Jest to kluczowa umiejętność potrzebna do rozwiązywania równań wyższych stopni, określania miejsc zerowych oraz skracania ułamków algebraicznych.

> **Definicja: Główne metody rozkładu na czynniki**
> 1. **Wyłączenie wspólnego czynnika przed nawias:** szukamy największego wspólnego dzielnika współczynników oraz wspólnej potęgi zmiennej: $ax + ay = a(x + y)$.
> 2. **Grupowanie wyrazów:** łączymy wyrazy w pary lub trójki, wyłączamy z nich wspólne czynniki, uzyskując jednakowy nawias: $ac + bc + ad + bd = c(a+b) + d(a+b) = (a+b)(c+d)$.
> 3. **Zastosowanie wzorów skróconego mnożenia:** np. $a^2 - b^2 = (a-b)(a+b)$.
> 4. **Rozkład trójmianu kwadratowego za pomocą $\Delta$:** $ax^2 + bx + c = a(x - x_1)(x - x_2)$.

### Przykład 1: Metoda grupowania wyrazów

Rozłóż wielomian $W(x) = 2x^3 - 6x^2 - x + 3$ na czynniki możliwie najniższego stopnia.

**Krok 1: Pogrupowanie w pary i wyłączenie czynników**

$$W(x) = (2x^3 - 6x^2) - (x - 3) = 2x^2(x - 3) - 1(x - 3)$$

**Krok 2: Wyłączenie wspólnego nawiasu $(x - 3)$**

$$W(x) = (x - 3)(2x^2 - 1)$$
Czynnik $2x^2 - 1$ można jeszcze rozłożyć ze wzoru na różnicę kwadratów: $(\sqrt{2}x - 1)(\sqrt{2}x + 1)$.
**Odpowiedź:** $W(x) = (x - 3)(\sqrt{2}x - 1)(\sqrt{2}x + 1)$ (lub $(x - 3)(2x^2 - 1)$).

### Przykład 2: Złożona faktoryzacja z wyłączeniem potęgi zmiennej

Rozłóż na czynniki wielomian $P(x) = 3x^5 - 12x^3$.

**Krok 1: Wyłączenie wspólnego czynnika $3x^3$**

$$P(x) = 3x^3(x^2 - 4)$$

**Krok 2: Rozkład nawiasu ze wzoru na różnicę kwadratów**

$$x^2 - 4 = (x - 2)(x + 2)$$
$$P(x) = 3x^3(x - 2)(x + 2)$$
**Odpowiedź:** Czynnikami wielomianu są $3x^3$, $(x - 2)$ oraz $(x + 2)$.

> **Wskazówka egzaminacyjna:**
> Nie zatrzymuj się w połowie rozkładu! Jeśli po wyłączeniu czynnika w nawiasie zostaje wyrażenie typu $(x^2 - 9)$ lub $(4x^2 - 25)$, musisz bezwzględnie rozbić je do postaci $(x - 3)(x + 3)$ lub $(2x - 5)(2x + 5)$. Natomiast suma kwadratów $x^2 + 4$ w zbiorze $\mathbb{R}$ jest nierozkładalna.
