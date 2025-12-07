% Use this editor as a MiniZinc scratch book
% Modelo MiniZinc para el problema de riego de tablones

include "alldifferent.mzn";
include "inverse.mzn";

int: n;
array[1..n] of int: ts;  % tiempo de supervivencia
array[1..n] of int: tr;  % tiempo de regado
array[1..n] of int: p;   % prioridad

% Variables de Secuenciación
array[1..n] of var 1..n: order;       % índice del tablón en la posición k (1..n)
constraint all_different(order);

array[1..n] of var 1..n: pos;         % posición (1..n) donde aparece el tablón i
constraint inverse(order, pos);

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

% 3. Penalización
array[1..n] of var 0..sum(tr): T; % max(0, Cjob[i] - ts[i]) 
constraint forall(i in 1..n) (
    T[i] >= Cjob[i] - ts[i] /\
    T[i] >= 0
);

% Función objetivo: minimizar suma de p[i] * T[i] 
var int: TotalCost = sum(i in 1..n)(p[i] * T[i]);
solve minimize TotalCost;

% Salida: primera línea costo total, luego los índices de los tablones (0..n-1)
output [
    show(TotalCost), "\n",
    "[",
    concat([ show(order[k] - 1) ++ if k == n then "" else " " endif | k in 1..n ]),
    "]"
];
