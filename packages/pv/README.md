<!-- SPDX-License-Identifier: Apache-2.0 -->
# pv

This directory packages pv 1.11.0 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. The immutable discovery snapshot is the fixed metadata capture
`discovery-20260808T165000Z-9a89920c269462cd`; it records 1.11.0 in Arch
stable and openSUSE Tumbleweed, Fedora 44 GA at 1.10.4, Ubuntu GA at 1.10.3,
and Debian stable at 1.9.31. An exact-name read-only AUR RPC query on
2026-08-12 returned no result. No AUR or distribution packaging recipe was
read or executed.

Upstream's official page identifies 1.11.0 as current stable. The immutable
Codeberg `v1.11.0` tag resolves to commit
`1fbd9b56a34a50782c317cca91661dcd137453b7`; its archive is SHA-256 pinned.
Pre-extraction inspection found one root, no links or special entries, and no
unsafe path. Upstream declares the source GPL-3.0-or-later.

The complete 52-case upstream suite runs with tmux and valgrind installed, so
terminal-width and memory-safety tests are not omitted. `%check` gives tmux a
fresh HOME whose starter pane is silent; this prevents unrelated user prompt
or shell-integration bytes from contaminating the detached-width measurement
without changing the upstream test. Installed smoke verifies lossless pipe
transfer and numeric completion output. The fixed target provides pv
1.8.5-2.oe2403sp3, so 1.11.0-1 is a higher EVR; every BuildRequires is
present. Target RPM, install, and smoke status remains unknown until
exact-head QEMU CI completes.

Exact-head Package CI run `33704850223` for commit
`1d6b4f7fb6150570cc16192afae7e3314fed8c82` compiled and installed
successfully and retained 10,258 seconds of its build budget. Of the 52
upstream checks, 47 passed and the five failures were exactly the five tests
that source `tests/run-valgrind.sh`. The retained log proves that Valgrind was
installed and accepted the required command-line options; it records neither a
timeout nor a sanitizer diagnostic. However, the individual Automake test logs
and `valgrind.out` were not included, so this evidence cannot distinguish a
QEMU/ptrace interaction from a genuine pv memory defect. Release 2 therefore
keeps all 52 tests and their original failure status, while printing bounded
per-test and Valgrind diagnostics into the retained rpmbuild log on failure.

Release 2 exact-head Package CI run `33707672244` for commit
`cbaff73805392e1fdc0e5d17e82c99db297bd30c` reproduced the same five failures
without a timeout, with 10,279 seconds remaining. The newly retained Automake
logs contained only exit status 1 and no `valgrind.out`. Upstream's helper
writes the actual Valgrind diagnostic to a temporary `workFile4`, copies it to
`valgrind.out` only for the configured memory-error status 125, and otherwise
lets `test-env.sh` delete it on exit. Therefore this run is not evidence of a
reported pv memory error, but it still cannot distinguish a Valgrind startup
failure from another wrapped-command failure. Release 3 adds a downstream
diagnostic-only patch that emits at most 2,000 lines of `workFile4` for every
nonzero status before cleanup. It preserves all 52 tests, Valgrind execution,
the existing status-125 handling, and every real failure status.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
