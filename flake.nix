{
  description = "Meta-Meme Manifold Prover";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            lean4
            elan
          ];

          shellHook = ''
            echo "Meta-Meme Manifold Prover"
            lean --version
          '';
        };

        packages.default = pkgs.stdenv.mkDerivation {
          name = "metameme-manifold";
          src = ./.;
          buildInputs = [ pkgs.lean4 ];
          buildPhase = ''
            lean src/Manifold.lean
          '';
          installPhase = ''
            mkdir -p $out
            cp -r . $out/
          '';
        };
      });
}
