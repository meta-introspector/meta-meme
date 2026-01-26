(** Standard Coq extraction to OCaml **)

Require Import AutomorphicLoop.
Require Extraction.

Extraction Language OCaml.
Recursive Extraction closed_loop iterate loop_closes.
