# 1. Zliczanie obiektów w prostych sytuacjach kombinatorycznych

Kombinatoryka to dział matematyki zajmujący się wyznaczaniem liczby elementów skończonych zbiorów oraz liczby możliwych układów (konfiguracji) spełniających określone warunki.

> **Definicja: Metody zliczania w prostych układach**
> - **Systematyczne wypisywanie:** Tworzenie uporządkowanej listy wszystkich możliwości (np. par liczb, ciągów wyników) w kolejności rosnącej lub alfabetycznej (leksykograficznej).
> - **Tabela dwuwymiarowa:** Szczególnie przydatna dla doświadczeń dwuetapowych (np. rzut dwoma kostkami sześciennymi – tabela $6 \times 6 = 36$ par wyników).
> - **Drzewo stochastyczne / decyzyjne:** Rozgałęzienia na każdym etapie prezentują kolejne wybory; liczba wszystkich gałęzi końcowych to liczba możliwych układów.

### Przykład 1: Rzut dwiema kostkami do gry

Rzucamy dwukrotnie symetryczną sześcienną kostką do gry. Ile jest par wyników $(a, b)$, dla których suma wyrzuconych oczek jest liczbą pierwszą większą od $6$?

**Krok 1: Identyfikacja możliwych sum**

Suma oczek na dwóch kostkach wynosi od $2$ do $12$. Liczby pierwsze w tym zakresie to $2, 3, 5, 7, 11$.
Liczby pierwsze większe od $6$ to wyłącznie: **$7$ oraz $11$**.

**Krok 2: Wypisanie par sprzyjających**

Suma równa $7$: $(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)$ – $6$ możliwości.
Suma równa $11$: $(5, 6), (6, 5)$ – $2$ możliwości.

**Krok 3: Podsumowanie**

Łączna liczba par wynosi $6 + 2 = 8$.

### Przykład 2: Zliczanie przekątnych i uścisków dłoni

Na spotkaniu $7$ osób każda przywitała się z każdą dokładnie jeden raz przez uścisk dłoni. Ile uścisków dłoni wymieniono?

**Krok**

Każda z $7$ osób wita się z pozostałymi $6$ osobami ($7 \cdot 6 = 42$). Ponieważ uścisk dłoni między osobą A i B to to samo powitanie co między B i A, wynik dzielimy przez $2$:
$$\text{Liczba uścisków} = \frac{7 \cdot 6}{2} = 21$$

> **Wskazówka egzaminacyjna (Wskazówka):**
> W prostych zadaniach kombinatorycznych wypisanie wszystkich możliwości na brudnopisie jest pewną i bezbłędną metodą. Zwracaj uwagę, czy kolejność elementów ma znaczenie (np. para $(1, 6)$ to inny wynik niż $(6, 1)$).
