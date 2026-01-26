(** MetaCoq extraction to Rust **)

From MetaCoq.Template Require Import All.
Require Import AutomorphicLoop.

(** MetaCoq commands to extract **)
MetaCoq Quote Definition loop_element_quoted := LoopElement.
MetaCoq Quote Definition closed_loop_quoted := closed_loop.
MetaCoq Quote Definition iterate_quoted := iterate.
MetaCoq Quote Definition loop_closes_quoted := loop_closes.

(** Extract to Rust **)
Extraction Language Rust.

(** Configure extraction **)
Extract Inductive LoopElement => "LoopElement" [
  "LoopElement::Emoji"
  "LoopElement::Concept"
  "LoopElement::Math"
  "LoopElement::Lean4"
  "LoopElement::Perf"
  "LoopElement::Self"
].

Extract Inductive nat => "u64" [ "0" "succ" ]
  "(fun fO fS n -> if n == 0 { fO() } else { fS(n - 1) })".

Extract Constant closed_loop => "closed_loop".
Extract Constant iterate => "iterate".

Recursive Extraction closed_loop iterate loop_closes.
