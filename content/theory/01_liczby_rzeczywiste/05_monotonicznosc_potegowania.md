# 5. Monotoniczność potęgowania

Monotoniczność funkcji potęgowej i wykładniczej pozwala na porównywanie liczb bez konieczności wykonywania żmudnych obliczeń przybliżonych. Zachowanie nierówności zależy od tego, czy podstawa potęgi jest większa od $1$, czy mieści się w przedziale $(0, 1)$.

> **Definicja: Reguły porównywania potęg**
> Gdy podstawa $a > 1$ (funkcja rosnąca):
>
> Większy wykładnik oznacza większą wartość potęgi:
>
> $$r < s \iff a^r < a^s$$
>
> Zwrot nierówności bez zmian
>
> Gdy podstawa $0 < a < 1$ (funkcja malejąca):
>
> Większy wykładnik oznacza mniejszą wartość potęgi:
>
> $$r < s \iff a^r > a^s$$
>
> Zmiana zwrotu nierówności

### Przykład 1: Porównywanie liczb o różnych podstawach i wykładnikach

Uporządkuj liczby $a = 2^{60}$, $b = 3^{40}$, $c = 5^{20}$ rosnąco.

**Krok 1: Sprowadzenie potęg do wspólnego wykładnika**

Wspólnym dzielnikiem wykładników $60, 40, 20$ jest $20$:
$$a = 2^{60} = (2^3)^{20} = 8^{20}$$
$$b = 3^{40} = (3^2)^{20} = 9^{20}$$
$$c = 5^{20} = 5^{20}$$

**Krok 2: Porównanie podstaw dla jednakowego wykładnika dodatniego**

Ponieważ $5 < 8 < 9$, to $5^{20} < 8^{20} < 9^{20}$, czyli:
$$c < a < b$$
**Odpowiedź:** W kolejności rosnącej: $5^{20}, 2^{60}, 3^{40}$.

### Przykład 2: Nierówność potęgowa z podstawą ułamkową

Rozwiąż nierówność: $\left(\frac{1}{2}\right)^{2x - 3} \ge \left(\frac{1}{2}\right)^{x + 1}$.

**Krok 1: Identyfikacja podstawy**

Podstawa wynosi $a = \frac{1}{2} \in (0, 1)$, zatem funkcja jest malejąca.

**Krok 2: Porównanie wykładników ze zmianą zwrotu**

$$2x - 3 \le x + 1 \implies 2x - x \le 1 + 3 \implies x \le 4$$
**Odpowiedź:** Rozwiązaniem jest przedział $x \in (-\infty, 4\rangle$.

> **Wskazówka egzaminacyjna:**
> Najczęstszym błędem na egzaminie jest zapomnienie o zmianie zwrotu nierówności, gdy opuszczamy podstawę potęgi będącą ułamkiem z przedziału $(0, 1)$! Zawsze sprawdź, czy podstawa jest większa od $1$.
