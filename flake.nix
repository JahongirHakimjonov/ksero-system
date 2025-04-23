{
  description = "Dev shell with hello, Go, Python";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        pypdf2     # <-- lowercase
        pywin32
        colorlog
        pillow
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        name = "full-dev-env";
        buildInputs = [
          pkgs.go
          pythonEnv
        ];
        shellHook = ''
          echo "🛠️  Welcome to your full dev shell, Ryan Gosling"

          # Install pytwain via pip, since it's not in nixpkgs
          python -m ensurepip --upgrade
          pip install --user pytwain
        '';
      };
    };
}
