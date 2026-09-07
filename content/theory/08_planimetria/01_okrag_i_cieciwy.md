# 1. Okrąg i cięciwy – promienie, średnice i styczne

**Okrąg** $o(S, r)$ to zbiór wszystkich punktów płaszczyzny oddalonych od środka $S$ o stałą odległość $r$ (promień). Najdłuższą cięciwą okręgu jest **średnica** $d = 2r$, która przechodzi przez środek okręgu.

> **Definicja: Kluczowe twierdzenia o okręgu i stycznej**
> - **Prostopadłość promienia i stycznej:** Styczna do okręgu jest **prostopadła** do promienia poprowadzonego do punktu styczności ($r \perp k$).
> - **Twierdzenie o odcinkach stycznych:** Jeśli z punktu $P$ leżącego na zewnątrz okręgu poprowadzimy dwie proste styczne do okręgu w punktach $A$ i $B$, to odcinki stycznych są równe:
> $$|PA| = |PB|$$
> - **Zależność w cięciwie:** Promień prostopadły do cięciwy dzieli ją na dwie równe części. W trójkącie prostokątnym o bokach: odległość środka od cięciwy ($d$), połowa cięciwy ($\frac{c}{2}$) i promień ($r$):
> $$r^2 = d^2 + \left(\frac{c}{2}\right)^2$$

### Przykład 1: Odległość cięciwy od środka okręgu

W okręgu o promieniu $r = 10\text{ cm}$ poprowadzono cięciwę o długości $c = 16\text{ cm}$. Oblicz odległość $d$ tej cięciwy od środka okręgu.

**Krok 1: Wyznaczenie połowy długości cięciwy**

$$\frac{c}{2} = \frac{16}{2} = 8\text{ cm}$$

**Krok 2: Zastosowanie twierdzenia Pitagorasa**

$$r^2 = d^2 + \left(\frac{c}{2}\right)^2 \implies 10^2 = d^2 + 8^2 \implies 100 = d^2 + 64$$
$$d^2 = 36 \implies d = 6\text{ cm}$$
**Odpowiedź:** Odległość cięciwy od środka okręgu wynosi $6\text{ cm}$.

### Przykład 2: Długość odcinka stycznej

Z punktu $P$ leżącego na zewnątrz okręgu o promieniu $r = 5$ poprowadzono styczną do okręgu w punkcie $A$. Odległość punktu $P$ od środka okręgu $S$ wynosi $|SP| = 13$. Oblicz długość odcinka stycznej $|PA|$.

**Odpowiedź:**

Promień $SA$ jest prostopadły do stycznej $PA$ w punkcie $A$, zatem trójkąt $SAP$ jest prostokątny z kątem prostym przy wierzchołku $A$:
$$|PA|^2 + r^2 = |SP|^2 \implies |PA|^2 + 5^2 = 13^2$$
$$|PA|^2 + 25 = 169 \implies |PA|^2 = 144 \implies |PA| = 12$$
Długość odcinka stycznej wynosi $12$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Gdy w zadaniu pojawia się słowo „styczna”, natychmiast połącz środek okręgu z punktem styczności i zaznacz kąt prosty ($90^\circ$). To niemal zawsze klucz do utworzenia trójkąta prostokątnego i zastosowania twierdzenia Pitagorasa!
