import Lean

/-- rust2lean: Lift Rust code into Lean as macros --/

namespace MetaMeme.Rust2Lean

structure RustFn where
  name : String
  args : List (String × String)
  returnType : String
  body : String
  deriving Repr

syntax "rust_fn!" ident : command

macro_rules
  | `(rust_fn! $name:ident) =>
    `(def $name : IO Unit := do
        IO.println s!"Rust: {$(Lean.quote (toString name.getId))}")

axiom rustLeanEquiv : ∀ (rf : RustFn), True

theorem rustFnValid (rf : RustFn) : True := rustLeanEquiv rf

end MetaMeme.Rust2Lean
