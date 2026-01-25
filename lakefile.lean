import Lake
open Lake DSL

package «meta-meme» where
  version := v!"0.1.0"
  keywords := #["formal-verification", "ai", "muses", "cryptography"]
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩,
    ⟨`autoImplicit, false⟩
  ]

require «doc-gen4» from git
  "https://github.com/leanprover/doc-gen4" @ "main"

@[default_target]
lean_lib MetaMeme where
  srcDir := "src"
  roots := #[`Master, `EigenvectorSharing, `ZKWitnessHME, `RDFaURL]
