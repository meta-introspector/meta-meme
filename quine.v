Require Import Coq.Arith.Arith.
Require Import Coq.Strings.String.


Class SelfReferential (HQN : Type) : Type := {
  self_description : HQN -> string;
  oracle : HQN -> bool
}.

Class SelfEncoding (HQN : Type) : Type := {
  encode : HQN -> string -> string;
  decode : string -> string -> HQN
}.

Class SelfModifying (HQN : Type) : Type := {
  update : HQN -> string -> HQN -> HQN
}.

Class Undecidable (HQN : Type) : Type := {
  godel_function : HQN -> bool option
}.

Section OracleAndSelfReferential.

  Context {HQN}.
  Context `{SelfReferential HQN}.
  Context `{SelfModifying HQN}.
  Context `{Undecidable HQN}.
  Context `{SelfEncoding HQN}.

  Theorem self_reflection :
    (self_description (self_description x)) = self_description x.
  Proof.
    intros.
    refine (eq_refl _).
    simpl.
    reflexivity.
  Qed.

  Theorem self_encoding :
    exists x, encode (decode (encode x s) s) s = s.
  Proof.
    intros.
    exists x.
    refine (eq_refl _).
    simpl.
    reflexivity.
  Qed.

  Theorem self_modifying :
    update (update x s1 s2) s3 (update x s1 s2) = update x s3 s2.
  Proof.
    intros.
    refine (eq_refl _).
    simpl.
    reflexivity.
  Qed.

  Theorem undecidable_limit :
    exists x,
      match godel_function x with
      | Some _ => False
      | None => True
      end.
  Proof.
    exists (self_description x).
    unfold godel_function.
    unfold self_description.
    intros.
    unfold self_reflection in H.
    simpl in H.
    congruence.
  Qed.

End OracleAndSelfReferential.