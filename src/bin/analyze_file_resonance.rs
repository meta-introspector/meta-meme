// Plocate file resonance analyzer
// Maps files to 15D Monster manifold based on size and compression

use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

#[derive(Debug, Clone)]
struct FileResonance {
    path: String,
    size: u64,
    conductor: u64,      // size / 1M
    weight: u64,         // size mod 196883 (Leech lattice)
    compression_ratio: f64,
    resonates: bool,     // weight < 10000
    level: u64,          // index in dataset
}

impl FileResonance {
    fn from_size(path: String, size: u64, level: u64) -> Self {
        let conductor = size / 1_000_000;
        let weight = size % 196883;
        let resonates = weight < 10000;
        
        Self {
            path,
            size,
            conductor,
            weight,
            compression_ratio: 0.0,
            resonates,
            level,
        }
    }
    
    fn lmfdb_label(&self) -> String {
        format!("{}.{}.{}", self.conductor, self.weight, self.level)
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Analyzing plocate files for Monster resonance");
    println!("=================================================\n");
    
    let witness_dir = "/mnt/data1/time2/time/2023/07/30/meta-meme/plocate_witness";
    
    // Read file sizes
    let sizes_file = format!("{}/file_sizes.txt", witness_dir);
    let file = File::open(&sizes_file)?;
    let reader = BufReader::new(file);
    
    let mut files: Vec<FileResonance> = Vec::new();
    
    for (level, line) in reader.lines().enumerate() {
        let line = line?;
        let parts: Vec<&str> = line.splitn(2, ' ').collect();
        if parts.len() == 2 {
            if let Ok(size) = parts[0].parse::<u64>() {
                let path = parts[1].to_string();
                files.push(FileResonance::from_size(path, size, level as u64));
            }
        }
    }
    
    println!("📊 Analyzed {} files\n", files.len());
    
    // Statistics
    let total = files.len();
    let resonant = files.iter().filter(|f| f.resonates).count();
    let resonance_rate = resonant as f64 / total as f64;
    
    let min_size = files.iter().map(|f| f.size).min().unwrap_or(0);
    let max_size = files.iter().map(|f| f.size).max().unwrap_or(0);
    let mean_size = files.iter().map(|f| f.size).sum::<u64>() / total as u64;
    
    println!("Size Distribution:");
    println!("  Min: {} bytes", min_size);
    println!("  Max: {} bytes", max_size);
    println!("  Mean: {} bytes", mean_size);
    
    println!("\nMonster Resonance:");
    println!("  Total files: {}", total);
    println!("  Resonant: {} ({:.1}%)", resonant, resonance_rate * 100.0);
    println!("  Non-resonant: {}", total - resonant);
    
    // Top resonances (lowest weight)
    let mut sorted = files.clone();
    sorted.sort_by_key(|f| f.weight);
    
    println!("\n🎯 Top 10 Resonances (closest to Leech lattice):");
    for f in sorted.iter().take(10) {
        println!("  {} bytes, weight={}, label={}", 
                 f.size, f.weight, f.lmfdb_label());
        println!("    {}", f.path);
    }
    
    // Largest files
    sorted.sort_by_key(|f| std::cmp::Reverse(f.size));
    
    println!("\n📏 Top 10 Largest Files:");
    for f in sorted.iter().take(10) {
        let resonance = if f.resonates { "✓" } else { "✗" };
        println!("  {} bytes, weight={}, resonates={}", 
                 f.size, f.weight, resonance);
        println!("    {}", f.path);
    }
    
    // Export to simple format
    let output_file = format!("{}/file_resonance.txt", witness_dir);
    let mut output = String::new();
    for f in &files {
        output.push_str(&format!("{}\t{}\t{}\t{}\t{}\t{}\n",
            f.level, f.size, f.conductor, f.weight, 
            if f.resonates { "1" } else { "0" }, f.path));
    }
    std::fs::write(&output_file, output)?;
    
    println!("\n✅ Saved to: {}", output_file);
    println!("   Ready for Parquet conversion");
    
    Ok(())
}
