// Perf trace to emoji bitmap in Rust + WASM + WebGPU
#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PerfTrace {
    pub cycles: u64,
    pub weight: u64,
    pub emoji: String,
    pub resonates: bool,
    pub coords_8d: [f32; 8],
}

impl PerfTrace {
    pub fn new(cycles: u64, instructions: u64, cache_misses: u64) -> Self {
        let weight = (cycles + instructions + cache_misses) % 196883;
        let resonates = weight < 10000;
        
        let emoji = Self::weight_to_emoji(weight);
        let coords_8d = Self::calculate_8d_coords(cycles, weight, resonates);
        
        Self {
            cycles,
            weight,
            emoji,
            resonates,
            coords_8d,
        }
    }
    
    fn weight_to_emoji(weight: u64) -> String {
        match weight {
            0..=3000 => "⚡".to_string(),
            3001..=5000 => "🚀".to_string(),
            5001..=7000 => "🔥".to_string(),
            7001..=10000 => "💎".to_string(),
            10001..=50000 => "🌊".to_string(),
            _ => "🌀".to_string(),
        }
    }
    
    fn calculate_8d_coords(cycles: u64, weight: u64, resonates: bool) -> [f32; 8] {
        // Map to 8D Monster manifold (first 8 dimensions)
        [
            (cycles / 1_000_000) as f32,           // conductor
            (weight as f32) / 196883.0,            // weight (normalized)
            0.0,                                    // level
            if resonates { 1.0 } else { 0.0 },     // traits
            (weight % 31) as f32 / 31.0,           // key_primes
            0.0,                                    // git_depth
            1.0,                                    // muse_count
            (cycles as f32).log2() / 32.0,         // complexity
        ]
    }
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct Perf2EmojiGame {
    traces: Vec<PerfTrace>,
    camera_pos: [f32; 8],
    camera_vel: [f32; 8],
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl Perf2EmojiGame {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            traces: Vec::new(),
            camera_pos: [0.0; 8],
            camera_vel: [0.0; 8],
        }
    }
    
    pub fn add_trace(&mut self, cycles: u64, instructions: u64, cache_misses: u64) {
        let trace = PerfTrace::new(cycles, instructions, cache_misses);
        self.traces.push(trace);
    }
    
    pub fn update(&mut self, dt: f32) {
        // Update camera position in 8D space
        for i in 0..8 {
            self.camera_pos[i] += self.camera_vel[i] * dt;
        }
    }
    
    pub fn set_camera_velocity(&mut self, dim: usize, vel: f32) {
        if dim < 8 {
            self.camera_vel[dim] = vel;
        }
    }
    
    pub fn get_trace_count(&self) -> usize {
        self.traces.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_perf_trace() {
        let trace = PerfTrace::new(10000, 5000, 100);
        assert_eq!(trace.weight, (10000 + 5000 + 100) % 196883);
        assert!(trace.resonates);
    }
    
    #[test]
    fn test_8d_coords() {
        let trace = PerfTrace::new(1_000_000, 0, 0);
        assert_eq!(trace.coords_8d[0], 1.0); // conductor
    }
}
