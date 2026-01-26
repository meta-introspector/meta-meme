#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};

#[cfg(feature = "wasm")]
pub mod automorphic_loop;

#[cfg(feature = "wasm")]
#[derive(Serialize, Deserialize)]
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct ProofShard {
    id: u32,
    theorem: String,
    proof: String,
    hash: String,
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl ProofShard {
    #[wasm_bindgen(constructor)]
    pub fn new(id: u32, theorem: String, proof: String) -> Self {
        let hash = Self::compute_hash(&theorem, &proof);
        Self { id, theorem, proof, hash }
    }

    fn compute_hash(theorem: &str, proof: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(theorem.as_bytes());
        hasher.update(proof.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    #[wasm_bindgen(getter)]
    pub fn hash(&self) -> String {
        self.hash.clone()
    }
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct ZKWasm {
    proofs: Vec<ProofShard>,
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl ZKWasm {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self { proofs: Vec::new() }
    }

    pub fn add_proof(&mut self, shard: ProofShard) {
        self.proofs.push(shard);
    }

    pub fn verify(&self, hash: &str) -> bool {
        self.proofs.iter().any(|p| p.hash == hash)
    }

    pub fn prove(&self, theorem: &str) -> Option<String> {
        self.proofs.iter()
            .find(|p| p.theorem == theorem)
            .map(|p| p.hash.clone())
    }

    pub fn to_url(&self, base: &str) -> String {
        let hashes: Vec<_> = self.proofs.iter().map(|p| p.hash.as_str()).collect();
        format!("{}?proofs={}", base, hashes.join(","))
    }
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn init() {
    console_error_panic_hook::set_once();
}
