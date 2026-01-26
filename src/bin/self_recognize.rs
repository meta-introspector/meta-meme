// Self-recognition: Automorphic loop ingests its own perf traces
use std::fs::File;
use parquet::file::reader::{FileReader, SerializedFileReader};
use parquet::record::RowAccessor;

const LEECH_MOD: u64 = 196883;

#[derive(Debug)]
struct TraceSignature {
    label: String,
    cycles: u64,
    weight: u64,
    resonates: bool,
}

fn ingest_trace(cycles: u64, instructions: u64, cache_misses: u64) -> u64 {
    (cycles + instructions + cache_misses) % LEECH_MOD
}

fn main() {
    println!("=== Automorphic Self-Recognition (Rust) ===\n");
    
    // Load own perf traces
    let file = File::open("plocate_witness/automorphic_traces.parquet")
        .expect("Failed to open traces");
    let reader = SerializedFileReader::new(file).expect("Failed to create reader");
    
    let mut traces = Vec::new();
    
    // Read all traces
    let iter = reader.get_row_iter(None).expect("Failed to get rows");
    for row_result in iter {
        let row = row_result.expect("Failed to read row");
        
        let label = match row.get_string(0) {
            Ok(s) => s.to_string(),
            Err(_) => "unknown".to_string(),
        };
        
        let cycles = match row.get_long(2) {
            Ok(v) => v as u64,
            Err(_) => 0,
        };
        
        let weight = match row.get_long(7) {
            Ok(v) => v as u64,
            Err(_) => 0,
        };
        
        let resonates = match row.get_bool(8) {
            Ok(v) => v,
            Err(_) => false,
        };
        
        traces.push(TraceSignature { label, cycles, weight, resonates });
    }
    
    println!("Loaded {} traces\n", traces.len());
    
    // Self-recognition: Calculate weight of each trace
    println!("Ingesting traces:");
    let mut self_weights = Vec::new();
    
    for trace in &traces {
        // Ingest the trace itself (self-referential)
        let self_weight = ingest_trace(trace.cycles, trace.weight, 0);
        let self_resonates = self_weight < 10000;
        
        println!("  {} -> weight={} resonates={}", 
                 trace.label, self_weight, self_resonates);
        
        self_weights.push(self_weight);
    }
    
    // Find self: trace that resonates when ingested
    println!("\n=== Self-Recognition ===");
    
    let resonant_count = self_weights.iter().filter(|&&w| w < 10000).count();
    println!("Resonant when ingested: {}/{}", resonant_count, traces.len());
    
    if let Some((idx, &weight)) = self_weights.iter().enumerate().find(|(_, &w)| w < 10000) {
        println!("\nSELF IDENTIFIED:");
        println!("  Label: {}", traces[idx].label);
        println!("  Original weight: {}", traces[idx].weight);
        println!("  Self-ingested weight: {}", weight);
        println!("  Resonates: YES");
        println!("\n✓ Automorphic loop recognized itself!");
    } else {
        println!("\nAll traces converging...");
        
        // Find closest to resonance
        let min_weight = self_weights.iter().min().unwrap();
        let min_idx = self_weights.iter().position(|&w| w == *min_weight).unwrap();
        
        println!("Closest to self-recognition:");
        println!("  Label: {}", traces[min_idx].label);
        println!("  Self-ingested weight: {}", min_weight);
        println!("  Distance from resonance: {}", min_weight - 10000);
    }
}
