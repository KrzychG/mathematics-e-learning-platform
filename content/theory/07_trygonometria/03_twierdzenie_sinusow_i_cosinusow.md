# 3. Twierdzenie sinusów, cosinusów oraz pole trójkąta

Twierdzenia sinusów i cosinusów to kluczowe uogólnienia praw trygonometrii na **dowolne trójkąty** (nie tylko prostokątne!). Umożliwiają obliczenie dowolnego boku, kąta lub promienia okręgu opisanego.

> **Definicja: Twierdzenie sinusów**
> Stosunek długości dowolnego boku do sinusa kąta leżącego naprzeciwko niego jest stały i równy średnicy okręgu opisanego ($2R$):
>
> $$\frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma} = 2R$$

Twierdzenie cosinusów

Kwadrat długości dowolnego boku trójkąta jest równy sumie kwadratów pozostałych boków pomniejszonej o podwojony ich iloczyn i cosinus kąta między nimi:

$$c^2 = a^2 + b^2 - 2ab \cdot \cos\gamma$$

Wzór na pole trójkąta z sinusem:

Pole trójkąta jest równe połowie iloczynu dwóch boków i sinusa kąta zawartego między nimi:
$$P = \frac{1}{2} \cdot a \cdot b \cdot \sin\gamma = \frac{1}{2} \cdot b \cdot c \cdot \sin\alpha = \frac{1}{2} \cdot a \cdot c \cdot \sin\beta$$

### Przykład 1: Twierdzenie cosinusów dla kąta rozwartego

W trójkącie dane są boki $a = 4$ i $b = 6$ oraz kąt między nimi $\gamma = 120^\circ$. Oblicz długość trzeciego boku $c$.

**Krok 1: Wyznaczenie $\cos 120^\circ$**

$$\cos 120^\circ = \cos(180^\circ - 60^\circ) = -\cos 60^\circ = -\frac{1}{2}$$

**Krok 2: Podstawienie do twierdzenia cosinusów**

$$c^2 = a^2 + b^2 - 2ab\cos\gamma = 4^2 + 6^2 - 2 \cdot 4 \cdot 6 \cdot \left(-\frac{1}{2}\right)$$
$$c^2 = 16 + 36 + 24 = 76$$

**Krok 3: Wyznaczenie długości boku $c$**

$$c = \sqrt{76} = \sqrt{4 \cdot 19} = 2\sqrt{19}$$

### Przykład 2: Promień okręgu opisanego i pole trójkąta

W trójkącie bok $a = 6$ leży naprzeciwko kąta $\alpha = 30^\circ$, a bok $b = 10$. Oblicz promień okręgu opisanego $R$ oraz pole trójkąta, jeśli kąt między bokami $a$ i $b$ wynosi $\gamma = 45^\circ$.

**Krok 1: Promień okręgu opisanego z twierdzenia sinusów**

$$\frac{a}{\sin\alpha} = 2R \implies \frac{6}{\sin 30^\circ} = 2R \implies \frac{6}{\frac{1}{2}} = 2R \implies 12 = 2R \implies R = 6$$

**Krok 2: Pole trójkąta**

$$P = \frac{1}{2} \cdot a \cdot b \cdot \sin\gamma = \frac{1}{2} \cdot 6 \cdot 10 \cdot \sin 45^\circ = 30 \cdot \frac{\sqrt{2}}{2} = 15\sqrt{2}$$

> **Wskazówka egzaminacyjna (Jak wybrać właściwe twierdzenie na egzaminie?):**
> • Znasz parę: **bok i kąt naprzeciwko** niego $\implies$ wybierz **twierdzenie sinusów**.
>
> • Znasz **dwa boki i kąt między nimi** lub **trzy boki** $\implies$ wybierz **twierdzenie cosinusów**.
