<!-- SPDX-License-Identifier: Apache-2.0 -->
# gifsicle

This directory packages Gifsicle 1.96 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. `Source0` is the immutable current-stable archive linked by
the official Gifsicle release page. Its SHA-256 was calculated locally, and
the archive was audited as a single safe `gifsicle-1.96/` tree with no links,
device nodes, FIFOs, or paths escaping that tree.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `1.96-1`, Fedora 44 GA `1.96-3.fc44`, openSUSE Tumbleweed
`1.96-1.6`, Debian 13.6 stable `1.96-1`, and Ubuntu 26.04 LTS GA
`1.96-1build1`. A read-only AUR RPC name search observed only the development
alias `gifsicle-git` (`1.93.r0.g416518e-1`) plus an unrelated Python wrapper;
no AUR recipe or distribution build script was fetched or executed.

The build keeps all three upstream programs: `gifsicle`, `gifdiff`, and the
X11 viewer `gifview`. `%check` runs the release archive's complete Testie
suite: 11 maintained image transformation and regression cases, with zero
failures and zero skips. The installed smoke independently creates a minimal
GIF, optimizes it, compares visual output, inspects metadata, and checks all
three installed program versions without requiring an X server.

The source is `GPL-2.0-only`; upstream also states a separate restricted
alternative grant, but this package is distributed under GPL-2.0-only.
Apache-2.0 covers only this repository's original packaging metadata and
smoke script.
