{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    coq_8_18
    (coqPackages_8_18.metacoq.override { })
    linuxPackages.perf
  ];
}
