use serde::{Deserialize, Serialize};
use std::process::Command;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize)]
struct DatasetRegistry {
    meta_datasets: MetaDatasets,
}

#[derive(Debug, Serialize, Deserialize)]
struct MetaDatasets {
    name: String,
    version: String,
    datasets: Vec<Dataset>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Dataset {
    id: String,
    org: String,
    repo: String,
    #[serde(rename = "type")]
    dataset_type: String,
    url: Option<String>,
    git_url: Option<String>,
    path: Option<String>,
    files: Option<Vec<String>>,
    size_mb: f64,
    rows: usize,
    purpose: String,
    required: bool,
}

fn clone_hf_dataset(dataset: &Dataset, target_dir: &str) -> Result<(), Box<dyn std::error::Error>> {
    if let Some(git_url) = &dataset.git_url {
        let clone_path = format!("{}/{}", target_dir, dataset.id);
        
        if Path::new(&clone_path).exists() {
            println!("  ✅ Already cloned: {}", dataset.id);
            return Ok(());
        }
        
        println!("  📥 Cloning {} from {}", dataset.id, git_url);
        
        let output = Command::new("git")
            .args(&["clone", git_url, &clone_path])
            .output()?;
        
        if output.status.success() {
            println!("  ✅ Cloned: {}", dataset.id);
        } else {
            eprintln!("  ❌ Failed to clone: {}", dataset.id);
        }
    }
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("📦 Dataset Cloner (Rust + Git)");
    println!("==================================================");
    
    // Load registry
    let registry_json = std::fs::read_to_string("../datasets_registry.json")?;
    let registry: DatasetRegistry = serde_json::from_str(&registry_json)?;
    
    println!("\n📋 Registry: {}", registry.meta_datasets.name);
    println!("   Version: {}", registry.meta_datasets.version);
    println!("   Datasets: {}", registry.meta_datasets.datasets.len());
    
    // Create datasets directory
    let target_dir = "../datasets";
    std::fs::create_dir_all(target_dir)?;
    
    // Clone required datasets
    println!("\n🔄 Cloning required datasets...");
    for dataset in &registry.meta_datasets.datasets {
        if dataset.required && dataset.dataset_type == "dataset" {
            clone_hf_dataset(dataset, target_dir)?;
        }
    }
    
    // Summary
    println!("\n📊 Summary:");
    for dataset in &registry.meta_datasets.datasets {
        let status = if dataset.dataset_type == "local" {
            "📁 Local"
        } else if Path::new(&format!("{}/{}", target_dir, dataset.id)).exists() {
            "✅ Cloned"
        } else {
            "⏳ Pending"
        };
        
        println!("  {} {}: {} ({:.2} MB, {} rows)", 
            status, dataset.id, dataset.purpose, dataset.size_mb, dataset.rows);
    }
    
    Ok(())
}
