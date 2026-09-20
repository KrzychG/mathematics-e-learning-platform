/**
 * Adapter parsera wyrażeń matematycznych dla wykresów funkcji.
 * Zastępuje własną implementację algorytmu Shunting-Yard biblioteką math.js (CDN).
 * 
 * Odpowiada za kompilację wzoru tekstowego (np. "2x^2 - 3x + 1", "-(x-2)^2 + 4", "sin(x)", "1/x")
 * do funkcji JavaScript f(x) obliczającej wartości dla osi układu współrzędnych.
 */
(function (global) {
    'use strict';

    const MathParser = {
        /**
         * Normalizuje zapis potoczny użytkownika (np. przecinki dziesiętne, mnożenie niejawne).
         */
        sanitize(expr) {
            if (!expr || typeof expr !== 'string') return '';
            return expr
                .trim()
                // Polski przecinek dziesiętny na kropkę (np. 2,5 -> 2.5)
                .replace(/(\d),(\d)/g, '$1.$2')
                // Mnożenie niejawne: 2x -> 2*x, 3(x+1) -> 3*(x+1)
                .replace(/([0-9])([a-zA-Z(])/g, '$1*$2')
                // Mnożenie nawiasów: (x+1)(x-1) -> (x+1)*(x-1)
                .replace(/\)([0-9a-zA-Z(])/g, ')*$1');
        },

        /**
         * Kompiluje wzór tekstowy do funkcji JavaScript f(x) za pośrednictwem biblioteki math.js.
         * 
         * @param {string} expr Wzór funkcji
         * @returns {function(number): number} Funkcja f(x) zwracająca wartość lub NaN
         */
        compile(expr) {
            try {
                const sanitized = this.sanitize(expr);
                if (!sanitized) return () => NaN;

                // Sprawdzamy dostępność biblioteki math.js
                if (global.math && typeof global.math.compile === 'function') {
                    const compiled = global.math.compile(sanitized);

                    return function evaluateMathJs(xVal) {
                        try {
                            const scope = {
                                x: xVal,
                                e: Math.E,
                                pi: Math.PI,
                                // Polskie oznaczenia logarytmów szkolnych
                                ln: (v) => (v <= 0 ? NaN : Math.log(v)),
                                log: (v) => (v <= 0 ? NaN : Math.log10(v))
                            };
                            const result = compiled.evaluate(scope);

                            // Bezpieczna konwersja do liczby zmiennoprzecinkowej
                            if (typeof result === 'number' && Number.isFinite(result)) {
                                return result;
                            }
                            return NaN;
                        } catch (evalErr) {
                            return NaN;
                        }
                    };
                }

                // Bezpieczny fallback offline
                return (xVal) => {
                    try {
                        if (sanitized === 'x') return xVal;
                        if (/^-?\d+(\.\d+)?$/.test(sanitized)) return parseFloat(sanitized);
                        return NaN;
                    } catch (e) {
                        return NaN;
                    }
                };
            } catch (compileErr) {
                return () => NaN;
            }
        }
    };

    global.MathParser = MathParser;
})(typeof window !== 'undefined' ? window : this);
