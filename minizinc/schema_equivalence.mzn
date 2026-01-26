% Schema Orbit Equivalence Checker (MiniZinc)
% Find all schemas equivalent to a given reference

% Two schemas to compare
array[1..2] of var float: conductor;
array[1..2] of var 0..100: weight;
array[1..2] of var 0..20: level;
array[1..2] of var 0..3: traits;
array[1..2] of var 0..10: key_primes;

% Complexity scores
array[1..2] of var float: complexity;
constraint forall(i in 1..2) (
  complexity[i] = conductor[i] + weight[i] * 2.0 + level[i] * 3.0 + 
                  traits[i] + key_primes[i] * 5.0
);

% Orbit epsilon
float: epsilon = 10.0;

% Constraint: Both schemas in same orbit (strictly less than epsilon)
constraint abs(complexity[1] - complexity[2]) <= epsilon;

% Constraint: Non-negative conductors
constraint forall(i in 1..2) (conductor[i] >= 0.0);

% Constraint: Bounded traits
constraint forall(i in 1..2) (traits[i] <= 3);

% Fix first schema (reference)
constraint conductor[1] = 137.1;
constraint weight[1] = 5;
constraint level[1] = 1;
constraint traits[1] = 3;
constraint key_primes[1] = 1;

% Find equivalent schema with different structure
constraint weight[2] != weight[1] \/ level[2] != level[1];

solve satisfy;

output [
  "Schema 1 (reference):\n",
  "  complexity: ", show(complexity[1]), "\n",
  "Schema 2 (equivalent):\n",
  "  conductor: ", show(conductor[2]), "\n",
  "  weight: ", show(weight[2]), "\n",
  "  level: ", show(level[2]), "\n",
  "  traits: ", show(traits[2]), "\n",
  "  key_primes: ", show(key_primes[2]), "\n",
  "  complexity: ", show(complexity[2]), "\n",
  "Orbit distance: ", show(abs(complexity[1] - complexity[2])), "\n",
  "Equivalent: ", show(abs(complexity[1] - complexity[2]) < epsilon), "\n"
];
