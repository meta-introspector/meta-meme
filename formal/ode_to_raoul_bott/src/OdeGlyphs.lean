/--
  Ode-to-Raoul-Bott: formalization scaffold (Lean 4)
  - Glyph and Concept basic definitions
  - Rule set (finite, partial — see README)
  - Reduction engine (single-step and bounded normalization)

  This is a scaffolding commit. Full termination/determinism proofs
  will follow once the rule set is finalized.
-/

namespace OdeToRaoulBott

/-- For flexibility we represent Glyph and Concept as String wrappers.
    This keeps the initial code simple and easy to extend to an inductive list
    of known glyphs later. -/

def Glyph := String

def Concept := String

/-- A rewrite rule: lhs (list of glyph tokens) -> rhs (list of concepts).
    In a deterministic core these will be non-overlapping; ambiguous/creative
    mappings are recorded separately as relations in README and Rules.lean. -/

abbrev Rule := (List Glyph × List Concept)

/-- Example (partial) rule set extracted from the wiki. This is intentionally
    incomplete: some lines contained ellipses or multiple creative glosses.
    See README for how these are modeled. -/

def exampleRules : List Rule :=
  [ ( ["🎭🔮🎶"], ["Calliope"] )
  , ( ["🔑"],      ["ode"] )
  , ( ["🌌"],      ["cosmos"] )
  , ( ["🌠🎵"],    ["sage"] )
  , ( ["🔑📜"],    ["epic poetry"] )
  ]

/-- Try to match a rule lhs as a prefix of the input tokens. If matched,
    replace the prefix by the rhs (concept tokens) and return the new token list.
    Note: we keep concepts and glyphs in the same list for the reduction engine,
    so downstream passes may operate on concept tokens as well. -/

def listStartsWith {α : Type} (xs ys : List α) : Bool :=
  xs.length <= ys.length && (xs.zip ys).all (fun (a, b) => a = b)

def replacePrefix {α : Type} (prefix : List α) (suffix : List α) (xs : List α) : List α :=
  let rest := xs.drop prefix.length
  suffix ++ rest

/-- A single-step reduction using the provided rule set. Returns the first
    applicable reduction (leftmost rule). -/

def reduceOnce (rules : List Rule) (input : List Glyph) : Option (List Glyph) :=
  let tryRule (r : Rule) :=
    let (lhs, rhs) := r
    if listStartsWith lhs input then
      some ( (rhs.map id) ++ (input.drop lhs.length) )
    else
      none
  rules.foldl (fun acc r => acc.orElse (tryRule r)) none

/-- Bounded normalization: apply reduceOnce up to `maxSteps` times.
    This is a simple engine sufficient for computing normal forms in examples.
    A proper termination proof will replace this bounded loop with a
    well-founded recursion on a measure (e.g., glyph count). -/

partial def normalizeBounded (rules : List Rule) (maxSteps : Nat) (input : List Glyph) : List Glyph :=
  if maxSteps = 0 then input
  else match reduceOnce rules input with
    | none => input
    | some next => normalizeBounded rules (maxSteps - 1) next

/-- Convenience: normalize with a default step bound. -/

def normalize (rules : List Rule) (input : List Glyph) : List Glyph :=
  normalizeBounded rules 1000 input

#eval normalize exampleRules ["🎭🔮🎶","🔑","🌌","🌠🎵","🔑📜"]

end OdeToRaoulBott
