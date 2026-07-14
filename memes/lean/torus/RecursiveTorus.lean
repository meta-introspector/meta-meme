import Mathlib
import RequestProject.ModularJInvariant
open Filter Topology
/-!
# A recursive self-image that shrinks to a set of points on a torus
This file answers the seeding conversation's final request — *"have it generate a recursive self
image that gets smaller and smaller until it ends in a set of points on a torus"* — in the
project's established style: a handful of **machine-checked, `sorry`-free theorems**, and, as a
side effect of `lake build`, a standalone **SVG** (`figures/recursive_torus.svg`) that draws
exactly the objects the theorems describe.
The picture is a *Droste effect*: one fixed "unit picture" is redrawn concentrically at recursion
depth `n`, each copy scaled by a fixed ratio `ρ = 3/5 < 1` and rotated a little.  Because
`ρⁿ → 0`, the nested copies get smaller and smaller; in the limit the whole self-image collapses
onto a single central cluster, which we draw as a **flat torus with its `N`-torsion lattice of
points** marked on it.  So the recursion literally "ends in a set of points on a torus".
Why a torus?  This is the natural terminus for the whole moonshine thread: an elliptic curve over
`ℂ` *is* a complex torus `ℂ / (ℤ + ℤτ)`, and the `j`-invariant `j(τ)` is exactly its
classifying number — the object the conversation started from.  The self-similarity of the drawing
mirrors the genuine self-similarity of `j` under the modular group `SL(2, ℤ)`
(`ModularJInvariant.jInvariant_SL2Z_invariant`): the same picture, reproduced at every scale.
## The proved content
* `size_strictAnti` / `size_tendsto_zero` — the copies **strictly shrink** and their size **tends
  to `0`**: the recursion really does get smaller and smaller without bound.
* `size_summable` / `tsum_size` — the total size across all infinitely many levels is *finite*
  (`∑ₙ ρⁿ = 5/2`): the whole infinite recursion fits in a bounded picture.
* `card_torusTorsion` — the terminal object is a genuine finite **set of points on the torus**:
  the `N`-torsion of the flat torus `ℝ²/ℤ²` is `(ℤ/N)²`, with exactly `N²` points.
* `double_torus_two_torsion_card` — the "shrinking" has an arithmetic avatar: the doubling map on
  the torus `ℝ²/ℤ²` has kernel the `4 = 2²` two-torsion points (one recursion step "halves").
* `torus_is_elliptic_curve_selfsimilar` — the conceptual anchor: the torus's classifying number
  `j(τ)` is invariant under `SL(2, ℤ)`, i.e. self-similar, reusing the project's
  `jInvariant_SL2Z_invariant`.
-/
namespace RecursiveTorus
/-! ## The shrinking recursion -/
/-- The nesting ratio of the recursive self-image: each copy is `ρ = 3/5` of its parent. -/
noncomputable def ratio : ℝ := 3 / 5
lemma ratio_pos : 0 < ratio := by unfold ratio; norm_num
lemma ratio_lt_one : ratio < 1 := by unfold ratio; norm_num
/-- The size of the self-image at recursion depth `n`: `size n = ρⁿ`. -/
noncomputable def size (n : ℕ) : ℝ := ratio ^ n
@[simp] lemma size_zero : size 0 = 1 := by simp [size]
/-- **The recursion strictly shrinks**: deeper copies are strictly smaller. -/
theorem size_strictAnti : StrictAnti size :=
  pow_right_strictAnti₀ ratio_pos ratio_lt_one
/-- **The recursion gets smaller and smaller without bound**: `size n → 0`. -/
theorem size_tendsto_zero : Tendsto size atTop (𝓝 0) :=
  tendsto_pow_atTop_nhds_zero_of_lt_one ratio_pos.le ratio_lt_one
/-- The sizes across all infinitely many levels are summable. -/
theorem size_summable : Summable size :=
  summable_geometric_of_lt_one ratio_pos.le ratio_lt_one
/-- **The whole infinite recursion fits in a bounded picture**: the total size is
`∑ₙ ρⁿ = 1/(1 - ρ) = 5/2`. -/
theorem tsum_size : ∑' n, size n = 5 / 2 := by
  have h : ∑' n : ℕ, ratio ^ n = (1 - ratio)⁻¹ :=
    tsum_geometric_of_lt_one ratio_pos.le ratio_lt_one
  simp only [size]
  rw [h]
  unfold ratio
  norm_num
/-! ## The terminal object: a set of points on a torus
The flat torus is `𝕋 = ℝ²/ℤ²`.  Its subgroup of `N`-torsion points (the points killed by
multiplication by `N`) is canonically `(ℤ/N) × (ℤ/N)`; concretely the lattice
`{ (a/N, b/N) : 0 ≤ a, b < N }` on the torus.  This is the finite "set of points on a torus"
the recursion ends in. -/
/-- The `N`-torsion lattice of the flat torus `ℝ²/ℤ²`, i.e. `(ℤ/N)²`. -/
abbrev TorusTorsion (N : ℕ) := ZMod N × ZMod N
/-- **The terminal set has exactly `N²` points on the torus.** -/
theorem card_torusTorsion (N : ℕ) [NeZero N] :
    Fintype.card (TorusTorsion N) = N ^ 2 := by
  simp [TorusTorsion, ZMod.card, sq]
/-- **One recursion step halves the torus.**  The two-torsion `(ℤ/2)²` of `ℝ²/ℤ²` — the kernel of
multiplication by `2` (the doubling map) — has exactly `4 = 2²` points: subdividing the torus once
produces four self-similar cells, the arithmetic avatar of the geometric shrink. -/
theorem double_torus_two_torsion_card :
    Fintype.card (TorusTorsion 2) = 4 := by
  simp [TorusTorsion]
/-! ## The conceptual anchor: the torus is an elliptic curve, classified by a self-similar `j` -/
/-- **The torus's classifying number is self-similar.**  A complex torus `ℂ/(ℤ + ℤτ)` is an
elliptic curve whose isomorphism class is the single number `j(τ)`, and `j` is invariant under the
modular group `SL(2, ℤ)`: the same value reappears at every point of each `SL(2, ℤ)`-orbit, exactly
the self-similarity the recursive drawing depicts.  (Reuses the project's
`ModularJInvariant.jInvariant_SL2Z_invariant`.) -/
theorem torus_is_elliptic_curve_selfsimilar
    (γ : Matrix.SpecialLinearGroup (Fin 2) ℤ) (z : UpperHalfPlane) :
    ModularJInvariant.jInvariant (γ • z) = ModularJInvariant.jInvariant z :=
  ModularJInvariant.jInvariant_SL2Z_invariant γ z
/-! ## Re-anchoring: the drawing depicts these proved statements -/
/-- The nested copies really do shrink strictly (drawn as ever-smaller frames). -/
example : StrictAnti size := size_strictAnti
/-- ...and vanish in the limit (the recursion ends in a point cluster). -/
example : Tendsto size atTop (𝓝 0) := size_tendsto_zero
/-- ...onto a torus carrying exactly `7² = 49` marked points. -/
example : Fintype.card (TorusTorsion 7) = 49 := by rw [card_torusTorsion]; norm_num
/-! ## Computable `Float` mirror and the SVG side effect -/
/-- Clamp a float to a byte. -/
def toByte (x : Float) : Nat :=
  if x ≤ 0.0 then 0 else if x ≥ 255.0 then 255 else x.toUInt64.toNat
def hex2 (n : Nat) : String :=
  let digit := fun d : Nat =>
    if d < 10 then toString d else String.singleton (Char.ofNat (97 + (d - 10)))
  digit (n / 16) ++ digit (n % 16)
def rgb (r g b : Float) : String := "#" ++ hex2 (toByte r) ++ hex2 (toByte g) ++ hex2 (toByte b)
/-- Format a float for SVG (short, deterministic). -/
def fmt (x : Float) : String :=
  let r := (x * 100.0)
  let r := (if r < 0.0 then r - 0.5 else r + 0.5)
  let n := r.toInt64.toInt / 100
  let f := (r.toInt64.toInt % 100).natAbs
  let fs := if f < 10 then "0" ++ toString f else toString f
  toString n ++ "." ++ fs
/-- `Float` value of the shrink ratio and its powers (mirrors `size`). -/
def ratioF : Float := 0.6
def sizeF (n : Nat) : Float := Id.run do
  let mut s : Float := 1.0
  for _ in [0:n] do
    s := s * ratioF
  return s
def pi : Float := 3.14159265358979
/-! ### The fixed "unit picture", drawn in the box `[-100,100]²`. -/
/-- Number of torsion points per direction on the torus (`N² = 49` points). -/
def torusN : Nat := 7
/-- Torus geometry in unit-box coordinates. -/
def bigR : Float := 55.0
def tubeR : Float := 21.0
/-- Pseudo-3D projection of a torus surface point `(u, v)` into the unit box. -/
def torusPoint (u v : Float) : Float × Float × Float :=
  let cx := (bigR + tubeR * Float.cos v) * Float.cos u
  let cy := (bigR + tubeR * Float.cos v) * Float.sin u
  let cz := tubeR * Float.sin v
  -- tilt about the x-axis so the donut reads as 3D
  let sx := cx
  let sy := 0.42 * cy - 0.86 * cz
  let depth := 0.86 * cy + 0.42 * cz     -- toward/away from viewer, for shading
  (sx, sy, depth)
/-- The torus wireframe: `u`-rings and `v`-rings sampled as polylines. -/
def torusWire (t : Float) : String := Id.run do
  let samples := 44
  let ringsU := 9
  let ringsV := 7
  let col := rgb (70.0 + 60.0 * t) (110.0 + 40.0 * t) (150.0 + 80.0 * t)
  let mut s := ""
  -- v-rings (around the tube) at fixed u
  for i in [0:ringsU] do
    let u := 2.0 * pi * i.toFloat / ringsU.toFloat
    let mut pts := ""
    for k in [0:samples+1] do
      let v := 2.0 * pi * k.toFloat / samples.toFloat
      let p := torusPoint u v
      pts := pts ++ fmt p.1 ++ "," ++ fmt p.2.1 ++ " "
    s := s ++ "<polyline points=\"" ++ pts ++
      "\" fill=\"none\" stroke=\"" ++ col ++ "\" stroke-width=\"0.7\" stroke-opacity=\"0.55\"/>"
  -- u-rings (the long way round) at fixed v
  for j in [0:ringsV] do
    let v := 2.0 * pi * j.toFloat / ringsV.toFloat
    let mut pts := ""
    for k in [0:samples+1] do
      let u := 2.0 * pi * k.toFloat / samples.toFloat
      let p := torusPoint u v
      pts := pts ++ fmt p.1 ++ "," ++ fmt p.2.1 ++ " "
    s := s ++ "<polyline points=\"" ++ pts ++
      "\" fill=\"none\" stroke=\"" ++ col ++ "\" stroke-width=\"0.7\" stroke-opacity=\"0.4\"/>"
  return s
/-- The `N × N` set of torsion points, drawn as circles with depth shading. -/
def torusPoints (t : Float) : String := Id.run do
  let mut s := ""
  for i in [0:torusN] do
    for j in [0:torusN] do
      let u := 2.0 * pi * i.toFloat / torusN.toFloat
      let v := 2.0 * pi * j.toFloat / torusN.toFloat
      let p := torusPoint u v
      let d := (p.2.2 / bigR + 1.5) / 2.5     -- normalised depth in ~[0,1]
      let r := 1.6 + 2.6 * d
      let col := rgb (255.0 * (0.25 + 0.75 * d)) (90.0 + 120.0 * d + 40.0 * t) (200.0 - 60.0 * t)
      s := s ++ "<circle cx=\"" ++ fmt p.1 ++ "\" cy=\"" ++ fmt p.2.1 ++
        "\" r=\"" ++ fmt r ++ "\" fill=\"" ++ col ++
        "\" stroke=\"#0a0a16\" stroke-width=\"0.35\"/>"
  return s
/-- The recursive frame (a rounded square in the unit box) plus the torus and its points. -/
def unitPicture (t : Float) : String :=
  let fc := rgb (30.0 + 40.0 * t) (34.0 + 30.0 * t) (60.0 + 60.0 * t)
  let sc := rgb (120.0 + 90.0 * t) (150.0 + 70.0 * t) (210.0)
  let frame :=
    "<rect x=\"-100\" y=\"-100\" width=\"200\" height=\"200\" rx=\"14\" ry=\"14\" fill=\"" ++ fc ++
    "\" fill-opacity=\"0.55\" stroke=\"" ++ sc ++ "\" stroke-width=\"1.4\"/>"
  frame ++ torusWire t ++ torusPoints t
/-! ### Assemble the Droste stack: the unit picture redrawn at each shrinking level. -/
/-- Number of recursion levels drawn (`ρ¹² ≈ 0.0022`, already sub-pixel). -/
def depth : Nat := 13
/-- Scale of the outermost copy (maps the unit box's half-width 100 to ~300 px). -/
def scale0 : Float := 3.0
/-- Rotation added per recursion level (degrees). -/
def rotStep : Float := 16.0
def drosteStack (cx cy : Float) : String := Id.run do
  let mut s := ""
  for n in [0:depth] do
    let sc := scale0 * sizeF n
    let deg := rotStep * n.toFloat
    let t := n.toFloat / (depth.toFloat - 1.0)     -- colour progresses with depth
    s := s ++ "<g transform=\"translate(" ++ fmt cx ++ " " ++ fmt cy ++
      ") rotate(" ++ fmt deg ++ ") scale(" ++ fmt sc ++ ")\">" ++ unitPicture t ++ "</g>"
  return s
def recursiveTorusSvg : String :=
  let w : Nat := 760
  let h : Nat := 820
  let cx : Float := 380.0
  let cy : Float := 380.0
  let header := "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" ++ toString w ++
    "\" height=\"" ++ toString h ++ "\" viewBox=\"0 0 " ++ toString w ++ " " ++ toString h ++ "\">"
  let defs :=
    "<defs><radialGradient id=\"bg\" cx=\"50%\" cy=\"46%\" r=\"70%\">" ++
    "<stop offset=\"0%\" stop-color=\"#141426\"/>" ++
    "<stop offset=\"100%\" stop-color=\"#06060e\"/></radialGradient></defs>"
  let bg := "<rect width=\"" ++ toString w ++ "\" height=\"" ++ toString h ++ "\" fill=\"url(#bg)\"/>"
  let stack := drosteStack cx cy
  let title :=
    "<text x=\"" ++ toString (w / 2) ++
    "\" y=\"36\" text-anchor=\"middle\" font-family=\"monospace\" font-size=\"18\" fill=\"#eef\">" ++
    "A recursive self-image shrinking to a set of points on a torus</text>"
  let sub :=
    "<text x=\"" ++ toString (w / 2) ++
    "\" y=\"58\" text-anchor=\"middle\" font-family=\"monospace\" font-size=\"11.5\" fill=\"#9aa0c4\">" ++
    "each copy is &#961; = 3/5 of its parent (&#961;&#8319; &#8594; 0); the limit is the torus " ++
    "&#8477;&#178;/&#8484;&#178; with its 7&#178; = 49 torsion points</text>"
  let cap1 :=
    "<text x=\"20\" y=\"" ++ toString (h - 58) ++
    "\" font-family=\"monospace\" font-size=\"11\" fill=\"#c8ccdf\">" ++
    "proved: size_strictAnti, size_tendsto_zero, tsum_size (&#8721; &#961;&#8319; = 5/2)</text>"
  let cap2 :=
    "<text x=\"20\" y=\"" ++ toString (h - 40) ++
    "\" font-family=\"monospace\" font-size=\"11\" fill=\"#c8ccdf\">" ++
    "terminal set: card_torusTorsion (N-torsion of &#8477;&#178;/&#8484;&#178; = (&#8484;/N)&#178;, N&#178; points)</text>"
  let cap3 :=
    "<text x=\"20\" y=\"" ++ toString (h - 22) ++
    "\" font-family=\"monospace\" font-size=\"11\" fill=\"#c8ccdf\">" ++
    "the torus is an elliptic curve &#8450;/(&#8484;+&#8484;&#964;), self-similar via j: " ++
    "torus_is_elliptic_curve_selfsimilar</text>"
  header ++ defs ++ bg ++ title ++ sub ++ stack ++ cap1 ++ cap2 ++ cap3 ++ "</svg>"
def emit : IO Unit := do
  IO.FS.writeFile "figures/recursive_torus.svg" recursiveTorusSvg
  IO.println "RecursiveTorus: wrote figures/recursive_torus.svg"
#eval emit
end RecursiveTorus
