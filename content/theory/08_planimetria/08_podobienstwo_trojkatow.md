# 8. Cechy podobieństwa trójkątów (BBB, BKB, KKK)

Dwa trójkąty są **podobne** ($\Delta ABC \sim \Delta A'B'C'$), gdy mają równe odpowiednie kąty wewnętrzne, a stosunki długości ich odpowiadających boków są równe i wynoszą stałą liczbę $k > 0$ zwaną **skalą podobieństwa**.

> **Definicja: Trzy cechy podobieństwa trójkątów**
> - **Cecha KKK (Kąt – Kąt – Kąt / Kąt – Kąt):** Jeżeli dwa kąty jednego trójkąta są równe dwóm kątom drugiego trójkąta, to trójkąty są podobne.
> - **Cecha BBB (Bok – Bok – Bok):** Jeżeli długości boków jednego trójkąta są proporcjonalne do długości odpowiednich boków drugiego trójkąta:
> $$\frac{a'}{a} = \frac{b'}{b} = \frac{c'}{c} = k$$
> - **Cecha BKB (Bok – Kąt – Bok):** Jeżeli dwa boki jednego trójkąta są proporcjonalne do dwóch boków drugiego, a kąty zawarte między tymi bokami są równe, to trójkąty są podobne.

### Przykład 1: Wysokość opuszczona na przeciwprostokątną

W trójkącie prostokątnym wysokość $h$ poprowadzona z wierzchołka kąta prostego dzieli przeciwprostokątną na dwa odcinki o długościach $x = 4\text{ cm}$ oraz $y = 9\text{ cm}$. Wyznacz wysokość $h$ oraz długości przyprostokątnych trójkąta.

**Krok 1: Podobieństwo trójkątów odciętych przez wysokość**

Wysokość dzieli trójkąt na dwa mniejsze trójkąty prostokątne podobne (cecha KK):
$$\frac{h}{x} = \frac{y}{h} \implies h^2 = x \cdot y$$
$$h^2 = 4 \cdot 9 = 36 \implies h = 6\text{ cm}$$

**Krok 2: Wyznaczenie przyprostokątnych $a$ i $b$ z twierdzenia Pitagorasa**

$$a = \sqrt{h^2 + x^2} = \sqrt{6^2 + 4^2} = \sqrt{36 + 16} = \sqrt{52} = 2\sqrt{13}\text{ cm}$$
$$b = \sqrt{h^2 + y^2} = \sqrt{6^2 + 9^2} = \sqrt{36 + 81} = \sqrt{117} = 3\sqrt{13}\text{ cm}$$

### Przykład 2: Trójkąty w trapezie utworzone przez przekątne

W trapezie o podstawach $a = 15$ i $b = 9$ przekątne przecinają się w punkcie $S$. Wykaż, że trójkąty oparte na podstawach ($ABS$ i $CDS$) są podobne i wyznacz skalę podobieństwa.

**Krok**

Kąty przy wierzchołkach podstaw są równe jako kąty naprzemianległe przy prostych równoległych (podstawach trapezu), a kąty przy punkcie $S$ są równe jako kąty wierzchołkowe. Z cechy KKK:
$$\Delta ABS \sim \Delta CDS$$
Skala podobieństwa wynosi stosunek długości podstaw:
$$k = \frac{a}{b} = \frac{15}{9} = \frac{5}{3}$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> Pamiętaj o genialnym twierdzeniu: *wysokość opuszczona na przeciwprostokątną jest średnią geometryczną odcinków, na które dzieli przeciwprostokątną* ($h = \sqrt{x \cdot y}$). To rozwiązuje zadanie w 10 sekund!
