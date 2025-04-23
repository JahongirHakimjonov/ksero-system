{
  description = "Dev shell with hello, Go, Python";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        name = "full-dev-env";
        buildInputs = [
          pkgs.go
          pkgs.python3
        ];
        shellHook = ''
          echo "🛠️  Welcome to your full dev shell, Ryan Gosling"
        '';
      };
    };
}

