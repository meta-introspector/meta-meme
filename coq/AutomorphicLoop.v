(** Automorphic Galois Loop in UniMath/Coq **)

Require Import UniMath.Foundations.All.
Require Import UniMath.Combinatorics.StandardFiniteSets.

(** Loop elements as finite type **)
Inductive LoopElement : UU :=
  | emoji : LoopElement
  | concept : LoopElement
  | math : LoopElement
  | lean4 : LoopElement
  | perf : LoopElement
  | self : LoopElement.

(** Closed loop automorphism **)
Definition closed_loop (e : LoopElement) : LoopElement :=
  match e with
  | emoji => concept
  | concept => math
  | math => lean4
  | lean4 => perf
  | perf => self
  | self => emoji
  end.

(** Iterate n times **)
Fixpoint iterate (n : nat) (e : LoopElement) : LoopElement :=
  match n with
  | O => e
  | S n' => closed_loop (iterate n' e)
  end.

(** Theorem: Loop closes after 6 iterations **)
Theorem loop_closes : iterate 6 emoji = emoji.
Proof.
  reflexivity.
Qed.

(** Element complexity **)
Definition element_complexity (e : LoopElement) : nat :=
  match e with
  | emoji => 0
  | concept => 10
  | math => 100
  | lean4 => 1
  | perf => 0
  | self => 150
  end.

(** Total complexity **)
Definition loop_complexity : nat := 261.

Theorem loop_complexity_correct :
  element_complexity emoji +
  element_complexity concept +
  element_complexity math +
  element_complexity lean4 +
  element_complexity perf +
  element_complexity self = loop_complexity.
Proof.
  reflexivity.
Qed.

(** Self is fixed point after 5 iterations **)
Theorem self_at_position_5 : iterate 5 emoji = self.
Proof.
  reflexivity.
Qed.

(** 15D coordinates **)
Definition Coord15D := nat × nat × nat × nat × nat × nat × nat × nat × 
                       nat × nat × nat × nat × nat × nat × nat.

Definition emoji_coords : Coord15D := 
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0).

Definition concept_coords : Coord15D := 
  (0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 0, 0, 0, 0, 0).

Definition math_coords : Coord15D := 
  (0, 10, 0, 0, 0, 0, 0, 100, 100, 100, 0, 0, 0, 0, 0).

Definition lean4_coords : Coord15D := 
  (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0).

Definition perf_coords : Coord15D := 
  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0).

Definition self_coords : Coord15D := 
  (0, 11, 1, 3, 1, 0, 9, 150, 150, 150, 0, 0, 0, 0, 0).

(** Map element to coordinates **)
Definition element_to_coords (e : LoopElement) : Coord15D :=
  match e with
  | emoji => emoji_coords
  | concept => concept_coords
  | math => math_coords
  | lean4 => lean4_coords
  | perf => perf_coords
  | self => self_coords
  end.

(** Extract 8th dimension (complexity) **)
Definition get_complexity (c : Coord15D) : nat :=
  match c with
  | (_, _, _, _, _, _, _, comp, _, _, _, _, _, _, _) => comp
  end.

Theorem coords_match_complexity (e : LoopElement) :
  get_complexity (element_to_coords e) = element_complexity e.
Proof.
  destruct e; reflexivity.
Qed.
