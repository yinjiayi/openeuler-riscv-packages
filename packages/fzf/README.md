<!-- SPDX-License-Identifier: Apache-2.0 -->
# fzf

This directory packages the upstream `https://github.com/junegunn/fzf` release
`0.74.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI downloads the
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
`5529d08897b85ae773695787c811ff9c9eeee32419c8a297fa1dbe586ed0a27e`.
The official `v0.74.5` annotated tag resolves to commit
`c0a193e031f01fb50bf6f7be4381990a3753f7cf`; every archive file was checked
against that commit's Git blob. The safe `fzf-0.74.5/` source root contains
30 original Go test files. The previous update input was an Android arm64
binary attachment, not buildable source. This correction preserves the
original Makefile test target and installed files. The first corrected-source
CI run built and installed 0.74.5, but its smoke test still expected the old
literal 0.74.3. The version assertion now compares the complete source-build
version string against the installed RPM's VERSION metadata; the filter and
all integration-file checks remain unchanged. This is a test-expectation fix,
not a skipped check or a claim of a passing new-head installation. New-head target
build/install results remain CI acceptance gates; source verification alone
does not prove target build success. No distribution recipe or AUR content
is executed during discovery or build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
