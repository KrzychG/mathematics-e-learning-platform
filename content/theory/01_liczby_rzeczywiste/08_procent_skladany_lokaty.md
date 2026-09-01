# 8. Procent składany, lokaty i kredyty

W obliczeniach finansowych kluczową rolę odgrywa **procent składany** – mechanizm, w którym odsetki po każdym okresie rozliczeniowym (kapitalizacji) są dopisywane do kapitału początkowego i pracują na kolejne odsetki w następnych okresach.

> **Definicja: Wzór na procent składany**
> Wysokość kapitału końcowego $K_n$ po $n$ okresach kapitalizacji:
>
> $$K_n = K_0 \cdot \left(1 + \frac{p}{100}\right)^n$$
>
> - $K_0$ – kapitał początkowy wpłacony na lokatę
> - $p$ – stopa procentowa przypadająca na **jeden okres kapitalizacji**
> - $n$ – łączna liczba okresów kapitalizacji w całym czasie trwania lokaty

### Przykład 1: Lokata z kapitalizacją kwartalną

Klient wpłacił do banku $10\,000$ zł na lokatę $2$-letnią o rocznym oprocentowaniu $6\%$ z kapitalizacją kwartalną. Zapisz wyrażenie opisujące kapitał końcowy (przed potrąceniem podatku).

**Krok 1: Wyznaczenie parametrów okresu**

Kapitał początkowy: $K_0 = 10\,000$ zł
Okresy kapitalizacji w roku: $4$ (kwartały). W ciągu $2$ lat: $n = 2 \cdot 4 = 8$ okresów.
Oprocentowanie na jeden kwartał: $p = \frac{6\%}{4} = 1{,}5\% = 0{,}015$.

**Krok 2: Zastosowanie wzoru na procent składany**

$$K_8 = 10\,000 \cdot (1 + 0{,}015)^8 = 10\,000 \cdot (1{,}015)^8$$
**Odpowiedź:** Stan konta po 2 latach wynosi $10\,000 \cdot (1{,}015)^8$ zł.

### Przykład 2: Zmiana procentowa i punkty procentowe

Poparcie dla partii wzrosło z $20\%$ do $25\%$. Oblicz, o ile punktów procentowych oraz o ile procent wzrosło to poparcie.

**Krok 1: Obliczenie wzrostu w punktach procentowych (p.p.)**

$$\Delta_{\text{p.p.}} = 25\% - 20\% = 5\text{ p.p.}$$

**Krok 2: Obliczenie względnej zmiany procentowej**

$$\Delta_{\%} = \frac{25 - 20}{20} \cdot 100\% = \frac{5}{20} \cdot 100\% = 25\%$$
**Odpowiedź:** Poparcie wzrosło o $5$ punktów procentowych, co stanowi wzrost o $25\%$.

> **Wskazówka egzaminacyjna:**
> Na egzaminie zadania z procentu składanego najczęściej wymagają jedynie **wskazania prawidłowego wyrażenia algebraicznego** (np. $10\,000 \cdot (1{,}015)^8$), a nie żmudnego wyliczania potęgi na kalkulatorze. Zwróć uwagę na dzielenie oprocentowania rocznego przez liczbę okresów w roku!
