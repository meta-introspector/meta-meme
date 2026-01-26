use polars::prelude::*;
use std::path::{Path, PathBuf};
use std::process::Command;
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
    git_repo: Option<String>,
    git_commit: Option<String>,
    git_remote: Option<String>,
}

fn get_git_info(file_path: &Path) -> (Option<String>, Option<String>, Option<String>) {
    let mut current = file_path.parent();
    
    // Walk up to find .git directory
    while let Some(dir) = current {
        let git_dir = dir.join(".git");
        if git_dir.exists() {
            let repo_path = dir.to_string_lossy().to_string();
            
            // Get current commit
            let commit = Command::new("git")
                .args(&["-C", &repo_path, "rev-parse", "HEAD"])
                .output()
                .ok()
                .and_then(|o| String::from_utf8(o.stdout).ok())
                .map(|s| s.trim().to_string());
            
            // Get remote URL
            let remote = Command::new("git")
                .args(&["-C", &repo_path, "remote", "get-url", "origin"])
                .output()
                .ok()
                .and_then(|o| String::from_utf8(o.stdout).ok())
                .map(|s| s.trim().to_string());
            
            return (Some(repo_path), commit, remote);
        }
        current = dir.parent();
    }
    
    (None, None, None)
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
    
    let (git_repo, git_commit, git_remote) = get_git_info(path);
    
    Some(ParquetSchema {
        file_path: path.to_string_lossy().to_string(),
        file_name: path.file_name()?.to_string_lossy().to_string(),
        file_size_mb: path.metadata().ok()?.len() as f64 / (1024.0 * 1024.0),
        num_rows: df.height(),
        num_columns: df.width(),
        creator_process: find_creator(&path.to_string_lossy()).to_string(),
        columns: df.get_column_names().iter().map(|s| s.to_string()).collect(),
        git_repo,
        git_commit,
        git_remote,
    })
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🗄️  Parquet Schema Index (Rust + Git)");
    
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
                println!("  📄 {} (git: {})", 
                    schema.file_name,
                    schema.git_repo.as_ref().map(|s| s.as_str()).unwrap_or("none")
                );
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
    let git_repos: Vec<_> = schemas.iter().map(|s| s.git_repo.as_deref().unwrap_or("")).collect();
    let git_commits: Vec<_> = schemas.iter().map(|s| s.git_commit.as_deref().unwrap_or("")).collect();
    let git_remotes: Vec<_> = schemas.iter().map(|s| s.git_remote.as_deref().unwrap_or("")).collect();
    
    let df = DataFrame::new(vec![
        Series::new("file_path", paths),
        Series::new("file_name", names),
        Series::new("file_size_mb", sizes.clone()),
        Series::new("num_rows", rows.clone()),
        Series::new("num_columns", cols),
        Series::new("creator_process", creators),
        Series::new("git_repo", git_repos),
        Series::new("git_commit", git_commits),
        Series::new("git_remote", git_remotes),
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
    let git_tracked = schemas.iter().filter(|s| s.git_repo.is_some()).count();
    
    println!("\n📊 Statistics:");
    println!("  Total files: {}", schemas.len());
    println!("  Total size: {:.2} MB", total_size);
    println!("  Total rows: {}", total_rows);
    println!("  Git tracked: {}/{}", git_tracked, schemas.len());
    
    Ok(())
}
