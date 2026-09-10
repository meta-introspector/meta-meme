# Ode to Raoul Bott — formalization notes

This directory contains an initial Lean 4 scaffolding for the Ode-to-Raoul-Bott
formalization. It intentionally starts small so we can iterate on the rule set.

What is included:
- src/OdeGlyphs.lean — basic Glyph/Concept types, an example rule set, and a
  small bounded normalizer useful for computation and testing.
- src/Rules.lean — documentation of ambiguous or incomplete rules (nondeterministic).
- src/Reduction.lean — tokenization helpers and example runs.
- src/Proofs.lean — placeholder for proof files and TODOs.

Next steps for me (after you confirm):
- Finalize the deterministic rule set (you can paste any missing RHS expansions
  for entries that ended with "..." in the wiki). Alternatively I will treat
  those entries as nondeterministic relations and exclude them from the
  deterministic proofs.
- Replace the bounded normalizer with a well-founded recursion and prove
  termination/determinism properties.
- Implement encode/decode to bytes and prove descent_to_bits_faithful.

If you'd like I can also add a small Lean test harness that runs the normalizer
on the entire wiki-emoji stanza and emits a JSON file with the computed normal
form.
