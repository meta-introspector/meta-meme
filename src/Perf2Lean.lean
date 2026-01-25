import Lean

/-- perf2lean: Convert performance traces to Lean proofs --/

namespace MetaMeme.Perf2Lean

structure PerfEvent where
  event : String
  count : Nat
  duration : Nat
  deriving Repr

syntax "perf!" str : term

macro_rules
  | `(perf! $event:str) => `(PerfEvent.mk $event 0 0)

/-- Prove performance bounds --/
def withinBounds (p : PerfEvent) (max : Nat) : Prop :=
  p.duration ≤ max

theorem perfBounded (p : PerfEvent) (h : p.duration ≤ 1000) :
    withinBounds p 1000 := h

end MetaMeme.Perf2Lean
