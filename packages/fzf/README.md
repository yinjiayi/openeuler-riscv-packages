<!-- SPDX-License-Identifier: Apache-2.0 -->
# fzf

This directory packages the upstream `https://github.com/junegunn/fzf` release
`0.74.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI downloads the
official tag archive over HTTPS and verifies the SHA-256 recorded in
`sources.yaml` before the network-enabled target build.

fzf is a command-line fuzzy finder. The RPM builds the Go command with the
reviewed version and a reproducible source revision, and installs `fzf`, the
`fzf-tmux` helper, both manual pages, Bash and Zsh completion files, Fish and
shell key-binding scripts, the preview helper, and the Vim plugin. `%check`
runs the upstream Go unit-test targets with `FZF_VERSION` and `FZF_REVISION`
explicitly supplied because release archives do not contain Git metadata. The
installed smoke test uses `--filter` for deterministic non-interactive matching
and verifies the integration files.

The release archive is pinned to SHA-256
`5b142217c3068647a7d8faa9c678cffada100b5f11a48609aa79c94ce04b28ef`, as
reviewed in `catalog/upstream-releases.yaml`. No distribution recipe or AUR
content is executed during discovery or build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
