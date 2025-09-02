with import <nixpkgs> {};

mkShell {
  packages = [
    uv
  ];
  shellHook = ''
    source .venv/bin/activate
  '';
}
