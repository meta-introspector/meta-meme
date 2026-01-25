{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.gradio
    python3Packages.pip
  ];
  
  shellHook = ''
    echo "🎭 Meta-Meme Gradio Test Environment"
    echo "Run: python app.py"
  '';
}
