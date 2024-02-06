{
  description = "A scraper for web serials that emails to Kindle";

  outputs = { self, nixpkgs }:
  let
    forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "x86_64-darwin" ];
    devPackages = { pkgs }:
      with pkgs; [
        python3Packages.black
        python3Packages.pylint
        python3Packages.venvShellHook
      ];
    runPackages = { pkgs }:
      with pkgs; [
        libxml2
        libxslt
        python3
        python3Packages.beautifulsoup4
        python3Packages.certifi
        python3Packages.click
        python3Packages.feedparser
        python3Packages.google-api-python-client
        python3Packages.google-auth-httplib2
        python3Packages.google-auth-oauthlib
        python3Packages.lxml
      ];
  in
  {
    devShells = forAllSystems (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
      {
        default = pkgs.mkShell {
          NIX_CONFIG = "experimental-features = nix-command flakes";
          venvDir = "./.venv";
          buildInputs = devPackages { inherit pkgs; } ++ runPackages { inherit pkgs; };
        };
      });
    packages = forAllSystems (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
      {
        default = pkgs.python3Packages.buildPythonPackage {
          pname = "serial_scraper";
          version = "1.0.0";
          src = ./.;
          propagatedBuildInputs = runPackages { inherit pkgs; };
        };
      });
    formatter = forAllSystems (system:
      nixpkgs.legacyPackages.${system}.python3Packages.black);
  };
}
