# Modello PLI per P_m||C_max (scheduling su m macchine identiche,
# minimizzazione del makespan). Formulazione assignment standard con
# rottura di simmetria sui carichi delle macchine (le macchine sono
# identiche: senza rottura di simmetria il solver esplora m! soluzioni
# equivalenti per ogni assegnazione, il che e' molto costoso per i
# solver MIP su questo problema classico).

set J;                       # job
set M ordered;                # macchine (ordinato: serve per ord()/next() nella rottura di simmetria)

param p{J} >= 0 integer;     # tempo di lavorazione di ciascun job

var x{J, M} binary;          # x[j,h] = 1 se il job j e' assegnato alla macchina h
var Cmax >= 0;
var load{M} >= 0;            # carico di ciascuna macchina (variabile vera, legata a x
                              # dal vincolo load_def sotto: la sintassi "var load = expr;"
                              # in AMPL imposta solo un valore *iniziale*, non un vincolo
                              # di uguaglianza, e produceva soluzioni non ottime)

minimize makespan: Cmax;

s.t. assign{j in J}: sum{h in M} x[j, h] = 1;

s.t. load_def{h in M}: load[h] = sum{j in J} p[j] * x[j, h];

s.t. load_bound{h in M}: load[h] <= Cmax;

# Rottura di simmetria: i carichi delle macchine, ordinate secondo l'ordine
# di M, devono essere non crescenti.
s.t. symmetry_break{h in M: ord(h) < card(M)}:
    load[h] >= load[next(h)];
