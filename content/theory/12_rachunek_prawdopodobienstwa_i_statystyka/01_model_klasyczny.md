# 1. Doświadczenia losowe i klasyczny model prawdopodobieństwa

**Rachunek prawdopodobieństwa** zajmuje się badaniem zjawisk losowych, czyli takich, których wyniku nie można ze stuprocentową pewnością przewidzieć przed zakończeniem doświadczenia.

> **Definicja: Pojęcia wstępne i model klasyczny**
> - **Przestrzeń zdarzeń elementarnych ($\Omega$):** Zbiór wszystkich możliwych, wzajemnie wykluczających się wyników doświadczenia. Liczbę wszystkich wyników oznaczamy $|\Omega|$.
> - **Zdarzenie losowe ($A$):** Dowolny podzbiór przestrzeni $\Omega$ ($A \subseteq \Omega$). Liczbę wyników sprzyjających zdarzeniu $A$ oznaczamy $|A|$.
> - **Klasyczna definicja prawdopodobieństwa (Laplace'a):** Stosujemy, gdy wszystkie zdarzenia elementarne są **jednakowo prawdopodobne**:
> $$P(A) = \frac{|A|}{|\Omega|}$$

### Przykład 1: Rzut dwiema kostkami sześciennymi

Rzucamy dwiema symetrycznymi sześciennymi kostkami do gry. Oblicz prawdopodobieństwo zdarzenia $A$ polegającego na tym, że suma wyrzuconych oczek jest równa co najmniej $10$.

**Krok 1: Wyznaczenie mocy przestrzeni $|\Omega|$ z reguły mnożenia**

$$|\Omega| = 6 \cdot 6 = 36$$

**Krok 2: Wypisanie wyników sprzyjających zdarzeniu $A$ (suma $\ge 10$)**

Możliwe sumy to: $10, 11, 12$:

Suma $10$: $(4, 6), (5, 5), (6, 4)$ – $3$ zdarzenia
Suma $11$: $(5, 6), (6, 5)$ – $2$ zdarzenia
Suma $12$: $(6, 6)$ – $1$ zdarzenie

Liczba wyników sprzyjających: $|A| = 3 + 2 + 1 = 6$.

**Krok 3: Obliczenie prawdopodobieństwa**

$$P(A) = \frac{|A|}{|\Omega|} = \frac{6}{36} = \frac{1}{6}$$

### Przykład 2: Losowanie kul z urny

W urnie znajduje się $7$ kul białych i $5$ kul czarnych. Losujemy jedną kulę. Oblicz prawdopodobieństwo wylosowania kuli białej.

**Krok**

Łączna liczba kul w urnie wynosi $|\Omega| = 7 + 5 = 12$.
Liczba kul sprzyjających zdarzeniu (białe): $|A| = 7$.

Prawdopodobieństwo wynosi:
$$P(A) = \frac{7}{12}$$

> **Wskazówka egzaminacyjna (Pamiętaj o granicach):**
> Prawdopodobieństwo dowolnego zdarzenia losowego **zawsze mieści się w przedziale $\langle 0, 1 \rangle$**. Jeśli w obliczeniach wyjdzie Ci liczba większa od $1$ lub ujemna, w rozwiązaniu jest błąd!
