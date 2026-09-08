# 12. Zastosowanie trygonometrii w figurach płaskich

Połączenie wiedzy planimetrycznej z trygonometrią pozwala na błyskawiczne wyznaczanie pól figur oraz długości odcinków bez konieczności mozolnego wyznaczania wysokości.

> **Definicja: Zestawienie trygonometrycznych wzorów na pola figur**
> - **Trójkąt (dwa boki i kąt między nimi):** $$P = \frac{1}{2} \cdot a \cdot b \cdot \sin\gamma$$
> - **Równoległobok (dwa sąsiednie boki i kąt między nimi):** $$P = a \cdot b \cdot \sin\alpha$$
> - **Romb (bok $a$ i kąt ostry/rozwarty $\alpha$):** $$P = a^2 \cdot \sin\alpha$$
> - **Dowolny czworokąt wypukły (przekątne $d_1, d_2$ i kąt $\varphi$ między nimi):**
> $$P = \frac{1}{2} \cdot d_1 \cdot d_2 \cdot \sin\varphi$$
> - **Związki z promieniami okręgów dla trójkąta:**
> $$P = \frac{a \cdot b \cdot c}{4R} \iff R = \frac{abc}{4P}, \qquad P = p \cdot r \iff r = \frac{P}{p}$$
> (gdzie $p = \frac{a+b+c}{2}$ to połowa obwodu trójkąta)

### Przykład 1: Pole równoległoboku o kącie rozwartym

Boki równoległoboku mają długości $a = 6\text{ cm}$ oraz $b = 10\text{ cm}$, a jeden z jego kątów ma miarę $\alpha = 120^\circ$. Oblicz pole powierzchni tego równoległoboku.

**Krok 1: Wyznaczenie $\sin 120^\circ$ ze wzoru redukcyjnego**

$$\sin 120^\circ = \sin(180^\circ - 60^\circ) = \sin 60^\circ = \frac{\sqrt{3}}{2}$$

**Krok 2: Obliczenie pola**

$$P = a \cdot b \cdot \sin 120^\circ = 6 \cdot 10 \cdot \frac{\sqrt{3}}{2} = 60 \cdot \frac{\sqrt{3}}{2} = 30\sqrt{3}\text{ cm}^2$$

### Przykład 2: Pole czworokąta o zadanych przekątnych

Przekątne czworokąta wypukłego mają długości $d_1 = 8\text{ cm}$ oraz $d_2 = 14\text{ cm}$, a kąt ostry przecięcia tych przekątnych wynosi $\varphi = 30^\circ$. Oblicz pole tego czworokąta.

**Odpowiedź:**

Stosujemy uniwersalny wzór na pole czworokąta z przekątnych:
$$P = \frac{1}{2} \cdot d_1 \cdot d_2 \cdot \sin\varphi = \frac{1}{2} \cdot 8 \cdot 14 \cdot \sin 30^\circ$$
$$P = 56 \cdot \frac{1}{2} = 28\text{ cm}^2$$
Pole czworokąta wynosi $28\text{ cm}^2$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Ponieważ $\sin(180^\circ - \alpha) = \sin\alpha$, sinus kąta ostrego i sinus kąta rozwartego w równoległoboku lub trójkącie mają **dokładnie tę samą wartość** (np. $\sin 60^\circ = \sin 120^\circ = \frac{\sqrt{3}}{2}$). Nie ma więc znaczenia, który z kątów podstawisz do wzoru na pole!
