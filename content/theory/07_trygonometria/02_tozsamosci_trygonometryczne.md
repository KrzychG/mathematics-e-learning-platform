# 2. Tożsamości trygonometryczne i wzory redukcyjne

Tożsamości trygonometryczne to równości prawdziwe dla każdego kąta z dziedziny. Pozwalają one upraszczać skomplikowane wyrażenia oraz wyznaczać wartości pozostałych funkcji, gdy znamy tylko jedną z nich.

> **Definicja: Podstawowe tożsamości trygonometryczne**
> - **Jedynka trygonometryczna:** $$\sin^2\alpha + \cos^2\alpha = 1 \implies \sin^2\alpha = 1 - \cos^2\alpha, \quad \cos^2\alpha = 1 - \sin^2\alpha$$
> - **Związek tangensa z sinusem i cosinusem:** $$\text{tg}\,\alpha = \frac{\sin\alpha}{\cos\alpha} \quad (\text{dla } \alpha \neq 90^\circ)$$
> - **Wzory redukcyjne dla kątów rozwartych $(180^\circ - \alpha)$:**
> $$\sin(180^\circ - \alpha) = \sin\alpha, \qquad \cos(180^\circ - \alpha) = -\cos\alpha, \qquad \text{tg}(180^\circ - \alpha) = -\text{tg}\,\alpha$$

### Przykład 1: Wyznaczanie funkcji dla kąta rozwartego

Kąt $\alpha$ jest rozwarty ($\alpha \in (90^\circ, 180^\circ)$) oraz $\sin\alpha = \frac{5}{13}$. Oblicz wartości $\cos\alpha$ oraz $\text{tg}\,\alpha$.

**Krok 1: Wyznaczenie $\cos^2\alpha$ z jedynki trygonometrycznej**

$$\cos^2\alpha = 1 - \sin^2\alpha = 1 - \left(\frac{5}{13}\right)^2 = 1 - \frac{25}{169} = \frac{144}{169}$$

**Krok 2: Wybór znaku cosinusa**

Ponieważ kąt $\alpha$ jest rozwarty ($\alpha \in (90^\circ, 180^\circ)$), jego cosinus jest **ujemny**:
$$\cos\alpha = -\sqrt{\frac{144}{169}} = -\frac{12}{13}$$

**Krok 3: Obliczenie tangensa**

$$\text{tg}\,\alpha = \frac{\sin\alpha}{\cos\alpha} = \frac{\frac{5}{13}}{-\frac{12}{13}} = -\frac{5}{12}$$

### Przykład 2: Zastosowanie wzorów redukcyjnych

Oblicz dokładną wartość wyrażenia $W = \sin 150^\circ - \cos 120^\circ + \text{tg}\,135^\circ$.

**Krok**

Korzystamy ze wzorów redukcyjnych:

$\sin 150^\circ = \sin(180^\circ - 30^\circ) = \sin 30^\circ = \frac{1}{2}$
$\cos 120^\circ = \cos(180^\circ - 60^\circ) = -\cos 60^\circ = -\frac{1}{2}$
$\text{tg}\,135^\circ = \text{tg}(180^\circ - 45^\circ) = -\text{tg}\,45^\circ = -1$

Podstawiając do wyrażenia:
$$W = \frac{1}{2} - \left(-\frac{1}{2}\right) + (-1) = \frac{1}{2} + \frac{1}{2} - 1 = 0$$

> **Wskazówka egzaminacyjna (Złota zasada egzaminacyjna):**
> Rozwiązując równanie $\cos^2\alpha = k$ lub $\sin^2\alpha = k$, zawsze sprawdzaj informację o przedziale kąta $\alpha$. Zapomnienie o znaku minus przy cosinusie w kącie rozwartym to najczęstsza przyczyna utraty punktów!
