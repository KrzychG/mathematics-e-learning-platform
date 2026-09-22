(function (global) {
    'use strict';

    function safeEval(fn, x) {
        try {
            const v = fn(x);
            return (typeof v === 'number' && Number.isFinite(v)) ? v : NaN;
        } catch (e) {
            return NaN;
        }
    }

    // Metoda bisekcji:
    // Po wykryciu zmiany znaku na końcach podprzedziału zacieśniamy zakres w 16 krokach,
    // co daje dokładność do 6 miejsc po przecinku (1e-6) na potrzeby zaznaczenia kropki na wykresie.
    function bisectRoot(fn, a, b, valA, maxIter = 16, tol = 1e-6) {
        let low = a, high = b;
        let vA = valA;
        if (Math.abs(vA) < tol) return a;
        const vB = safeEval(fn, b);
        if (Math.abs(vB) < tol) return b;

        for (let k = 0; k < maxIter; k++) {
            const mid = (low + high) / 2;
            const midVal = safeEval(fn, mid);
            if (!Number.isFinite(midVal)) break;
            if (Math.abs(midVal) < tol) return mid;
            if (vA * midVal <= 0) {
                high = mid;
            } else {
                low = mid;
                vA = midVal;
            }
        }
        return (low + high) / 2;
    }

    /**
     * Numeryczne wyznaczanie miejsc zerowych funkcji na przedziale.
     * Zwraca tablicę unikalnych pierwiastków lub pustą tablicę z flagą isIdenticallyZero = true,
     * gdy badana funkcja jest tożsamościowo równa zero f(x) == 0.
     *
     * @param {function(number): number} fn Badana funkcja f(x)
     * @param {number} minX Początek badanego przedziału osi OX
     * @param {number} maxX Koniec badanego przedziału osi OX
     * @param {number} samples Liczba kroków próbkowania
     * @returns {number[] & { isIdenticallyZero?: boolean }}
     */
    function findFunctionZeros(fn, minX, maxX, samples = 140) {
        const roots = [];
        if (typeof fn !== 'function' || !Number.isFinite(minX) || !Number.isFinite(maxX) || minX >= maxX) {
            return roots;
        }

        //Sprawdzenie czy funkcja jest tożsamościowo równa zero na badanym przedziale
        const checkSteps = 24;
        const testStep = (maxX - minX) / checkSteps;
        const testPoints = [];
        for (let i = 0; i <= checkSteps; i++) {
            testPoints.push(minX + i * testStep);
        }
        // Punkty referencyjne
        [-10, -5, -2, -1, 0, 1, 2, 5, 10, Math.PI, Math.E].forEach(pt => {
            if (!testPoints.some(p => Math.abs(p - pt) < 1e-4)) {
                testPoints.push(pt);
            }
        });

        let finiteCount = 0;
        let allZero = true;
        for (const pt of testPoints) {
            const val = safeEval(fn, pt);
            if (Number.isFinite(val)) {
                finiteCount++;
                if (Math.abs(val) > 1e-7) {
                    allZero = false;
                    break;
                }
            }
        }

        if (finiteCount >= 5 && allZero) {
            roots.isIdenticallyZero = true;
            return roots;
        }

        // Poszukiwanie zmian znaku na siatce próbkowania
        const step = (maxX - minX) / samples;
        let prevX = minX;
        let prevVal = safeEval(fn, prevX);

        for (let i = 1; i <= samples; i++) {
            const curX = minX + i * step;
            const curVal = safeEval(fn, curX);

            if (Number.isFinite(prevVal) && Number.isFinite(curVal)) {
                const bothNearZero = Math.abs(prevVal) < 1e-7 && Math.abs(curVal) < 1e-7;

                if (!bothNearZero && prevVal * curVal <= 0 && Math.abs(curVal - prevVal) < 50) {
                    let rootX = bisectRoot(fn, prevX, curX, prevVal);
                    const rootVal = safeEval(fn, rootX);

                    // wartość musi być faktycznie bliska 0
                    if (Number.isFinite(rootVal) && Math.abs(rootVal) < 1e-3) {
                        const roundedInt = Math.round(rootX);
                        if (Math.abs(rootX - roundedInt) < 1e-4) {
                            rootX = roundedInt;
                        } else {
                            const roundedHalf = Math.round(rootX * 2) / 2;
                            if (Math.abs(rootX - roundedHalf) < 1e-4) {
                                rootX = roundedHalf;
                            }
                        }

                        if (!roots.some(r => Math.abs(r - rootX) < 0.08)) {
                            roots.push(rootX);
                        }
                    }
                }
            }

            prevX = curX;
            prevVal = curVal;
        }

        roots.sort((a, b) => a - b);
        return roots;
    }

    global.GraphSolvers = { findFunctionZeros };
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this));
