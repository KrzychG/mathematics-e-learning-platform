# 5. Równania wymierne

**Równaniem wymiernym** nazywamy równanie, w którym niewiadoma występuje w mianowniku co najmniej jednego ułamka algebraicznego. Pierwszym i bezwzględnie koniecznym krokiem przy rozwiązywaniu równania wymiernego jest ustalenie jego **dziedziny** ($D$), czyli wykluczenie liczb zerujących jakikolwiek mianownik.

> **Definicja: Algorytm rozwiązywania równania wymiernego**
> 1. **Wyznaczenie dziedziny $D$:** przyrównujemy każdy mianownik do zera: $\text{mianownik} \neq 0$.
> 2. **Sprowadzenie do proporcji lub wspólnego mianownika:** dla proporcji $\frac{A}{B} = \frac{C}{D}$ stosujemy mnożenie na krzyż: $A \cdot D = B \cdot C$.
> 3. **Rozwiązanie powstałego równania:** rozwiązujemy równanie liniowe lub kwadratowe.
> 4. **Weryfikacja z dziedziną:** odrzucamy pierwiastki nienależące do dziedziny $D$!

### Przykład 1: Równanie z ułamkiem przyrównanym do zera

Rozwiąż równanie: $\frac{(x - 4)(x + 2)}{x - 4} = 0$.

**Krok 1: Wyznaczenie dziedziny**

Mianownik: $x - 4 \neq 0 \implies x \neq 4$. Zatem $D = \mathbb{R} \setminus \{4\}$.

**Krok 2: Przyrównanie licznika do zera i konfrontacja z $D$**

$$(x - 4)(x + 2) = 0 \implies x = 4 \quad \lor \quad x = -2$$
Sprawdzamy przynależność do $D$:

$x = 4 \notin D$ (odrzucamy – pierwiastek obcy!)
$x = -2 \in D$ (prawidłowe rozwiązanie)

**Odpowiedź:** Jedynym rozwiązaniem równania jest $x = -2$.

### Przykład 2: Równanie wymierne rozwiązywane „na krzyż”

Rozwiąż równanie: $\frac{2x - 3}{x + 1} = \frac{x - 1}{x + 1}$.

**Krok 1: Dziedzina**

$$x + 1 \neq 0 \implies x \neq -1 \implies D = \mathbb{R} \setminus \{-1\}$$

**Krok 2: Mnożenie przez wspólny mianownik $(x + 1)$**

$$2x - 3 = x - 1 \implies 2x - x = -1 + 3 \implies x = 2$$
Ponieważ $2 \in D$, jest to rozwiązanie poprawne.
**Odpowiedź:** Rozwiązaniem równania jest $x = 2$.

> **Wskazówka egzaminacyjna:**
> Zadanie z równania wymiernego, w którym jeden z pierwiastków licznika zeruje mianownik, to absolutny klasyk egzaminacyjny! Zawsze zapisuj dziedzinę na początku. Jeśli pominiesz odrzucenie pierwiastka obcego, otrzymasz 0 punktów za całe zadanie!
