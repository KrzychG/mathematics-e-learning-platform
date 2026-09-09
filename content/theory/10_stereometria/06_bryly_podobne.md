# 6. Bryły podobne i stosunek objętości

Dwie bryły są **podobne** w skali $k > 0$, jeśli mają identyczny kształt przestrzenny, a wszystkie odpowiadające sobie wymiary liniowe (krawędzie, wysokości, promienie podstaw, przekątne) są proporcjonalne ze współczynnikiem $k$.

> **Definicja: Skala podobieństwa a pole i objętość**
> - **Wymiary liniowe (długości odcinków):**
> $$\frac{a_1}{a_2} = \frac{H_1}{H_2} = \frac{R_1}{R_2} = \frac{D_1}{D_2} = k$$
> - **Pola powierzchni:** Stosunek pól powierzchni (całkowitych i bocznych) jest równy **kwadratowi skali podobieństwa**:
> $$\frac{P_1}{P_2} = k^2$$
> - **Objętości:** Stosunek objętości brył podobnych jest równy **sześcianowi skali podobieństwa**:
> $$\frac{V_1}{V_2} = k^3 \iff k = \sqrt[3]{\frac{V_1}{V_2}}$$

### Przykład 1: Stosunek pól i objętości kul

Objętość pierwszej kuli wynosi $V_1 = 54\pi$, a objętość drugiej kuli wynosi $V_2 = 16\pi$. Wyznacz stosunek ich pól powierzchni $\frac{P_1}{P_2}$.

**Krok 1: Wyznaczenie sześcianu skali i samej skali $k$**

$$\frac{V_1}{V_2} = k^3 \implies k^3 = \frac{54\pi}{16\pi} = \frac{27}{8} \implies k = \sqrt[3]{\frac{27}{8}} = \frac{3}{2} = 1{,}5$$

**Krok 2: Wyznaczenie stosunku pól powierzchni**

$$\frac{P_1}{P_2} = k^2 = \left(\frac{3}{2}\right)^2 = \frac{9}{4} = 2{,}25$$
**Odpowiedź:** Stosunek pól wynosi $\frac{9}{4}$.

### Przykład 2: Zadanie praktyczne z masą figury (Skala trójwymiarowa)

Model pomnika wykonany z brązu ma wysokość $20\text{ cm}$ i masę $1{,}5\text{ kg}$. Rzeczywisty pomnik, wykonany z tego samego stopu brązu, ma wysokość $2\text{ m}$. Oblicz masę rzeczywistego pomnika.

**Krok 1: Ujednolicenie jednostek i wyznaczenie skali $k$**

Wysokość modelu: $H_m = 20\text{ cm} = 0{,}2\text{ m}$.
Wysokość pomnika: $H_p = 2\text{ m}$.

Skala powiększenia liniowego:
$$k = \frac{H_p}{H_m} = \frac{2}{0{,}2} = 10$$

**Krok 2: Zależność masy od objętości ($k^3$)**

Masa jednorodnej bryły jest wprost proporcjonalna do jej objętości ($m = \rho \cdot V$). Zatem:
$$\frac{m_p}{m_m} = k^3 = 10^3 = 1000$$
$$m_p = 1000 \cdot m_m = 1000 \cdot 1{,}5\text{ kg} = 1500\text{ kg} = 1{,}5\text{ tony}$$
**Odpowiedź:** Rzeczywisty pomnik waży $1500\text{ kg}$.

> **Wskazówka egzaminacyjna (Zasada trzech wymiarów):**
> • 1D (długość, obwód, wysokość) $\implies$ skala $k$
>
> • 2D (pole powierzchni, podstawa) $\implies$ skala $k^2$
>
> • 3D (objętość, pojemność w litrach, masa z tej samej gęstości) $\implies$ skala $k^3$
