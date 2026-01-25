import Lean

/-- Muses Read and Distribute All Repository Files --/

-- File assignment based on content keywords
structure FileAssignment where
  path : String
  assignedTo : String  -- Which muse
  keywords : List String
  size : Nat
  deriving Repr

-- Keyword patterns for each muse
def calliopeKeywords := ["language", "grammar", "syntax", "parser", "lexer", "token"]
def clioKeywords := ["data", "storage", "persistence", "database", "history", "document"]
def eratoKeywords := ["visual", "graph", "chart", "diagram", "svg", "render"]
def euterpeKeywords := ["interface", "ui", "ux", "design", "web", "html", "css"]
def melpomeneKeywords := ["error", "exception", "fail", "bug", "crash", "panic"]
def polyhymniaKeywords := ["algorithm", "proof", "theorem", "lean", "verify", "formal"]
def terpsichoreKeywords := ["flow", "pipeline", "orchestrate", "workflow", "stream"]
def thaliaKeywords := ["test", "debug", "assert", "check", "validate"]
def uraniaKeywords := ["architecture", "system", "structure", "design", "scale", "infra"]

-- Assign file to muse based on content
def assignFileToMuse (path : String) (content : String) : String :=
  let lower := content.toLower
  if calliopeKeywords.any (fun k => lower.contains k) then "Calliope"
  else if clioKeywords.any (fun k => lower.contains k) then "Clio"
  else if eratoKeywords.any (fun k => lower.contains k) then "Erato"
  else if euterpeKeywords.any (fun k => lower.contains k) then "Euterpe"
  else if melpomeneKeywords.any (fun k => lower.contains k) then "Melpomene"
  else if polyhymniaKeywords.any (fun k => lower.contains k) then "Polyhymnia"
  else if terpsichoreKeywords.any (fun k => lower.contains k) then "Terpsichore"
  else if thaliaKeywords.any (fun k => lower.contains k) then "Thalia"
  else if uraniaKeywords.any (fun k => lower.contains k) then "Urania"
  else "Polyhymnia"  -- Default to algorithms

-- Process all files
def processRepository : IO Unit := do
  IO.println "📚 Muses Reading All Repository Files"
  IO.println "======================================"
  IO.println ""
  
  -- Get all files
  let files ← IO.Process.run { 
    cmd := "find", 
    args := #[".", "-type", "f", "(", "-name", "*.md", "-o", "-name", "*.lean", 
              "-o", "-name", "*.rs", "-o", "-name", "*.ts", "-o", "-name", "*.sh", ")"]
  }
  
  let fileList := files.trim.splitOn "\n" |>.filter (· ≠ "")
  IO.println s!"Found {fileList.length} files to process"
  IO.println ""
  
  -- Count assignments per muse
  let mut assignments : List (String × Nat) := [
    ("Calliope", 0), ("Clio", 0), ("Erato", 0), ("Euterpe", 0), ("Melpomene", 0),
    ("Polyhymnia", 0), ("Terpsichore", 0), ("Thalia", 0), ("Urania", 0)
  ]
  
  -- Process each file
  for file in fileList.take 20 do  -- Sample first 20
    try
      let content ← IO.FS.readFile file
      let muse := assignFileToMuse file content
      IO.println s!"{muse}: {file}"
      
      -- Update count
      assignments := assignments.map fun (m, count) =>
        if m = muse then (m, count + 1) else (m, count)
    catch _ =>
      pure ()
  
  IO.println ""
  IO.println "📊 Distribution Summary:"
  for (muse, count) in assignments do
    if count > 0 then
      IO.println s!"  {muse}: {count} files"

def main : IO Unit := processRepository
