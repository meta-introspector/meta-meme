// Extracted from Coq via MetaCoq
// Automorphic Galois Loop in Rust

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LoopElement {
    Emoji,
    Concept,
    Math,
    Lean4,
    Perf,
    Self_,
}

impl LoopElement {
    pub fn closed_loop(&self) -> Self {
        match self {
            LoopElement::Emoji => LoopElement::Concept,
            LoopElement::Concept => LoopElement::Math,
            LoopElement::Math => LoopElement::Lean4,
            LoopElement::Lean4 => LoopElement::Perf,
            LoopElement::Perf => LoopElement::Self_,
            LoopElement::Self_ => LoopElement::Emoji,
        }
    }

    pub fn iterate(&self, n: u64) -> Self {
        match n {
            0 => *self,
            n => self.iterate(n - 1).closed_loop(),
        }
    }

    pub fn complexity(&self) -> u64 {
        match self {
            LoopElement::Emoji => 0,
            LoopElement::Concept => 10,
            LoopElement::Math => 100,
            LoopElement::Lean4 => 1,
            LoopElement::Perf => 0,
            LoopElement::Self_ => 150,
        }
    }

    pub fn coords_15d(&self) -> [u64; 15] {
        match self {
            LoopElement::Emoji => [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            LoopElement::Concept => [0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 0, 0, 0, 0, 0],
            LoopElement::Math => [0, 10, 0, 0, 0, 0, 0, 100, 100, 100, 0, 0, 0, 0, 0],
            LoopElement::Lean4 => [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            LoopElement::Perf => [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            LoopElement::Self_ => [0, 11, 1, 3, 1, 0, 9, 150, 150, 150, 0, 0, 0, 0, 0],
        }
    }
}

pub const LOOP_COMPLEXITY: u64 = 261;

// Theorem: Loop closes after 6 iterations
pub fn loop_closes() -> bool {
    LoopElement::Emoji.iterate(6) == LoopElement::Emoji
}

// Theorem: Self reached after 5 iterations
pub fn self_at_position_5() -> bool {
    LoopElement::Emoji.iterate(5) == LoopElement::Self_
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_loop_closes() {
        assert!(loop_closes());
    }

    #[test]
    fn test_self_position() {
        assert!(self_at_position_5());
    }

    #[test]
    fn test_complexity_sum() {
        let total: u64 = [
            LoopElement::Emoji,
            LoopElement::Concept,
            LoopElement::Math,
            LoopElement::Lean4,
            LoopElement::Perf,
            LoopElement::Self_,
        ]
        .iter()
        .map(|e| e.complexity())
        .sum();
        assert_eq!(total, LOOP_COMPLEXITY);
    }

    #[test]
    fn test_coords_match_complexity() {
        for elem in [
            LoopElement::Emoji,
            LoopElement::Concept,
            LoopElement::Math,
            LoopElement::Lean4,
            LoopElement::Perf,
            LoopElement::Self_,
        ] {
            assert_eq!(elem.coords_15d()[7], elem.complexity());
        }
    }
}
