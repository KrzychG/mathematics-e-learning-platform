# 3. Statystyka opisowa – średnia arytmetyczna i średnia ważona

Miary tendencji centralnej pozwalają scharakteryzować cały zbiór danych liczbowych za pomocą jednej typowej wartości reprezentatywnej.

> **Definicja: Średnia arytmetyczna ($\bar{x}$)**
> Iloraz sumy wszystkich wartości przez ich liczbę $n$:
>
> $$\bar{x} = \frac{x_1 + x_2 + \dots + x_n}{n}$$
>
> **Z tabeli liczebności:** $$\bar{x} = \frac{n_1 x_1 + n_2 x_2 + \dots + n_k x_k}{n_1 + n_2 + \dots + n_k}$$

Średnia ważona ($\bar{x}_w$)

Uwzględnia różną wagę (znaczenie $w_i > 0$) poszczególnych elementów:

$$\bar{x}_w = \frac{w_1 x_1 + w_2 x_2 + \dots + w_k x_k}{w_1 + w_2 + \dots + w_k}$$

### Przykład 1: Wyznaczanie brakującej wartości z danej średniej

Średnia arytmetyczna zestawu sześciu liczb: $3, 8, 5, x, 11, 7$ wynosi $7$. Wyznacz wartość liczby $x$.

**Odpowiedź:**

Układamy równanie na podstawie definicji średniej dla $n = 6$:
$$\bar{x} = \frac{3 + 8 + 5 + x + 11 + 7}{6} \implies 7 = \frac{34 + x}{6}$$
$$7 \cdot 6 = 34 + x \implies 42 = 34 + x \implies x = 42 - 34 = 8$$
Szukana liczba to $x = 8$.

### Przykład 2: Obliczanie średniej ważonej ocen

Uczeń otrzymał z matematyki oceny: ze sprawdzianu $4$ (waga $3$), z kartkówki $5$ (waga $2$) oraz z odpowiedzi ustnej $3$ (waga $1$). Oblicz jego ocenę semestralną jako średnią ważoną.

**Odpowiedź:**

Podstawiamy oceny i ich wagi do wzoru:
$$\bar{x}_w = \frac{3 \cdot 4 + 2 \cdot 5 + 1 \cdot 3}{3 + 2 + 1} = \frac{12 + 10 + 3}{6} = \frac{25}{6} \approx 4{,}17$$
Średnia ważona wynosi $\frac{25}{6} \approx 4{,}17$.

> **Wskazówka egzaminacyjna (Wskazówka):**
> Pamiętaj, że w mianowniku średniej ważonej stoi **suma wag** ($w_1 + w_2 + \dots$), a nie liczba ocen!
