# 1. Definicje funkcji trygonometrycznych kąta $0^\circ - 180^\circ$

W geometrii i analizie matematycznej funkcje trygonometryczne definiujemy zarówno w trójkącie prostokątnym (dla kątów ostrych $\alpha \in (0^\circ, 90^\circ)$), jak i na płaszczyźnie kartezjańskiej za pomocą punktu leżącego na ramieniu końcowym kąta (dla kątów $\alpha \in \langle 0^\circ, 180^\circ \rangle$).

> **Definicja: Trójkąt prostokątny (kąt ostry $\alpha$)**
> - $\sin\alpha = \frac{a}{c} = \frac{\text{przyprostokątna naprzeciwko } \alpha}{\text{przeciwprostokątna}}$
> - $\cos\alpha = \frac{b}{c} = \frac{\text{przyprostokątna przyległa do } \alpha}{\text{przeciwprostokątna}}$
> - $\text{tg}\,\alpha = \frac{a}{b} = \frac{\text{przyprostokątna naprzeciwko } \alpha}{\text{przyprostokątna przyległa do } \alpha}$

Układ współrzędnych ($\alpha \in \langle 0^\circ, 180^\circ \rangle$)

Dla punktu $P(x, y)$ na ramieniu końcowym kąta i odległości $r = \sqrt{x^2 + y^2} > 0$:

$$\sin\alpha = \frac{y}{r}, \quad \cos\alpha = \frac{x}{r}, \quad \text{tg}\,\alpha = \frac{y}{x} \; (x \neq 0)$$

### Tabela wartości kątów charakterystycznych

| $\alpha$ | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $90^\circ$ | $120^\circ$ | $135^\circ$ | $150^\circ$ | $180^\circ$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\sin\alpha$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{1}{2}$ | $0$ |
| $\cos\alpha$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{\sqrt{2}}{2}$ | $\frac{1}{2}$ | $0$ | $-\frac{1}{2}$ | $-\frac{\sqrt{2}}{2}$ | $-\frac{\sqrt{3}}{2}$ | $-1$ |
| $\text{tg}\,\alpha$ | $0$ | $\frac{\sqrt{3}}{3}$ | $1$ | $\sqrt{3}$ | nie istnieje | $-\sqrt{3}$ | $-1$ | $-\frac{\sqrt{3}}{3}$ | $0$ |

### Przykład 1: Punkt na ramieniu końcowym kąta

Punkt $P(-4, 3)$ leży na ramieniu końcowym kąta $\alpha \in \langle 0^\circ, 180^\circ \rangle$. Wyznacz wartości $\sin\alpha, \cos\alpha$ oraz $\text{tg}\,\alpha$.

**Krok 1: Obliczenie odległości $r$ od początku układu współrzędnych**

$$r = \sqrt{x^2 + y^2} = \sqrt{(-4)^2 + 3^2} = \sqrt{16 + 9} = \sqrt{25} = 5$$

**Krok 2: Wyznaczenie wartości funkcji z definicji**

$$\sin\alpha = \frac{y}{r} = \frac{3}{5}, \qquad \cos\alpha = \frac{x}{r} = \frac{-4}{5} = -\frac{4}{5}, \qquad \text{tg}\,\alpha = \frac{y}{x} = \frac{3}{-4} = -\frac{3}{4}$$

### Przykład 2: Obliczanie wartości wyrażenia algebraicznego

Oblicz wartość liczbową wyrażenia $W = 4 \cdot \cos 60^\circ \cdot \sin 30^\circ + \sqrt{3} \cdot \text{tg}\,30^\circ - \cos 180^\circ$.

**Krok**

Podstawiamy znane wartości z tabeli:
$$W = 4 \cdot \frac{1}{2} \cdot \frac{1}{2} + \sqrt{3} \cdot \frac{\sqrt{3}}{3} - (-1)$$
$$W = 4 \cdot \frac{1}{4} + \frac{3}{3} + 1 = 1 + 1 + 1 = 3$$

> **Wskazówka egzaminacyjna (Zasada znaków w ćwiartkach):**
> W I ćwiartce ($0^\circ < \alpha < 90^\circ$) wszystkie funkcje są **dodatnie**. W II ćwiartce ($90^\circ < \alpha < 180^\circ$) tylko **sinus jest dodatni**, a cosinus i tangens przyjmują wartości **ujemne**!
