# 1. Wzory skróconego mnożenia

**Wzory skróconego mnożenia** pozwalają na szybkie potęgowanie sum i różnic oraz rozkładanie sum algebraicznych na iloczyny bez konieczności czasochłonnego mnożenia każdego wyrazu przez każdy. Są one fundamentalnym narzędziem w przekształceniach algebraicznych na egzaminie.

> **Definicja: Wzory stopnia drugiego i trzeciego**
> $$(a + b)^2 = a^2 + 2ab + b^2, \qquad (a - b)^2 = a^2 - 2ab + b^2$$
> $$a^2 - b^2 = (a - b)(a + b)$$
>
> $$(a + b)^3 = a^3 + 3a^2b + 3ab^2 + b^3, \qquad (a - b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$$
> $$a^3 - b^3 = (a - b)(a^2 + ab + b^2), \qquad a^3 + b^3 = (a + b)(a^2 - ab + b^2)$$

### Przykład 1: Upraszczanie wyrażenia ze wzorami skróconego mnożenia

Rozwiń i zredukuj wyrażenie: $W = (2x - 3)^2 - (x + 4)(x - 4) - 3x(x - 2)$.

**Krok 1: Zastosowanie wzorów $(a-b)^2$ oraz $(a+b)(a-b)$**

$$(2x - 3)^2 = (2x)^2 - 2 \cdot 2x \cdot 3 + 3^2 = 4x^2 - 12x + 9$$
$$(x + 4)(x - 4) = x^2 - 4^2 = x^2 - 16$$
$$3x(x - 2) = 3x^2 - 6x$$

**Krok 2: Złożenie całości z uwzględnieniem znaków minus przed nawiasami**

$$W = (4x^2 - 12x + 9) - (x^2 - 16) - (3x^2 - 6x)$$
$$W = 4x^2 - 12x + 9 - x^2 + 16 - 3x^2 + 6x$$
$$W = (4 - 1 - 3)x^2 + (-12 + 6)x + (9 + 16) = -6x + 25$$
**Odpowiedź:** Uproszczone wyrażenie to $-6x + 25$.

### Przykład 2: Zastosowanie różnicy kwadratów do obliczeń liczbowych

Oblicz sprytnie wartość liczbową: $L = 1005^2 - 995^2$.

**Krok 1: Zastosowanie wzoru $a^2 - b^2 = (a - b)(a + b)$**

Dla $a = 1005$ i $b = 995$:
$$L = (1005 - 995)(1005 + 995)$$

**Krok 2: Błyskawiczne obliczenie iloczynu**

$$L = 10 \cdot 2000 = 20\,000$$
**Odpowiedź:** Wartość wynosi $20\,000$ (bez żmudnego podnoszenia do kwadratu).

> **Wskazówka egzaminacyjna:**
> Najczęstszy błąd zdających to gubienie podwojonego iloczynu: $(a + b)^2 \neq a^2 + b^2$! Prawidłowo: $(a + b)^2 = a^2 + 2ab + b^2$. Pamiętaj także o zmianie znaków wszystkich wyrazów, gdy przed nawiasem stoi znak minus: $-(a^2 - b^2) = -a^2 + b^2$.
