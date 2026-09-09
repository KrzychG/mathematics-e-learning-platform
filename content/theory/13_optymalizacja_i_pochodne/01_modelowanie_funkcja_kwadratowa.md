# 1. Modelowanie sytuacji praktycznych funkcją kwadratową

W zakresie podstawowym nowego egzaminu zagadnienia optymalizacyjne opierają się na modelowaniu zjawisk za pomocą **funkcji kwadratowej** $f(x) = ax^2 + bx + c$. Zadanie polega na przekształceniu problemu słownego w relację analityczną jednej zmiennej.

> **Definicja: Czterokrokowy algorytm budowy modelu optymalizacyjnego**
> 1. **Krok 1 (Wybór zmiennej):** Określenie, jaka wielkość jest zmienną niezależną (np. niech $x$ oznacza długość jednego z boków prostokąta lub liczbę obniżek ceny).
> 2. **Krok 2 (Zależności pomocnicze):** Wyrażenie drugiej wielkości za pomocą zmiennej $x$ na podstawie warunku z treści zadania (np. stałego obwodu lub stałej sumy).
> 3. **Krok 3 (Dziedzina geometryczna/fizyczna):** Wyznaczenie przedziału dopuszczalnych wartości zmiennej $x$ (wymiary muszą być ściśle dodatnie: $x > 0$ oraz inne boki $> 0$).
> 4. **Krok 4 (Funkcja celu):** Zapisanie wzoru optymalizowanej wielkości (pola, zysku, kosztu) jako funkcji kwadratowej:
> $$f(x) = ax^2 + bx + c$$

### Przykład 1: Modelowanie pola wybiegu przy rzece

Rolnik chce ogrodzić siatką o długości $120\text{ m}$ prostokątny wybieg dla zwierząt. Jeden z boków wybiegu przylega do rzeki i nie wymaga ogrodzenia. Zbuduj model matematyczny pola tego wybiegu w zależności od długości boku prostopadłego do rzeki.

**Krok 1: Wprowadzenie zmiennych**

Niech $x$ oznacza długość każdego z dwóch boków prostopadłych do rzeki ($x > 0$), a $y$ długość boku równoległego do rzeki ($y > 0$).

**Krok 2: Zależność z długości siatki**

Suma trzech ogrodzonych boków wynosi $120\text{ m}$:
$$2x + y = 120 \implies y = 120 - 2x$$

**Krok 3: Wyznaczenie dziedziny geometrycznej**

Wymiary muszą być dodatnie:
$$\begin{cases} x > 0 \\ 120 - 2x > 0 \end{cases} \implies \begin{cases} x > 0 \\ 2x < 120 \end{cases} \implies x \in (0, 60)$$

**Krok 4: Wzór funkcji celu pola $P(x)$**

$$P(x) = x \cdot y = x(120 - 2x) = -2x^2 + 120x \quad \text{dla } x \in (0, 60)$$

### Przykład 2: Modelowanie przychodu z biletów

Kino sprzedaje bilety na seans w cenie $30\text{ zł}$, gromadząc średnio $200$ widzów. Badania rynkowe wskazują, że każda obniżka ceny o $2\text{ zł}$ powoduje wzrost liczby widzów o $40$ osób. Wyznacz wzór przychodu kina w zależności od liczby obniżek $x$.

**Krok**

Niech $x$ oznacza liczbę obniżek o $2\text{ zł}$ ($x \ge 0$ i $30 - 2x > 0 \implies x \in \langle 0, 15)$):
Nowa cena biletu: $C(x) = 30 - 2x$

Nowa liczba widzów: $L(x) = 200 + 40x$

Przychód kina $R(x)$ to iloczyn ceny i liczby widzów:
$$R(x) = (30 - 2x)(200 + 40x) = 6000 + 1200x - 400x - 80x^2 = -80x^2 + 800x + 6000$$

> **Wskazówka egzaminacyjna (Wymóg formalny):**
> W zadaniu optymalizacyjnym **zawsze musisz podać dziedzinę** funkcji (np. $x \in (0, 60)$). Brak określenia dziedziny skutkuje utratą punktu według klucza egzaminacyjnego!
