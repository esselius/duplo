with import <nixpkgs-unstable> {};

mkShell {
  packages = [
    uv
  ];
  shellHook = ''
    source .venv/bin/activate
  '';
}
