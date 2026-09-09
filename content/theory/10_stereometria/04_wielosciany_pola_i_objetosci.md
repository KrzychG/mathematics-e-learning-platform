# 4. Graniastosłupy i ostrosłupy – pola i objętości

Wielościany to bryły ograniczone wielokątami (ścianami). Kluczem do obliczenia pola i objętości jest poprawne wyznaczenie pola podstawy $P_p$ oraz wysokości bryły $H$.

> **Definicja: Graniastosłupy ($V = P_p \cdot H$)**
> - Pole całkowite: $$P_c = 2P_p + P_b$$
> - **Prostopadłościan ($a \times b \times c$):**
> $$V = abc, \quad P_c = 2(ab + bc + ac), \quad D = \sqrt{a^2 + b^2 + c^2}$$
> - **Sześcian (krawędź $a$):**
> $$V = a^3, \quad P_c = 6a^2, \quad D = a\sqrt{3}$$

Ostrosłupy ($V = \frac{1}{3} P_p \cdot H$)

- Pole całkowite: $$P_c = P_p + P_b$$
- **Czworościan foremny (krawędź $a$):**
$$P_c = a^2\sqrt{3}, \quad H = \frac{a\sqrt{6}}{3}, \quad V = \frac{a^3\sqrt{2}}{12}$$

### Przykład 1: Graniastosłup prawidłowy trójkątny

W graniastosłupie prawidłowym trójkątnym krawędź podstawy ma długość $a = 6$, a przekątna ściany bocznej tworzy z krawędzią podstawy kąt $60^\circ$. Oblicz objętość tego graniastosłupa.

**Krok 1: Obliczenie pola podstawy (trójkąt równoboczny)**

$$P_p = \frac{a^2\sqrt{3}}{4} = \frac{6^2\sqrt{3}}{4} = \frac{36\sqrt{3}}{4} = 9\sqrt{3}$$

**Krok 2: Wyznaczenie wysokości graniastosłupa $H$ z tangensa w ścianie bocznej**

$$\text{tg}\,60^\circ = \frac{H}{a} \implies \sqrt{3} = \frac{H}{6} \implies H = 6\sqrt{3}$$

**Krok 3: Obliczenie objętości bryły**

$$V = P_p \cdot H = 9\sqrt{3} \cdot 6\sqrt{3} = 54 \cdot 3 = 162$$

### Przykład 2: Objętość ostrosłupa prawidłowego czworokątnego

Krawędź podstawy ostrosłupa prawidłowego czworokątnego ma długość $a = 8$, a krawędź boczna wynosi $b = 2\sqrt{17}$. Oblicz objętość tego ostrosłupa.

**Krok 1: Promień okręgu opisanego na podstawie (połowa przekątnej kwadratu)**

$$d = a\sqrt{2} = 8\sqrt{2} \implies R = \frac{d}{2} = 4\sqrt{2}$$

**Krok 2: Wyznaczenie wysokości ostrosłupa $H$ z twierdzenia Pitagorasa**

$$H^2 + R^2 = b^2 \implies H^2 + (4\sqrt{2})^2 = (2\sqrt{17})^2$$
$$H^2 + 32 = 68 \implies H^2 = 36 \implies H = 6$$

**Krok 3: Obliczenie objętości**

$$P_p = a^2 = 8^2 = 64 \implies V = \frac{1}{3} P_p \cdot H = \frac{1}{3} \cdot 64 \cdot 6 = 128$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> Pamiętaj, że słowo „prawidłowy” w nazwie ostrosłupa lub graniastosłupa oznacza, że jego podstawą jest **wielokąt foremny** (trójkąt równoboczny, kwadrat, sześciokąt foremny), a w przypadku ostrosłupa spodek wysokości leży dokładnie w środku tego wielokąta.
