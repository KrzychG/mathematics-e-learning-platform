# 2. Klasyfikacja trójkątów i twierdzenie odwrotne do tw. Pitagorasa

Rodzaj trójkąta ze względu na miary kątów wewnętrznych można jednoznacznie określić znając wyłącznie długości jego trzech boków $a \le b \le c$ (gdzie $c$ jest bokiem najdłuższym).

> **Definicja: Kryterium klasyfikacji kątowej (dla najdłuższego boku $c$)**
> - **Trójkąt ostrokątny:** $$a^2 + b^2 > c^2$$ (wszystkie trzy kąty wewnętrzne są ostre, mniejsze niż $90^\circ$).
> - **Trójkąt prostokątny (twierdzenie odwrotne do tw. Pitagorasa):** $$a^2 + b^2 = c^2$$ (kąt leżący naprzeciwko boku $c$ ma miarę dokładnie $90^\circ$).
> - **Trójkąt rozwartokątny:** $$a^2 + b^2 < c^2$$ (kąt leżący naprzeciwko boku $c$ ma miarę większą niż $90^\circ$).

Twierdzenie o relacji bok – kąt:

W dowolnym trójkącie

naprzeciw większego kąta wewnętrznego leży dłuższy bok

(i odwrotnie: naprzeciw dłuższego boku leży kąt o większej mierze).

### Przykład 1: Badanie rodzaju trójkąta na podstawie boków

Określ rodzaj trójkąta (ostrokątny, prostokątny czy rozwartokątny) o bokach długości:

**a) Boki: $5, 7, 8$ (najdłuższy bok to $c = 8$):**

$$a^2 + b^2 = 5^2 + 7^2 = 25 + 49 = 74$$
$$c^2 = 8^2 = 64$$
Ponieważ $74 > 64$ ($a^2 + b^2 > c^2$), trójkąt jest **ostrokątny**.

**b) Boki: $4, 6, 9$ (najdłuższy bok to $c = 9$):**

$$a^2 + b^2 = 4^2 + 6^2 = 16 + 36 = 52$$
$$c^2 = 9^2 = 81$$
Ponieważ $52 < 81$ ($a^2 + b^2 < c^2$), trójkąt jest **rozwartokątny**.

### Przykład 2: Relacja między kątami a bokami

W trójkącie $ABC$ kąty przy wierzchołkach $A$ i $B$ mają miary odpowiednio $\alpha = 45^\circ$ oraz $\beta = 70^\circ$. Uszereguj boki $a = |BC|, b = |AC|, c = |AB|$ od najkrótszego do najdłuższego.

**Krok 1: Wyznaczenie miary trzeciego kąta $\gamma$**

$$\gamma = 180^\circ - (45^\circ + 70^\circ) = 180^\circ - 115^\circ = 65^\circ$$

**Krok 2: Uszeregowanie kątów i odpowiadających im boków**

$$\alpha = 45^\circ < \gamma = 65^\circ < \beta = 70^\circ$$
Z twierdzenia o relacji bok-kąt wynika, że:
$$a < c < b$$
**Odpowiedź:** Najkrótszym bokiem jest $a$, a najdłuższym $b$.

> **Wskazówka egzaminacyjna (Pamiętaj o nierówności trójkąta!):**
> Zanim porównasz kwadraty boków, zawsze upewnij się, że trójkąt w ogóle istnieje ($a + b > c$). Na przykład boki $2, 3, 6$ nie tworzą trójkąta, bo $2 + 3 = 5 < 6$!
