# 4. Statystyka opisowa – mediana i dominanta (moda)

Mediana i dominanta to miary pozycyjne w statystyce opisowej. Są one odporne na obecność wartości skrajnych (nietypowo wysokich lub niskich), które silnie zniekształcają zwykłą średnią arytmetyczną.

> **Definicja: Mediana ($Me$) – Wartość środkowa**
> **Warunek wstępny:** Zestaw danych MUSI być najpierw **uporządkowany niemalejąco** ($x_1 \le x_2 \le \dots \le x_n$):
>
> - Gdy liczba danych $n$ jest **nieparzysta** ($n = 2k + 1$): mediana to dokładnie element środkowy:
> $$Me = x_{k+1}$$
> - Gdy liczba danych $n$ jest **parzysta** ($n = 2k$): mediana to średnia arytmetyczna dwóch wyrazów środkowych:
> $$Me = \frac{x_k + x_{k+1}}{2}$$

Dominanta ($D$ / $Mo$) – Moda

Wartość, która w danym zestawie występuje **najczęściej** (ma największą liczebność).

- Jeśli jedna wartość występuje częściej niż pozostałe $\implies$ mamy jedną dominantę.
- Jeśli wszystkie wartości pojawiają się z tą samą częstością $\implies$ dominanta nie istnieje.

### Przykład 1: Mediana dla parzystej i nieparzystej liczby danych

Wyznacz medianę i dominantę dla następujących zestawów ocen:

**Zestaw A (7 ocen):**

$3, 5, 2, 4, 3, 4, 3$
1. Porządkujemy rosnąco: $2, 3, 3, \mathbf{3}, 4, 4, 5$

2. Liczba elementów $n = 7$ (nieparzysta). Środkowym (czwartym) elementem jest $3$. Zatem:
$$Me = 3$$
Najczęściej (3 razy) występuje ocena $3$, zatem dominanta to:
$$D = 3$$

**Zestaw B (8 czasów w sekundach):**

$12, 15, 10, 18, 14, 16, 11, 14$
1. Porządkujemy rosnąco: $10, 11, 12, \mathbf{14}, \mathbf{14}, 15, 16, 18$

2. Liczba elementów $n = 8$ (parzysta). Środkowe elementy to czwarty ($14$) i piąty ($14$):
$$Me = \frac{14 + 14}{2} = 14$$

### Przykład 2: Mediana z niewiadomą

Dane są liczby w porządku rosnącym: $2, 4, 5, x, 11, 14$. Wiadomo, że mediana tego zestawu wynosi $7$. Wyznacz liczbę $x$.

**Odpowiedź:**

Liczba elementów wynosi $n = 6$ (parzysta). Dwa elementy środkowe to trzeci ($5$) i czwarty ($x$):
$$Me = \frac{5 + x}{2} \implies 7 = \frac{5 + x}{2} \implies 14 = 5 + x \implies x = 9$$
$x = 9$ (warunek uporządkowania $5 \le 9 \le 11$ jest spełniony).

> **Wskazówka egzaminacyjna (Najczęstszy błąd):**
> Liczenie mediany bez wcześniejszego uporządkowania danych! Wybranie liczby stojącej pośrodku w nieuporządkowanym ciągu to gwarantowane zero punktów na egzaminie.
