{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs_20
    nodePackages.npm
  ];
  
  shellHook = ''
    echo "🌐 Cloudflare Workers Deployment Environment"
    echo "Installing wrangler..."
    npm install -g wrangler 2>/dev/null || true
    export PATH="$HOME/.npm-global/bin:$PATH"
    echo "Ready to deploy!"
  '';
}
