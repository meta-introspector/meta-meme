% MiniZinc model: N-gram similarity with GPU acceleration
% Finds optimal code patterns using constraint solving

% Number of files to compare
int: n_files = 4;  % Our file + 3 similar files

% Number of top n-grams to consider
int: n_patterns = 20;

% N-gram frequencies (from our analysis)
array[1..n_patterns] of int: our_ngrams = [
  38, 37, 33, 30, 27, 27, 20, 20, 20, 16,
  15, 15, 15, 15, 15, 14, 14, 14, 13, 13
];

% Similarity scores (from analysis)
array[1..3] of float: similarities = [0.0121, 0.0365, 0.0265];

% Decision variables: which patterns to keep/optimize
array[1..n_patterns] of var 0..1: keep_pattern;
array[1..n_patterns] of var 0..1: optimize_pattern;

% Constraint: Can't optimize what we don't keep
constraint forall(i in 1..n_patterns)(
  optimize_pattern[i] <= keep_pattern[i]
);

% Objective: Maximize unique patterns (high frequency, low similarity)
var int: uniqueness_score = sum(i in 1..n_patterns)(
  keep_pattern[i] * our_ngrams[i]
);

% Constraint: Keep at least 80% of patterns
constraint sum(keep_pattern) >= 16;

% Constraint: Optimize at least 30% of kept patterns
constraint sum(optimize_pattern) >= 6;

% Prioritize high-frequency patterns
constraint forall(i in 1..10)(
  keep_pattern[i] = 1  % Keep top 10
);

% GPU acceleration hint: patterns for parallel processing
array[1..n_patterns] of var 0..1: gpu_accelerate;

% Constraint: GPU accelerate the most compute-intensive patterns
constraint sum(gpu_accelerate) = 5;  % Top 5 for GPU

% Constraint: Only GPU accelerate what we optimize
constraint forall(i in 1..n_patterns)(
  gpu_accelerate[i] <= optimize_pattern[i]
);

solve maximize uniqueness_score;

output [
  "N-gram Optimization with GPU Acceleration\n",
  "==========================================\n\n",
  "Uniqueness Score: ", show(uniqueness_score), "\n",
  "Patterns to Keep: ", show(sum(keep_pattern)), "/", show(n_patterns), "\n",
  "Patterns to Optimize: ", show(sum(optimize_pattern)), "\n",
  "GPU Accelerated: ", show(sum(gpu_accelerate)), "\n\n",
  "Top 10 Pattern Decisions:\n",
  "  Pattern 1 (freq=38): ", show(keep_pattern[1]), " ", show(optimize_pattern[1]), " ", show(gpu_accelerate[1]), "\n",
  "  Pattern 2 (freq=37): ", show(keep_pattern[2]), " ", show(optimize_pattern[2]), " ", show(gpu_accelerate[2]), "\n",
  "  Pattern 3 (freq=33): ", show(keep_pattern[3]), " ", show(optimize_pattern[3]), " ", show(gpu_accelerate[3]), "\n",
  "  Pattern 4 (freq=30): ", show(keep_pattern[4]), " ", show(optimize_pattern[4]), " ", show(gpu_accelerate[4]), "\n",
  "  Pattern 5 (freq=27): ", show(keep_pattern[5]), " ", show(optimize_pattern[5]), " ", show(gpu_accelerate[5]), "\n",
  "\nRecommendations:\n",
  "  1. Keep high-frequency patterns\n",
  "  2. GPU accelerate Monster weight calculations\n",
  "  3. GPU accelerate N-gram similarity\n",
  "  4. GPU accelerate Resonance detection\n"
];
