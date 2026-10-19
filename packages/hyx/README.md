<!-- SPDX-License-Identifier: Apache-2.0 -->
# Hyx

Official stable release 2026.01.11 from <https://yx7.cc/code/>, archive
<https://yx7.cc/code/hyx/hyx-2026.01.11.tar.xz>, SHA-256
`550863c9e6a2c0e2618c16a562c8ee995e88c1d30e62abfdf4ecb819b3c4df54`.
All 16 regular release files were read without running upstream code.
`license.txt` grants MIT, copyright 2016–2026 Lorenz Panny, and is retained
in both binary subpackages and unchanged in the source archive.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` records Hyx lineage
from AUR, Debian and Ubuntu; no distro recipe is executed. Its homepage-level
`yx7.cc-code` also names the separate Ynetd project. The official project
index and dedicated Hyx release directory disambiguate this component as
`yx7.cc-code-hyx`, not a Ynetd alias.

The original Makefile's default `hyx` target and all editor modes remain.
Upstream has no check/test target; none is represented as an upstream suite.
RPM flags retain assertions. Added `hyx-tests` checks version/help/invalid
arguments and eight bounded offline pseudoterminal (PTY) cases. A PTY is an
operating-system terminal interface used to feed deterministic editor keys,
not a physical terminal. Cases cover replacement/save, undo/redo, empty-file
information, unnamed insert/save, search, special keys in ASCII/command
modes, narrow layout, output bytes, normal exit and restored terminal flags.
Identical checks run on staged and installed binaries. No network or source
compilation is needed by installed checks. Dependencies are libc/POSIX;
Python 3 and Bash for tests are supplied by target repositories.

Patch `0001-bound-terminal-input-and-empty-file-info.patch` is original
MIT-licensed downstream work from static source review. It bounds ctype
inputs for special keys/bytes, avoids empty-file Ctrl-G division by zero and
null-name formatting, and bounds narrow-terminal arithmetic/address shifts.
No test selection or editor feature is removed. No upstream submission is
made, per operator policy. Remove after an official fixed release passes
the same regressions unchanged.

The first target run rejected three patch hunks in `%prep`, before compilation.
The corrected patch encoding is checked with GNU patch at zero fuzz, and its
inert materialized source is byte-equal to the originally intended edits.
Apple patch alone is not sufficient verification for the target patch tool.

Target: openEuler 24.03 LTS SP3 riscv64/RVA23, locked OCI and QEMU user mode.
No local source/RPM/QEMU execution was performed. Build/install/physical
RPM acceptance is pending remote CI. PTY checks do not establish native
hardware, terminal-device, job-control/signal, timing, performance or general
memory-safety claims. No auto-merge or protection bypass.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
