% Recursive Schema Model (MiniZinc)
% Each element of a schema can itself be a schema

% Schema node types
enum NodeType = {ATOM, SCHEMA};

% Number of nodes in recursive schema
int: n_nodes = 10;

% Node properties
array[1..n_nodes] of var NodeType: node_type;
array[1..n_nodes] of var 0..n_nodes: parent;  % 0 = root
array[1..n_nodes] of var 0..10: depth;

% Root node must be a schema
constraint node_type[1] = SCHEMA;
constraint parent[1] = 0;
constraint depth[1] = 0;

% Depth constraint: child depth = parent depth + 1
constraint forall(i in 2..n_nodes) (
  if parent[i] > 0 then
    depth[i] = depth[parent[i]] + 1
  else
    depth[i] = 0
  endif
);

% Atoms cannot have children
constraint forall(i in 1..n_nodes) (
  if node_type[i] = ATOM then
    forall(j in 1..n_nodes) (parent[j] != i)
  endif
);

% Complexity: count all nodes
var int: complexity = sum(i in 1..n_nodes)(1);

% Max depth
var int: max_depth = max(depth);

% Constraint: At least 3 levels deep
constraint max_depth >= 3;

% Constraint: At least 2 schema nodes
constraint sum(i in 1..n_nodes)(node_type[i] = SCHEMA) >= 2;

solve maximize max_depth;

output [
  "Recursive Schema:\n",
  "  nodes: ", show(n_nodes), "\n",
  "  complexity: ", show(complexity), "\n",
  "  max_depth: ", show(max_depth), "\n"
];
