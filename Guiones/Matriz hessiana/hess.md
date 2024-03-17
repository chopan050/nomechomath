El gradiente y la matriz hessiana son algo así como la primera y segunda derivada, pero de funciones MULTIVARIABLE. Así que para explicarlas, hay que entender bien las derivadas en UNA. VARIABLE.

Partamos con la función f(x) = x^2.

Cuando x vale 1, f(x) también vale 1.
Y f(2) vale 4.

Entonces, si partes de x = 1, y AUMENTAS x en 1 unidad, f(x) pasa de valer 1 a valer 4, por lo que aumenta: 3 unidades. Al incremento en x lo denotamos "Delta x", y al incremento en f, "Delta f". Un Delta x de 1, provocó un Delta f de 3.

Probemos un Delta x más pequeño: 0.1.
f(1) es 1, y f(1.1) es 1.01. Al restar ambos valores, Delta f es 0.01.

Podemos seguir achicando Delta x, pero hay que hacer zoom en la función, y observa: cada vez se parece más a una recta, algo como f(x) = mx + n.

Las rectas son ideales en el sentido de que el cambio en f es PROPORCIONAL al cambio en x: un Delta x de 1 provoca un Delta f de m. Al duplicar Delta x se duplica Delta f: vale 2m. En general, Delta f es m veces Delta x. Es decir, la razón Delta f sobre Delta x es siempre una constante: m, la "pendiente" de la recta.

Pero esto solo pasa en rectas. La función f(x) = x^2 es más... curvilínea,

Imagina que x es el lado de un cuadrado, y f(x) es su área.