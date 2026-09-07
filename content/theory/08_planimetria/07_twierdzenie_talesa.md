# 7. Twierdzenie Talesa

**Twierdzenie Talesa** to jedno z fundamentalnych twierdzeń geometrii euklidesowej. Mówi ono o proporcjonalności odcinków wyciętych na ramionach kąta przez proste równoległe.

> **Definicja: Treść twierdzenia Talesa**
> Jeżeli ramiona kąta o wierzchołku $A$ przetniemy dwiema prostymi równoległymi $k \parallel l$, które przecinają jedno ramię w punktach $B, C$, a drugie ramię w punktach $D, E$, to:
>
> $$\frac{|AB|}{|BC|} = \frac{|AD|}{|DE|} \qquad \text{oraz} \qquad \frac{|AB|}{|AC|} = \frac{|AD|}{|AE|}$$
>
> **Wniosek (odcinki na prostych równoległych z podobieństwa):**
>
> $$\frac{|BD|}{|CE|} = \frac{|AB|}{|AC|} = \frac{|AD|}{|AE|}$$

### Przykład 1: Odcinki na ramionach kąta

Ramiona kąta przecięto prostymi równoległymi. Na jednym ramieniu proste wycięły odcinki $|AB| = 6$ oraz $|BC| = 9$. Na drugim ramieniu odpowiadający pierwszy odcinek ma długość $|AD| = 4$. Oblicz długość odcinka $|DE|$.

**Odpowiedź:**

Układamy proporcję z twierdzenia Talesa:
$$\frac{|AB|}{|BC|} = \frac{|AD|}{|DE|} \implies \frac{6}{9} = \frac{4}{|DE|}$$
$$6 \cdot |DE| = 9 \cdot 4 \implies 6 \cdot |DE| = 36 \implies |DE| = 6$$
Długość odcinka wynosi $|DE| = 6$.

### Przykład 2: Długość odcinka na prostej równoległej (Częsta pułapka)

W trójkącie $ACE$ poprowadzono prostą równoległą do boku $CE$, która przecina bok $AC$ w punkcie $B$, a bok $AE$ w punkcie $D$. Wiadomo, że $|AB| = 8$, $|BC| = 4$ oraz $|CE| = 15$. Oblicz długość odcinka $|BD|$.

**Krok 1: Wyznaczenie długości całego boku $|AC|$**

$$|AC| = |AB| + |BC| = 8 + 4 = 12$$

**Krok 2: Ułożenie właściwej proporcji z podobieństwa trójkątów $ABD$ i $ACE$**

$$\frac{|BD|}{|CE|} = \frac{|AB|}{|AC|} \implies \frac{|BD|}{15} = \frac{8}{12} = \frac{2}{3}$$
$$|BD| = 15 \cdot \frac{2}{3} = 10$$
**Odpowiedź:** Długość odcinka wynosi $|BD| = 10$.

> **Wskazówka egzaminacyjna (Uważaj na pułapkę):**
> Licząc odcinek leżący **na prostej równoległej** (np. $|BD|$), nie możesz ułożyć proporcji $\frac{|BD|}{|CE|} = \frac{|AB|}{|BC|}$! Musisz zawsze odnieść go do **całego boku trójkąta** $\frac{|AB|}{|AC|}$, ponieważ odcinek równoległy tworzy trójkąt podobny do trójkąta wyjściowego.
