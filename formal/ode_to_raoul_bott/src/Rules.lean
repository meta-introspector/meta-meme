-- Rules.lean
-- Record of the rule set (deterministic core + nondeterministic relations)
-- This file intentionally keeps the creative/multivalued mappings documented
-- but does not include the ambiguous mappings in the deterministic "rules" list.

-- See README.md for instructions on how to finalize the rule set.

/-- Example of documenting nondeterministic mappings: -/

/-
  The wiki contained several lines where the same emoji sequence was
  given multiple natural-language glosses in different passages, and at
  least one rule ended with an ellipsis "...". Those are recorded here
  as comments and will be modeled as relations in a later commit.

  Example ambiguous mapping from the wiki:
    "🔑📜 -> epic poetry ..."
  The right-hand side is incomplete in the source; we therefore treat
  this entry as incomplete and non-functional for deterministic proofs.
-/

-- TODO: add a script that extracts every emoji token used in the wiki and
-- checks coverage against the deterministic rule set.
