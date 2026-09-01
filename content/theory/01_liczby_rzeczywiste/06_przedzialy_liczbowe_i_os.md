# 6. Przedziały liczbowe i oś liczbowa

**Przedział liczbowy** to spójny podzbiór zbioru liczb rzeczywistych $\mathbb{R}$. Przedziały mogą być ograniczone (otwarte, domknięte, lewo- lub prawostronnie domknięte) lub nieograniczone. Na przedziałach wykonujemy podstawowe operacje teoriomnogościowe: sumę ($\cup$), część wspólną / iloczyn ($\cap$) oraz różnicę zbiorów ($\setminus$).

> **Definicja: Rodzaje przedziałów i operacje**
> $$\langle a, b \rangle = \{x \in \mathbb{R}: a \le x \le b\}, \qquad (a, b) = \{x \in \mathbb{R}: a < x < b\}$$
> $$(-\infty, b\rangle = \{x \in \mathbb{R}: x \le b\}, \qquad (a, +\infty) = \{x \in \mathbb{R}: x > a\}$$
>
> - **Suma $A \cup B$:** elementy należące do zbioru $A$ LUB do zbioru $B$.
> - **Część wspólna $A \cap B$:** elementy należące jednocześnie do zbioru $A$ I do zbioru $B$.
> - **Różnica $A \setminus B$:** elementy należące do zbioru $A$ i NIENALEŻĄCE do zbioru $B$.

### Przykład 1: Działania na przedziałach liczbowych

Dane są przedziały $A = \langle -3, 4)$ oraz $B = (1, 6\rangle$. Wyznacz zbiory: $A \cup B$, $A \cap B$, $A \setminus B$ oraz $B \setminus A$.

**Krok 1: Suma i iloczyn**

$$A \cup B = \langle -3, 6\rangle$$
$$A \cap B = (1, 4)$$

**Krok 2: Różnice zbiorów**

$$A \setminus B = \langle -3, 1\rangle \quad \text{(liczba } 1 \notin B\text{, więc pozostaje w } A\setminus B\text{)}$$
$$B \setminus A = \langle 4, 6\rangle \quad \text{(liczba } 4 \notin A\text{, więc pozostaje w } B\setminus A\text{)}$$

### Przykład 2: Zapisywanie warunku z osi liczbowej

Wyznacz wszystkie liczby całkowite należące do zbioru $C = A \cap B$, gdzie $A = (-2, 5\rangle$ oraz $B = \langle 0, 7)$.

**Krok 1: Wyznaczenie części wspólnej**

$$C = A \cap B = \langle 0, 5\rangle$$

**Krok 2: Wypisanie liczb całkowitych**

Liczby całkowite $x \in \mathbb{Z}$ spełniające $0 \le x \le 5$ to:
$$\{0, 1, 2, 3, 4, 5\}$$
**Odpowiedź:** Do zbioru należy $6$ liczb całkowitych: $0, 1, 2, 3, 4, 5$.

> **Wskazówka egzaminacyjna:**
> Najwięcej błędów dotyczy domknięcia na krańcach przy różnicy zbiorów! Jeśli odejmujesz przedział otwarty w punkcie $x = a$ (np. $B = (1, 6\rangle$), to liczba $1$ NIE jest odejmowana i w wyniku różnicy $A \setminus B$ punkt ten musi być **domknięty**: $\langle -3, 1\rangle$!
