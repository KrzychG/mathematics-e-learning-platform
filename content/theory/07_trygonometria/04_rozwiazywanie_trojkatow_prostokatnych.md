# 4. Rozwiązywanie trójkątów prostokątnych

**Rozwiązanie trójkąta prostokątnego** polega na wyznaczeniu długości wszystkich jego boków oraz miar wszystkich kątów na podstawie danych wejściowych (zazwyczaj jednego boku i kąta ostrego lub dwóch boków).

> **Definicja: Aparat pojęciowy**
> - Suma kątów ostrych: $$\alpha + \beta = 90^\circ \implies \beta = 90^\circ - \alpha$$
> - Twierdzenie Pitagorasa: $$a^2 + b^2 = c^2$$
> - Funkcje trygonometryczne:
> $$\sin\alpha = \frac{a}{c}, \quad \cos\alpha = \frac{b}{c}, \quad \text{tg}\,\alpha = \frac{a}{b}$$

Trójkąty o kątach szczególnych

- **Kąty $30^\circ, 60^\circ, 90^\circ$ (połowa trójkąta równobocznego):**

Przyprostokątne: $a$ (naprzeciw $30^\circ$), $a\sqrt{3}$ (naprzeciw $60^\circ$), przeciwprostokątna: $2a$.
- **Kąty $45^\circ, 45^\circ, 90^\circ$ (połowa kwadratu):**

Przyprostokątne: $a, a$, przeciwprostokątna: $a\sqrt{2}$.

### Przykład 1: Rozwiązanie trójkąta o znanej przeciwprostokątnej i kącie

W trójkącie prostokątnym przeciwprostokątna ma długość $c = 10$, a jeden z kątów ostrych ma miarę $\alpha = 30^\circ$. Wyznacz długości obu przyprostokątnych oraz miarę drugiego kąta ostrego.

**Krok 1: Wyznaczenie drugiego kąta ostrego $\beta$**

$$\beta = 90^\circ - \alpha = 90^\circ - 30^\circ = 60^\circ$$

**Krok 2: Wyznaczenie przyprostokątnej $a$ leżącej naprzeciw $30^\circ$**

$$\sin 30^\circ = \frac{a}{c} \implies \frac{1}{2} = \frac{a}{10} \implies a = 10 \cdot \frac{1}{2} = 5$$

**Krok 3: Wyznaczenie drugiej przyprostokątnej $b$**

$$\cos 30^\circ = \frac{b}{c} \implies \frac{\sqrt{3}}{2} = \frac{b}{10} \implies b = 10 \cdot \frac{\sqrt{3}}{2} = 5\sqrt{3}$$

### Przykład 2: Zadanie praktyczne (Drabina przy ścianie)

Drabina o długości $5\text{ m}$ jest oparta o pionową ścianę budynku. Podstawa drabiny jest oddalona od ściany o $3\text{ m}$. Wyznacz wysokość, na jaką sięga drabina, oraz cosinus kąta $\alpha$, jaki drabina tworzy z poziomym podłożem.

**Krok 1: Wyznaczenie wysokości ze wzoru Pitagorasa**

Niech $h$ oznacza wysokość sięgania drabiny. Wówczas:
$$h^2 + 3^2 = 5^2 \implies h^2 + 9 = 25 \implies h^2 = 16 \implies h = 4\text{ m}$$

**Krok 2: Wyznaczenie cosinusa kąta nachylenia**

Cosinus to stosunek przyprostokątnej przyległej (odległość od ściany) do przeciwprostokątnej (długość drabiny):
$$\cos\alpha = \frac{3}{5} = 0{,}6$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> W zadaniach z treścią zawsze narysuj prosty szkic sytuacyjny i zaznacz kąt prosty. Zwróć szczególną uwagę, czy w treści mowa o kącie między drabiną a *podłożem* (poziom), czy między drabiną a *ścianą* (pion).
