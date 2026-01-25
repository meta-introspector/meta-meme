{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    lean4
    elan
  ];

  shellHook = ''
    echo "Lean4 environment ready"
    lean --version
  '';
}
