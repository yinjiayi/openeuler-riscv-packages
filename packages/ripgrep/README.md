<!-- SPDX-License-Identifier: Apache-2.0 -->
# ripgrep

This directory packages upstream `https://github.com/BurntSushi/ripgrep` version
`15.2.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official GitHub
tag archive is pinned in `sources.yaml` to SHA-256
`7605249d3eb0d5f170e3414498e3344e26b1e7a147aec518b57090b80036a562`.

The SPEC uses Cargo's locked dependency graph and keeps the target build
network-enabled so CI can retrieve the declared Rust crates. It runs the full
upstream `cargo test --all` suite, installs the `rg` binary, generated man page,
and Bash, Fish, and Zsh completion scripts. The installed smoke test exercises
matching, line numbering, the packaged man page, and a negative search result.

External source and patch licenses remain those of their respective upstream
projects. The repository license covers only original packaging metadata,
scripts, tests, and documentation.
