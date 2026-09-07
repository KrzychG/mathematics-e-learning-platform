# 6. Długość łuku okręgu i pole wycinka koła

Łuk okręgu i wycinek koła to fragmenty odpowiednio obwodu i pola koła o promieniu $r$, wyznaczone przez kąt środkowy o mierze $\alpha \in (0^\circ, 360^\circ)$.

> **Definicja: Wzory na długość łuku i pole wycinka**
> - **Długość okręgu i pole koła:** $$L = 2\pi r, \qquad P_k = \pi r^2$$
> - **Długość łuku okręgu o kącie środkowym $\alpha$:**
> $$l = \frac{\alpha}{360^\circ} \cdot 2\pi r = \frac{\alpha}{180^\circ} \cdot \pi r$$
> - **Pole wycinka koła o kącie środkowym $\alpha$:**
> $$P_w = \frac{\alpha}{360^\circ} \cdot \pi r^2 = \frac{1}{2} \cdot l \cdot r$$
> - **Pole odcinka koła (część wycinka odcięta cięciwą):**
> $$P_{\text{odc}} = P_w - P_{\Delta} = \frac{\alpha}{360^\circ} \pi r^2 - \frac{1}{2} r^2 \sin\alpha$$

### Przykład 1: Obliczanie długości łuku i pola wycinka

W kole o promieniu $r = 6\text{ cm}$ dany jest kąt środkowy $\alpha = 60^\circ$. Oblicz długość łuku $l$ oraz pole wycinka koła $P_w$.

**Krok 1: Długość łuku**

$$l = \frac{60^\circ}{360^\circ} \cdot 2\pi \cdot 6 = \frac{1}{6} \cdot 12\pi = 2\pi\text{ cm}$$

**Krok 2: Pole wycinka**

$$P_w = \frac{60^\circ}{360^\circ} \cdot \pi \cdot 6^2 = \frac{1}{6} \cdot 36\pi = 6\pi\text{ cm}^2$$
(Można też sprawdzić: $P_w = \frac{1}{2} \cdot l \cdot r = \frac{1}{2} \cdot 2\pi \cdot 6 = 6\pi$)

### Przykład 2: Wyznaczanie kąta środkowego z pola

Pole wycinka koła o promieniu $r = 12$ wynosi $24\pi$. Wyznacz miarę kąta środkowego $\alpha$ odpowiadającego temu wycinkowi.

**Odpowiedź:**

Podstawiamy dane do wzoru na pole wycinka:
$$P_w = \frac{\alpha}{360^\circ} \cdot \pi r^2 \implies 24\pi = \frac{\alpha}{360^\circ} \cdot \pi \cdot 12^2$$
$$24\pi = \frac{\alpha}{360^\circ} \cdot 144\pi \implies 24 = \frac{144}{360} \cdot \alpha$$
$$24 = \frac{2}{5} \cdot \alpha \implies \alpha = 24 \cdot \frac{5}{2} = 60^\circ$$
Kąt środkowy ma miarę $60^\circ$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Pamiętaj o związku $P_w = \frac{1}{2} l r$. Działa on dokładnie jak wzór na pole trójkąta (połowa podstawy razy wysokość), gdzie „podstawą” jest łuk $l$, a „wysokością” promień $r$.
