{
  description = "Dev shell with Go, Python, and some pip-installed extras";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python3;
      pythonEnv = python.withPackages (ps: with ps; [
        pypdf2
        colorlog
        pillow
        virtualenv  # <-- kerakli
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

          # virtualenv yaratish
          if [ ! -d ".venv" ]; then
            python -m virtualenv .venv
          fi

          source .venv/bin/activate

          # pip install only if not installed
          if ! pip show pytwain >/dev/null 2>&1; then
            pip install pytwain
          fi
        '';
      };
    };
}
