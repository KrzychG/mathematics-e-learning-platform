# 2. Ciągi określone rekurencyjnie

Ciąg jest zdefiniowany **rekurencyjnie**, jeśli podany jest co najmniej jeden wyraz początkowy (np. $a_1$) oraz reguła (równanie rekurencyjne) pozwalająca obliczyć kolejny wyraz ciągu $a_{n+1}$ na podstawie wyrazu poprzedniego $a_n$ (lub kilku wyrazów poprzednich).

> **Definicja: Struktura wzoru rekurencyjnego**
> $$\begin{cases} a_1 = c \\ a_{n+1} = g(a_n) \quad \text{dla } n \ge 1 \end{cases}$$
>
> Aby obliczyć $k$-ty wyraz ciągu rekurencyjnego, musimy wyznaczyć kolejno wszystkie wyrazy poprzedzające: $a_1 \to a_2 \to a_3 \to \dots \to a_k$.

### Przykład 1: Wyznaczanie kolejnych wyrazów z reguły rekurencyjnej

Ciąg $(a_n)$ określony jest wzorem rekurencyjnym:

$$\begin{cases} a_1 = 4 \\ a_{n+1} = 2a_n - 3 \quad \text{dla } n \ge 1 \end{cases}$$

Oblicz wyrazy $a_2, a_3$ oraz $a_4$.

**Wyraz $a_2$ (dla $n = 1$):**

$$a_2 = 2 \cdot a_1 - 3 = 2 \cdot 4 - 3 = 8 - 3 = 5$$

**Wyraz $a_3$ (dla $n = 2$):**

$$a_3 = 2 \cdot a_2 - 3 = 2 \cdot 5 - 3 = 10 - 3 = 7$$

**Wyraz $a_4$ (dla $n = 3$):**

$$a_4 = 2 \cdot a_3 - 3 = 2 \cdot 7 - 3 = 14 - 3 = 11$$

### Przykład 2: Rekurencja dwuwyrazowa (Ciąg typu Fibonacciego)

Dany jest ciąg $(x_n)$, w którym $x_1 = 2$, $x_2 = 3$ oraz $x_{n+2} = 2x_{n+1} - x_n$ dla $n \ge 1$. Wyznacz $x_4$.

**Krok 1: Wyznaczenie $x_3$ (podstawiamy $n = 1$)**

$$x_3 = 2 \cdot x_2 - x_1 = 2 \cdot 3 - 2 = 6 - 2 = 4$$

**Krok 2: Wyznaczenie $x_4$ (podstawiamy $n = 2$)**

$$x_4 = 2 \cdot x_3 - x_2 = 2 \cdot 4 - 3 = 8 - 3 = 5$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> W zadaniach z ciągami rekurencyjnymi nie ma wzoru, do którego można bezpośrednio podstawić np. $n = 100$. Zawsze obliczaj wyrazy metodycznie krok po kroku i sprawdzaj, czy nie pojawia się powtarzający się cykl lub łatwa do uogólnienia zależność.
