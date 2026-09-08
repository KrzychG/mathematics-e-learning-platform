# 5. Przekształcenia geometryczne w układzie współrzędnych

W geometrii analitycznej najczęściej stosowanymi izometriami (przekształceniami zachowującymi odległości i kształty) są symetrie względem osi układu współrzędnych oraz symetria środkowa względem początku układu $O(0, 0)$.

> **Definicja: Reguły przekształcania współrzędnych punktu $P(x, y)$**
> - **Symetria względem osi $OX$ ($S_{OX}$):** Zmienia się wyłącznie znak rzędnej ($y$):
> $$(x, y) \xrightarrow{S_{OX}} (x, -y)$$
> - **Symetria względem osi $OY$ ($S_{OY}$):** Zmienia się wyłącznie znak odciętej ($x$):
> $$(x, y) \xrightarrow{S_{OY}} (-x, y)$$
> - **Symetria środkowa względem początku układu $O(0, 0)$ ($S_O$):** Zmieniają się znaki obu współrzędnych:
> $$(x, y) \xrightarrow{S_O} (-x, -y)$$

### Przykład 1: Obraz trójkąta w symetrii osiowej

Trójkąt $ABC$ ma wierzchołki $A(-2, 3)$, $B(4, 1)$ oraz $C(1, -5)$. Wyznacz współrzędne wierzchołków trójkąta $A'B'C'$ będącego obrazem trójkąta $ABC$ w symetrii względem osi $OY$.

**Krok**

W symetrii względem osi $OY$ zmieniamy znak pierwszej współrzędnej ($x \to -x$):

$A(-2, 3) \xrightarrow{S_{OY}} A'(-(-2), 3) = A'(2, 3)$
$B(4, 1) \xrightarrow{S_{OY}} B'(-4, 1)$
$C(1, -5) \xrightarrow{S_{OY}} C'(-1, -5)$

### Przykład 2: Obraz okręgu w symetrii środkowej

Dany jest okrąg o równaniu $(x - 4)^2 + (y + 1)^2 = 16$. Napisz równanie okręgu będącego jego obrazem w symetrii środkowej względem początku układu współrzędnych $O(0, 0)$.

**Krok 1: Wyznaczenie środka i promienia okręgu wyjściowego**

Środkiem okręgu jest punkt $S(4, -1)$, a jego promień to $r = \sqrt{16} = 4$.

**Krok 2: Przekształcenie środka okręgu w symetrii względem $(0, 0)$**

$$S(4, -1) \xrightarrow{S_O} S'(-4, -(-1)) = S'(-4, 1)$$
Promień okręgu w symetrii środkowej pozostaje bez zmian ($r' = 4$).

**Krok 3: Zapisanie równania nowego okręgu**

$$(x - (-4))^2 + (y - 1)^2 = 16 \implies (x + 4)^2 + (y - 1)^2 = 16$$

> **Wskazówka egzaminacyjna (Pamiętaj):**
> Symetria osiowa i środkowa to przekształcenia izometryczne – figury nie zmieniają swoich rozmiarów ani pól, zmienia się jedynie ich położenie na płaszczyźnie.
