# 3. Badanie monotoniczności ciągów

Ciąg liczbowy $(a_n)$ jest funkcją zmiennej dyskretnej $n \in \mathbb{N}_+$, dlatego jego monotoniczność badamy, porównując dwa sąsiednie wyrazy: wyraz kolejny $a_{n+1}$ oraz wyraz poprzedni $a_n$.

> **Definicja: Kryterium różnicowe monotoniczności**
> Dla każdego $n \in \mathbb{N}_+$ badamy znak różnicy **$a_{n+1} - a_n$**:
>
> - **Ciąg rosnący:** $a_{n+1} - a_n > 0 \iff a_{n+1} > a_n$ (każdy kolejny wyraz jest większy od poprzedniego)
> - **Ciąg malejący:** $a_{n+1} - a_n < 0 \iff a_{n+1} < a_n$ (każdy kolejny wyraz jest mniejszy od poprzedniego)
> - **Ciąg stały:** $a_{n+1} - a_n = 0 \iff a_{n+1} = a_n$ (wszystkie wyrazy są równe)

### Przykład 1: Badanie monotoniczności ciągu liniowego

Zbadaj monotoniczność ciągu o wyrazie ogólnym $a_n = 7 - 3n$.

**Krok 1: Wyznaczenie wyrazu $a_{n+1}$**

$$a_{n+1} = 7 - 3(n + 1) = 7 - 3n - 3 = 4 - 3n$$

**Krok 2: Utworzenie różnicy $a_{n+1} - a_n$**

$$a_{n+1} - a_n = (4 - 3n) - (7 - 3n) = 4 - 3n - 7 + 3n = -3$$

**Krok 3: Ocena znaku różnicy**

Różnica wynosi $-3 < 0$ dla każdego $n \in \mathbb{N}_+$.
**Wniosek:** Ciąg $(a_n)$ jest **malejący**.

### Przykład 2: Badanie monotoniczności ciągu ułamkowego

Wykaż, że ciąg określony wzorem $a_n = \frac{n}{n + 2}$ jest rosnący.

**Krok 1: Wyznaczenie wyrazu $a_{n+1}$**

$$a_{n+1} = \frac{n + 1}{(n + 1) + 2} = \frac{n + 1}{n + 3}$$

**Krok 2: Sprowadzenie różnicy $a_{n+1} - a_n$ do wspólnego mianownika**

$$a_{n+1} - a_n = \frac{n + 1}{n + 3} - \frac{n}{n + 2} = \frac{(n + 1)(n + 2) - n(n + 3)}{(n + 3)(n + 2)}$$
$$= \frac{(n^2 + 3n + 2) - (n^2 + 3n)}{(n + 3)(n + 2)} = \frac{2}{(n + 3)(n + 2)}$$

**Krok 3: Analiza znaku licznika i mianownika**

Dla każdego $n \in \mathbb{N}_+$ ($n \ge 1$):

Licznik $2 > 0$ jest zawsze dodatni,
Mianownik $(n + 3)(n + 2) > 0$ jest iloczynem dwóch liczb dodatnich.

Zatem $\frac{2}{(n + 3)(n + 2)} > 0$ dla każdego $n \in \mathbb{N}_+$.
**Wniosek:** Ciąg $(a_n)$ jest **rosnący**, c.n.d.

> **Wskazówka egzaminacyjna (Częsty błąd):**
> Obliczenie tylko dwóch pierwszych wyrazów (np. $a_1$ i $a_2$) i stwierdzenie, że skoro $a_2 > a_1$, to ciąg jest rosnący, jest **błędem kardynalnym**! Niektóre ciągi rosną na początku, a potem maleją. Prawidłowy dowód zawsze wymaga zbadania znaku ogólnej różnicy $a_{n+1} - a_n$.
