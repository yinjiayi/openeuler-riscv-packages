<!-- SPDX-License-Identifier: Apache-2.0 -->
# fzy

This directory packages fzy 1.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable archive for upstream's current
stable `1.1` tag (commit `d811eaf9d73593f8293a73f98a17b36f016873e6`)
and is pinned by a locally calculated SHA-256 in `sources.yaml`. Upstream's
official acceptance test locks ttytest 0.6.0, so the corresponding official
RubyGem is supplied as a SHA-pinned, build-only `Source1`; the build performs
no network access.

Frozen discovery snapshot `discovery-20260812T010000Z-b30-fzy` records Arch
Extra `1.1-1`, AUR `fzy-static` `1.1-2`, Debian stable `1.0-1`, openSUSE
Tumbleweed `1.1-1.5`, and Ubuntu Resolute `1.1-1build1`; Fedora 44 has no fzy
source package in the snapshot. Distribution metadata was used only as
lineage evidence; no distribution recipe was read or executed.

`%check` first runs the complete upstream property/unit executable (32 tests,
102 assertions) and then all 25 maintained TTY acceptance cases through tmux
and ttytest 0.6.0. The second gate checks editing, signals, prompts, scoring,
selection, help, and version behavior; it is not replaced by a noninteractive
smoke. The installed smoke independently exercises `--show-matches` and checks
the selected line.

Installed fzy and ttytest are MIT. Upstream's vendored theft and greatest test
code is ISC, so the source license expression is `MIT AND ISC`. Apache-2.0
covers only this repository's original packaging metadata and scripts.
