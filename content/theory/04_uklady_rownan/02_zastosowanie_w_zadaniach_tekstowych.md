# 2. Zastosowanie układów równań w zadaniach tekstowych

Wiele praktycznych problemów matematycznych (obliczenia handlowe, zadania o wieku, mieszaninach i stężeniach, prędkości, drodze i czasie) wymaga przetłumaczenia treści zadania na język algebry w postaci **układu dwóch równań z dwiema niewiadomymi**.

> **Definicja: Etapy modelowania matematycznego zadania z treścią**
> 1. **Wybór niewiadomych i jednostek:** precyzyjne nazwanie zmiennych (np. niech $x$ oznacza liczbę biletów ulgowych, a $y$ – normalnych).
> 2. **Określenie dziedziny / warunków fizycznych:** np. $x, y \in \mathbb{N}$ (liczba sztuk nie może być ułamkowa ani ujemna).
> 3. **Zapisanie układu równań:** ułożenie dwóch niezależnych związków wynikających z treści.
> 4. **Rozwiązanie układu i weryfikacja z sensem zadania:** sprawdzenie jednostek i zapisanie odpowiedzi słownej.

### Przykład 1: Zadanie o zakupach (bilety do teatru)

Za $5$ biletów normalnych i $3$ ulgowe zapłacono łącznie $260$ zł. Bilet normalny jest o $20$ zł droższy od biletu ulgowego. Oblicz cenę jednego biletu normalnego i jednego ulgowego.

**Krok 1: Oznaczenie zmiennych i ułożenie układu**

Niech $x$ – cena biletu normalnego (w zł), $y$ – cena biletu ulgowego (w zł).

$$\begin{cases} 5x + 3y = 260 \\ x - y = 20 \end{cases}$$

**Krok 2: Rozwiązanie układu przez podstawienie $x = y + 20$**

$$5(y + 20) + 3y = 260 \implies 5y + 100 + 3y = 260$$
$$8y = 160 \implies y = 20 \text{ zł}$$
$$x = 20 + 20 = 40 \text{ zł}$$
**Odpowiedź:** Bilet normalny kosztuje $40$ zł, a bilet ulgowy $20$ zł.

### Przykład 2: Zadanie o liczbach dwucyfrowych

Suma cyfr pewnej liczby dwucyfrowej wynosi $11$. Jeżeli przestawimy cyfry tej liczby, to otrzymamy liczbę o $27$ większą od początkowej. Wyznacz tę liczbę.

**Krok 1: Zapisanie liczby dwucyfrowej w systemie dziesiątkowym**

Niech $d$ – cyfra dziesiątek, $j$ – cyfra jedności ($d, j \in \{1, 2, \dots, 9\}$).

Liczba początkowa: $10d + j$. Liczba po przestawieniu: $10j + d$.

$$\begin{cases} d + j = 11 \\ (10j + d) - (10d + j) = 27 \end{cases}$$

**Krok 2: Rozwiązanie układu**

Upraszczamy drugie równanie: $9j - 9d = 27 \implies j - d = 3$.
$$\begin{cases} j + d = 11 \\ j - d = 3 \end{cases}$$
Dodajemy stronami: $2j = 14 \implies j = 7$, zatem $d = 11 - 7 = 4$.
Liczba to $10 \cdot 4 + 7 = 47$.

**Odpowiedź:** Szukaną liczbą dwucyfrową jest $47$.

> **Wskazówka egzaminacyjna:**
> W zadaniach o liczbach dwucyfrowych najczęstszym błędem jest zapis liczby jako iloczynu $x \cdot y$ zamiast formy pozycyjnej $10x + y$! Zawsze pamiętaj o pełnym sformułowaniu odpowiedzi słownej na końcu zadania.
