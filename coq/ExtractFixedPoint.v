Require Import Nat.
Require Import List.
Load FixedPointConstruction.
Require Extraction.

Extraction Language OCaml.

Recursive Extraction
  LMFDBLabel
  FixedPoint
  ComplexityCurve
  construct_label
  construct_fixed_point
  lattice_curve
  fp_0 fp_1 fp_2 fp_3 fp_71
  diagonal_fp
  fixed_point_orbit
  is_diagonal
  construction_preserves_structure.
