-- Reduction.lean
-- Small helpers and example tests for the reduction engine.

import OdeToRaoulBott

open OdeToRaoulBott

/-- Example helper that tokenizes a whitespace-separated emoji line into tokens.
    For the wiki we will likely need a more robust tokenizer; this is a start. -/

def tokenize (s : String) : List String :=
  s.splitOn " "

#eval tokenize "🎭🔮🎶 🔑 🌌 🌠🎵 🔑📜"

/-- Example: compute the normal form of the first line of the emoji stanza. -/

def exampleInput : List String := tokenize "🎭🔮🎶 🔑 🌌 🌠🎵 🔑📜"

#eval normalize exampleRules exampleInput
