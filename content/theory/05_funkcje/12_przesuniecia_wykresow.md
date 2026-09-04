# 12. Przesunięcia wykresów f(x-a) i f(x)+b

Przekształcenia wykresów funkcji pozwalają na szybkie szkicowanie skomplikowanych wykresów na podstawie znajomości wykresu funkcji bazowej $y = f(x)$. Do podstawowych przekształceń należą **przesunięcie równoległe (translacja) o wektor** oraz **symetrie osiowe**.

> **Definicja: Reguły przekształcania wykresów**
> | Wzór | Przekształcenie geometryczne | Wpływ na punkty $(x, y)$ |
> | --- | --- | --- |
> | $y = f(x - p)$ | Przesunięcie o $p$ w prawo ($p > 0$) lub w lewo ($p < 0$) | $(x + p, y)$ |
> | $y = f(x) + q$ | Przesunięcie o $q$ w górę ($q > 0$) lub w dół ($q < 0$) | $(x, y + q)$ |
> | $y = f(x - p) + q$ | Translacja o wektor $\vec{v} = [p, q]$ | $(x + p, y + q)$ |
> | $y = -f(x)$ | Symetria osiowa względem osi $OX$ | $(x, -y)$ |
> | $y = f(-x)$ | Symetria osiowa względem osi $OY$ | $(-x, y)$ |

### Przykład 1: Translacja o wektor

Wykres funkcji $f(x) = \frac{2}{x}$ przesunięto o wektor $\vec{v} = [-3, 4]$. Podaj wzór otrzymanej funkcji $g(x)$, jej dziedzinę oraz równania asymptot.

**Krok 1: Zastosowanie wzoru na translację o wektor $[-3, 4]$**

Dla $p = -3$ i $q = 4$:
$$g(x) = f(x - (-3)) + 4 = f(x + 3) + 4 = \frac{2}{x + 3} + 4$$

**Krok 2: Wyznaczenie dziedziny i asymptot**

Mianownik: $x + 3 \neq 0 \implies x \neq -3$, zatem $D_g = \mathbb{R} \setminus \{-3\}$.
Asymptota pionowa: $x = -3$. Asymptota pozioma: $y = 4$.

### Przykład 2: Zmiana dziedziny i zbioru wartości pod wpływem wektora

Dziedziną funkcji $f$ jest przedział $\langle -2, 5 \rangle$, a jej zbiorem wartości jest $\langle 1, 7 \rangle$. Wyznacz dziedzinę i zbiór wartości funkcji $h(x) = f(x - 4) - 3$.

**Krok 1: Wpływ przesunięcia na dziedzinę ($x - 4$)**

Wykres przesuwamy o $4$ jednostki w prawo, zatem do każdego krańca dziedziny dodajemy $4$:
$$D_h = \langle -2 + 4, 5 + 4 \rangle = \langle 2, 9 \rangle$$

**Krok 2: Wpływ przesunięcia na zbiór wartości ($- 3$)**

Wykres przesuwamy o $3$ jednostki w dół, zatem od każdego krańca $ZW$ odejmujemy $3$:
$$ZW_h = \langle 1 - 3, 7 - 3 \rangle = \langle -2, 4 \rangle$$
**Odpowiedź:** $D_h = \langle 2, 9 \rangle$, $ZW_h = \langle -2, 4 \rangle$.

> **Wskazówka egzaminacyjna:**
> Najczęstsza pomyłka kierunku: we wzorze $f(x - 3)$ przesunięcie następuje **W PRAWO** (o $+3$), a we wzorze $f(x + 3)$ **W LEWO** (o $-3$)! Z kolei liczba poza nawiasem działa intuicyjnie: $+q$ w górę, $-q$ w dół.
