# 1. Działania w zbiorze liczb rzeczywistych

Zbiór liczb rzeczywistych $\mathbb{R}$ składa się ze zbioru liczb wymiernych $\mathbb{Q}$ (liczb, które można zapisać w postaci ułamka $\frac{p}{q}$, gdzie $p \in \mathbb{Z}$ oraz $q \in \mathbb{Z} \setminus \{0\}$) oraz liczb niewymiernych $\mathbb{IQ}$ (liczb o rozwinięciu dziesiętnym nieskończonym i nieokresowym, np. $\sqrt{2}, \pi$).

> **Definicja: Klasyfikacja podzbiorów liczb rzeczywistych**
> Hierarchia zbiorów liczbowych:
>
> $$\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$$
>
> - $\mathbb{N} = \{0, 1, 2, 3, \dots\}$ – liczby naturalne
> - $\mathbb{Z} = \{\dots, -2, -1, 0, 1, 2, \dots\}$ – liczby całkowite
> - Rozwinięcie dziesiętne liczby wymiernej jest zawsze skończone lub nieskończone okresowe (np. $\frac{1}{3} = 0{,}(3)$).

> **Definicja: Kolejność wykonywania działań**
> 1. Działania w nawiasach (od najbardziej wewnętrznych).
> 2. Potęgowanie, pierwiastkowanie i logarytmowanie.
> 3. Mnożenie i dzielenie (w kolejności występowania od lewej do prawej).
> 4. Dodawanie i odejmowanie (w kolejności występowania od lewej do prawej).

### Przykład 1: Zamiana ułamka okresowego na ułamek zwykły

Przedstaw liczbę $x = 0{,}2(18)$ w postaci ułamka nieskracalnego $\frac{p}{q}$.

**Krok 1: Wypisanie równania i przesunięcie przecinka**

Oznaczmy: $x = 0{,}2181818\dots$

Mnożymy przez $10$, aby przed przecinkiem znalazła się część nieokresowa:
$$10x = 2{,}181818\dots$$
Mnożymy przez $1000$ (okres ma 2 cyfry, więc mnożymy przez $10 \cdot 100$):
$$1000x = 218{,}181818\dots$$

**Krok 2: Odjęcie równań stronami i uproszczenie**

$$1000x - 10x = 218{,}1818\dots - 2{,}1818\dots \implies 990x = 216$$
$$x = \frac{216}{990} = \frac{108}{495} = \frac{12}{55}$$
**Odpowiedź:** Liczba $0{,}2(18)$ jest równa $\frac{12}{55}$.

### Przykład 2: Złożone wyrażenie arytmetyczne

Oblicz wartość wyrażenia: $W = \frac{2{,}5 - \frac{3}{4} \cdot 2}{\left(-\frac{1}{2}\right)^2 + 0{,}75}$.

**Krok 1: Obliczenie licznika**

$$\text{Licznik} = 2{,}5 - \left(\frac{3}{4} \cdot 2\right) = 2{,}5 - \frac{6}{4} = 2{,}5 - 1{,}5 = 1$$

**Krok 2: Obliczenie mianownika i ilorazu**

$$\text{Mianownik} = \left(-\frac{1}{2}\right)^2 + 0{,}75 = \frac{1}{4} + \frac{3}{4} = 1$$
$$W = \frac{1}{1} = 1$$
**Odpowiedź:** Wartość wyrażenia wynosi $1$.

> **Wskazówka egzaminacyjna:**
> Zwracaj szczególną uwagę na znak minus przed nawiasem oraz potęgowanie liczb ujemnych: $(-a)^2 = a^2$, ale $-a^2 = -(a^2)$. Pamiętaj też, że dzielenie przez zero w zbiorze $\mathbb{R}$ jest operacją niedozwoloną!
