use polars::prelude::*;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct ParquetSchema {
    file_path: String,
    file_name: String,
    file_size_mb: f64,
    num_rows: usize,
    num_columns: usize,
    creator_process: String,
    columns: Vec<String>,
}

fn should_exclude(path: &str) -> bool {
    ["test", "pyarrow/tests", "pandas/tests", ".venv", "site-packages"]
        .iter()
        .any(|p| path.contains(p))
}

fn find_creator(path: &str) -> &'static str {
    if path.contains("toolchain-analysis") { "toolchain-analysis" }
    else if path.contains("rust_lattice") { "rust-lattice-analyzer" }
    else if path.contains("markov") { "markov-model-builder" }
    else if path.contains("nix-controller") { "nix-controller" }
    else if path.contains("perf") { "performance-profiler" }
    else if path.contains("nix_build") { "nix-build-logger" }
    else if path.contains("meta-introspector") { "meta-introspector" }
    else if path.contains("meta-meme") { "meta-meme-generator" }
    else { "unknown" }
}

fn scan_parquet(path: &Path) -> Option<ParquetSchema> {
    let df = LazyFrame::scan_parquet(path, Default::default()).ok()?.collect().ok()?;
    
    Some(ParquetSchema {
        file_path: path.to_string_lossy().to_string(),
        file_name: path.file_name()?.to_string_lossy().to_string(),
        file_size_mb: path.metadata().ok()?.len() as f64 / (1024.0 * 1024.0),
        num_rows: df.height(),
        num_columns: df.width(),
        creator_process: find_creator(&path.to_string_lossy()).to_string(),
        columns: df.get_column_names().iter().map(|s| s.to_string()).collect(),
    })
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🗄️  Parquet Schema Index (Rust)");
    
    let dirs = vec![
        dirs::home_dir().unwrap().join(".local/share/toolchain-analysis"),
        dirs::home_dir().unwrap().join("nix-controller/data"),
        dirs::home_dir().unwrap().join("meta-introspector"),
        PathBuf::from("/mnt/data1/time2/time/2023/07/30/meta-meme"),
    ];
    
    let mut schemas = Vec::new();
    
    for dir in dirs {
        if !dir.exists() { continue; }
        println!("📂 Scanning {:?}...", dir);
        
        for entry in WalkDir::new(&dir)
            .max_depth(3)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().map_or(false, |ext| ext == "parquet"))
        {
            let path_str = entry.path().to_string_lossy();
            if should_exclude(&path_str) { continue; }
            
            if let Some(schema) = scan_parquet(entry.path()) {
                println!("  📄 {}", schema.file_name);
                schemas.push(schema);
            }
        }
    }
    
    println!("\n✅ Found {} parquet files", schemas.len());
    
    // Create index DataFrame
    let paths: Vec<_> = schemas.iter().map(|s| s.file_path.as_str()).collect();
    let names: Vec<_> = schemas.iter().map(|s| s.file_name.as_str()).collect();
    let sizes: Vec<_> = schemas.iter().map(|s| s.file_size_mb).collect();
    let rows: Vec<_> = schemas.iter().map(|s| s.num_rows as i64).collect();
    let cols: Vec<_> = schemas.iter().map(|s| s.num_columns as i64).collect();
    let creators: Vec<_> = schemas.iter().map(|s| s.creator_process.as_str()).collect();
    
    let df = DataFrame::new(vec![
        Series::new("file_path", paths),
        Series::new("file_name", names),
        Series::new("file_size_mb", sizes),
        Series::new("num_rows", rows),
        Series::new("num_columns", cols),
        Series::new("creator_process", creators),
    ])?;
    
    // Save
    let mut file = std::fs::File::create("parquet_schema_index.parquet")?;
    ParquetWriter::new(&mut file).finish(&mut df.clone())?;
    println!("✅ Saved parquet_schema_index.parquet");
    
    // Save JSON
    std::fs::write("parquet_schemas.json", serde_json::to_string_pretty(&schemas)?)?;
    println!("✅ Saved parquet_schemas.json");
    
    // Stats
    let total_size: f64 = sizes.iter().sum();
    let total_rows: i64 = rows.iter().sum();
    println!("\n📊 Statistics:");
    println!("  Total files: {}", schemas.len());
    println!("  Total size: {:.2} MB", total_size);
    println!("  Total rows: {}", total_rows);
    
    Ok(())
}
