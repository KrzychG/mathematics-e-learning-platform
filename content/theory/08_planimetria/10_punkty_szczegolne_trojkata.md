# 10. Punkty szczególne w trójkącie

W każdym trójkącie wyróżniamy cztery fundamentalne punkty geometryczne wyznaczone przez przecięcie charakterystycznych prostych.

> **Definicja: 1. Środek okręgu opisanego ($S_{op}$)**
> Punkt przecięcia **symetralnych boków** trójkąta. Jest jednakowo oddalony od wszystkich wierzchołków ($|SA| = |SB| = |SC| = R$).
>
> - W trójkącie prostokątnym środek ten leży **dokładnie na środku przeciwprostokątnej**: $$R = \frac{c}{2}$$

2. Środek okręgu wpisanego ($S_{wp}$)

Punkt przecięcia **dwusiecznych kątów wewnętrznych** trójkąta. Jest jednakowo oddalony od wszystkich boków o promień $r$.

- Związek z polem i połową obwodu $p = \frac{a+b+c}{2}$: $$P = p \cdot r$$
- W trójkącie prostokątnym: $$r = \frac{a + b - c}{2}$$

3. Środek ciężkości ($G$)

Punkt przecięcia **środkowych** trójkąta (odcinków łączących wierzchołek ze środkiem przeciwległego boku).

- **Własność 2:1:** Dzieli każdą środkową w stosunku $2:1$, licząc od wierzchołka: $$|AG| = \frac{2}{3} \cdot s_a, \qquad |GA_1| = \frac{1}{3} \cdot s_a$$

4. Ortocentrum ($H$)

Punkt przecięcia prostych zawierających **wysokości** trójkąta.

- W trójkącie prostokątnym ortocentrum leży dokładnie w **wierzchołku kąta prostego**!
- W trójkącie rozwartokątnym leży na zewnątrz trójkąta.

### Przykład 1: Środkowa i podział 2:1

W trójkącie $ABC$ środkowa $CD$ ma długość $18\text{ cm}$. Punkt $S$ jest środkiem ciężkości tego trójkąta. Oblicz długości odcinków $|CS|$ oraz $|SD|$.

**Krok**

Środek ciężkości dzieli środkową na odcinki w stosunku $2:1$, gdzie dłuższy odcinek łączy się z wierzchołkiem $C$:
$$|CS| = \frac{2}{3} \cdot |CD| = \frac{2}{3} \cdot 18 = 12\text{ cm}$$
$$|SD| = \frac{1}{3} \cdot |CD| = \frac{1}{3} \cdot 18 = 6\text{ cm}$$

### Przykład 2: Promień okręgu wpisanego w trójkąt prostokątny

Przyprostokątne trójkąta prostokątnego mają długości $a = 6$ i $b = 8$. Oblicz promień okręgu wpisanego $r$ oraz promień okręgu opisanego $R$.

**Krok 1: Wyznaczenie przeciwprostokątnej $c$**

$$c = \sqrt{a^2 + b^2} = \sqrt{6^2 + 8^2} = \sqrt{36 + 64} = 10$$

**Krok 2: Obliczenie promienia okręgu opisanego $R$**

$$R = \frac{c}{2} = \frac{10}{2} = 5$$

**Krok 3: Obliczenie promienia okręgu wpisanego $r$**

$$r = \frac{a + b - c}{2} = \frac{6 + 8 - 10}{2} = \frac{4}{2} = 2$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> W trójkącie równobocznym wszystkie cztery punkty szczególne (środek okręgu opisanego, wpisanego, środek ciężkości oraz ortocentrum) **pokrywają się w jednym punkcie**!
