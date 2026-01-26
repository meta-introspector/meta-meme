use std::path::PathBuf;
use polars::prelude::*;
use walkdir::WalkDir;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("📦 Parquet Discovery (Rust)");
    
    let cache_dirs = vec![
        dirs::home_dir().unwrap().join("meta-introspector"),
        dirs::home_dir().unwrap().join("zos_server"),
        dirs::home_dir().unwrap().join("nix/index"),
        PathBuf::from("/mnt/data1"),
    ];
    
    let mut paths = Vec::new();
    let mut names = Vec::new();
    let mut sizes = Vec::new();
    let mut caches = Vec::new();
    
    for cache_dir in cache_dirs {
        if !cache_dir.exists() { continue; }
        
        println!("🔍 Scanning {:?}...", cache_dir);
        
        for entry in WalkDir::new(&cache_dir)
            .max_depth(5)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().map_or(false, |ext| ext == "parquet"))
        {
            if let Ok(meta) = entry.metadata() {
                paths.push(entry.path().to_string_lossy().to_string());
                names.push(entry.file_name().to_string_lossy().to_string());
                sizes.push(meta.len());
                caches.push(cache_dir.to_string_lossy().to_string());
            }
        }
    }
    
    println!("✅ Found {} parquet files", paths.len());
    
    let df = DataFrame::new(vec![
        Series::new("path", paths),
        Series::new("name", names),
        Series::new("size", sizes),
        Series::new("cache", caches),
    ])?;
    
    let mut file = std::fs::File::create("parquet_index.parquet")?;
    ParquetWriter::new(&mut file).finish(&mut df.clone())?;
    
    println!("✅ Saved parquet_index.parquet");
    println!("{}", df);
    
    Ok(())
}
