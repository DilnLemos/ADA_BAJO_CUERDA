# Informe de Implementación — Problema del Riego Óptimo 
---

## 1. Descripción del Problema

El **problema del riego óptimo** consiste en determinar el orden en que deben regarse los tablones de una finca utilizando un único sistema de riego, de modo que se minimice el sufrimiento de los cultivos por falta de agua.

Cada tablón tiene tres características:

* $ts_i$: tiempo máximo que puede sobrevivir sin riego (días),
* $tr_i$: tiempo que tarda en regarse (días),
* $p_i$: prioridad (entero entre 1 y 4, siendo 4 la más alta).

El riego se realiza de forma secuencial y no hay costo por mover el sistema de riego entre tablones.

---

## 2. Modelo Matemático/Minizinc
El proyecto se basará en un modelo hecho en el programa *minizinc* para realizar todas las pruebas contundentes de funcionamiento para la función objetivo.

##### *a. Dados los parámetros*
$n$: número de tablones (enteros). Para cada tablón $i\in\{0,\dots,n-1\}$:$$\begin{aligned}
&t^s_i &&:\ \text{tiempo de supervivencia (días)}\\
&t^r_i &&:\ \text{tiempo de regado (días)}\\
&p_i &&:\ \text{prioridad (peso), entero en }\{1,\dots,4\}
\end{aligned}$$
```minizinc
include "alldifferent.mzn";
include "inverse.mzn";

int: n;
array[1..n] of int: ts;  % tiempo de supervivencia (t^s_i)
array[1..n] of int: tr;  % tiempo de regado (t^r_i)
array[1..n] of int: p;   % prioridad (p_i)

```

##### *b. Variables de Decisión y Permutación:*
Buscamos una permutación $\Pi=\langle\pi_0,\pi_1,\dots,\pi_{n-1}\rangle$ de los índices $\{0,\dots,n-1\}$ usando La restricción $all_.different$ que  asegura que se considere una secuencia única de tablones, mientras que $inverse$ establece la relación de mapeo entre la posición de riego y el índice del tablón.
1. La representamos con las siguientes variables enteras:$$\begin{aligned}
&\mathrm{order}[k] = \text{índice del tablón que se riega en la posición }k\quad( k=1,\dots,n ).\\
&\mathrm{pos}_i = \text{la posición }(1..n) \text{ donde aparece el tablón }i \text{ en la permutación (inversa de order).}
\end{aligned}$$
```minizinc

% Variables de Secuenciación
array[1..n] of var 1..n: order;       % índice del tablón en la posición k (1..n)
constraint all_different(order);

array[1..n] of var 1..n: pos;         % posición (1..n) donde aparece el tablón i
constraint inverse(order, pos);
```

##### *c. Tiempos de Riego Secuencial:*
Definimos el tiempo de inicio de riego para la posición $k$, $T^\mathrm{ini}(k)$, y el tiempo de finalización de riego para la posición $k$, $C(k)$.$$\begin{aligned}
T^\mathrm{ini}(1) &= 0 \quad\text{(El primer tablón inicia en } t=0 \text{)}\\
C(k) &= T^\mathrm{ini}(k) + t^r_{\mathrm{order}[k]} \quad\text{(Finalización = Inicio + Regado).}\\
T^\mathrm{ini}(k) &= C(k-1) \quad\text{para } k=2,\dots,n \quad\text{(El siguiente inicia cuando el anterior finaliza)}
\end{aligned}$$
```minizinc

% Cálculo tiempo inicio (t_pi_j^Pi) y Finalización (t_pi_j^Pi + tr_pi_j)
array[1..n] of var 0..sum(tr): Cpos;  %  Tiempo de finalización de riego para el tablón en la posición k

% Tiempo de Inicio para el tablón en la posición k. (t_pi_j^Pi)
array[1..n] of var 0..sum(tr): TstartPos;

% Restricciones del tiempo de inicio
constraint TstartPos[1] = 0; % El primer tablón inicia en t=0 
constraint Cpos[1] = TstartPos[1] + element(order[1], tr); % Cálculo recursivo

constraint forall(k in 2..n) (
    TstartPos[k] = Cpos[k-1] % El tablón en la posición k inicia cuando termina el anterior (posición k-1)
);

constraint forall(k in 2..n) (
    
    Cpos[k] = TstartPos[k] + element(order[k], tr) % El tiempo de finalización es el tiempo de inicio + tiempo de regado
);

% 2. Cálculo tiempo fin por tablón (Cjob)

array[1..n] of var 0..sum(tr): Cjob; % Tiempo de finalización para el tablón i
constraint forall(i in 1..n) (
    Cjob[i] = Cpos[pos[i]]
);
```

##### *d. Penalización (Tardanza Ponderada):*
Se implementa la linealización de la función tardanza ($T_i = \max(0, C_i - t^s_i)$) mediante dos restricciones de desigualdad, garantizando que el valor de $T[i]$ sea exactamente el retraso, o cero si no hay retraso.
$$\begin{aligned}
&C_i = C(\mathrm{pos}_i) \quad\text{(tiempo de finalización del tablón }i).\\
&T_i = \max\bigl(0,\; C_i - t^s_i\bigr) \quad\text{(tardanza/retraso en días)}
\end{aligned}$$
```minizinc
% 3. Penalización
array[1..n] of var 0..sum(tr): T; % max(0, Cjob[i] - ts[i]) 
constraint forall(i in 1..n) (
    T[i] >= Cjob[i] - ts[i] /\
    T[i] >= 0
);
```

##### *e. Función Objetivo*
Se busca minimizar el Costo Total de Riego ($CRF^\Pi$), que es la suma de las penalizaciones ponderadas por la prioridad de cada tablón2.$$\min Z = \sum_{i=0}^{n-1} p_i\,T_i,
\quad\text{donde } T_i = \max\bigl(0,\; C_i - t^s_i\bigr).$$
```minizinc

% Función objetivo: minimizar suma de p[i] * T[i] 
var int: TotalCost = sum(i in 1..n)(p[i] * T[i]);
solve minimize TotalCost;

% Salida: primera línea costo total, luego los índices de los tablones (0..n-1)
output [
    show(TotalCost), "\n",
    concat([ show(order[k] - 1) ++ if k < n then "\n" else "" endif | k in 1..n ])
];
```

##### f. Restricciones Principales
$$\begin{aligned}
&\mathrm{order}: \text{es una permutación de }\{1,\dots,n\}.\\
&\mathrm{pos}: \text{es la inversa de }\mathrm{order}.\\
&T^\mathrm{start}(1) = 0\\
&T^\mathrm{start}(k) - C(k-1) = 0 \quad \forall k=2,\dots,n.\\
&C(k) - T^\mathrm{start}(k) = t^r_{\mathrm{order}[k]} \quad \forall k=1,\dots,n.\\
&C_i = C(\mathrm{pos}_i) \quad \forall i=0,\dots,n-1.\\
&T_i \ge C_i - t^s_i \quad \forall i\ \text{(Garantiza la linealización del máximo).}\\
&T_i \ge 0 \quad \forall i.
\end{aligned}$$
