# 2. Własności prawdopodobieństwa i reguły obliczeń

Zamiast każdorazowo wypisywać wszystkie zdarzenia elementarne, w trudniejszych zadaniach stosujemy aksjomatyczne własności rachunku prawdopodobieństwa lub metodę drzew stochastycznych.

> **Definicja: Kluczowe własności prawdopodobieństwa**
> - **Granice i zdarzenia skrajne:** $$0 \le P(A) \le 1, \qquad P(\Omega) = 1, \qquad P(\emptyset) = 0$$
> - **Zdarzenie przeciwne ($A'$):** Zdarzenie, które zachodzi wtedy i tylko wtedy, gdy NIE zachodzi $A$:
> $$P(A') = 1 - P(A) \iff P(A) = 1 - P(A')$$
> - **Prawdopodobieństwo sumy zdarzeń ($A \cup B$):**
> $$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
> (Dla zdarzeń wykluczających się, gdy $A \cap B = \emptyset$: $P(A \cup B) = P(A) + P(B)$)

### Przykład 1: Zastosowanie zdarzenia przeciwnego („co najmniej raz”)

Rzucamy trzykrotnie symetryczną monetą. Oblicz prawdopodobieństwo zdarzenia $A$ polegającego na tym, że **co najmniej raz** wypadnie orzeł.

**Krok 1: Określenie zdarzenia przeciwnego $A'$**

Zdarzeniem przeciwnym do „co najmniej raz orzeł” jest: „orzeł nie wypadł ani razu” (czyli **same reszki**: $(R, R, R)$).

**Krok 2: Obliczenie prawdopodobieństwa $P(A')$**

Moc przestrzeni: $|\Omega| = 2^3 = 8$.
Zdarzeniu $A'$ sprzyja tylko $1$ wynik: $|A'| = 1$. Zatem:
$$P(A') = \frac{1}{8}$$

**Krok 3: Obliczenie $P(A)$ ze wzoru na zdarzenie przeciwne**

$$P(A) = 1 - P(A') = 1 - \frac{1}{8} = \frac{7}{8}$$

### Przykład 2: Prawdopodobieństwo sumy i iloczynu zdarzeń

Zdarzenia losowe $A, B \subseteq \Omega$ spełniają warunki: $P(A) = 0{,}6$, $P(B) = 0{,}5$ oraz $P(A \cup B) = 0{,}8$. Oblicz prawdopodobieństwo iloczynu tych zdarzeń $P(A \cap B)$.

**Odpowiedź:**

Korzystamy ze wzoru na sumę zdarzeń:
$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$
$$0{,}8 = 0{,}6 + 0{,}5 - P(A \cap B)$$
$$0{,}8 = 1{,}1 - P(A \cap B) \implies P(A \cap B) = 1{,}1 - 0{,}8 = 0{,}3$$
$P(A \cap B) = 0{,}3$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Gdy w treści zadania widzisz słowa: **„co najmniej raz”** lub **„chociaż jeden”**, niemal w 100% przypadków najszybszym i najprostszym sposobem rozwiązania jest przejście do zdarzenia przeciwnego: $P(A) = 1 - P(A')$.
