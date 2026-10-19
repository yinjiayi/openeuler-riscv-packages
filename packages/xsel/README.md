<!-- SPDX-License-Identifier: Apache-2.0 -->
# xsel

This directory packages Xsel 1.2.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Its command reads and writes X11 selections; it is not a
Wayland clipboard implementation.

## Source and license

The [official homepage](https://vergenet.net/~conrad/software/xsel/) identifies
the kfish/xsel repository. The fixed official `1.2.1` tag archive is
`https://codeload.github.com/kfish/xsel/tar.gz/refs/tags/1.2.1`, SHA-256
`18487761f5ca626a036d65ef2db8ad9923bf61685e06e7533676c56d7d60eb14`.
All 22 regular members were reviewed without executing upstream code locally.
No detached signature is advertised by the tag source; SHA-256 is mandatory,
not a claim of independently signed provenance.

The program's COPYING and matching C/header notices are
[HPND-sell-variant](https://spdx.org/licenses/HPND-sell-variant.html), which
explicitly lists Xsel's COPYING as a reference; this is not MIT. The original
archive also retains `install-sh` under X11, `aclocal.m4` under FSFULLR,
public-domain `mkinstalldirs`, and `missing` under GPL-2.0-or-later with the
[Autoconf generic exception](https://spdx.org/licenses/Autoconf-exception-generic.html).
These helpers are not linked into the program. The tests subpackage retains
the unmodified archive, all embedded notices and an additional verbatim
official GPL-2.0 license text with its own SHA-256 in sources.yaml; its License
field includes those auxiliary terms conservatively. The downstream checker
has its own HPND-sell-variant copyright/permission notice.

## Build and tests

The fixed tag lacks generated configure/Makefile.in. Standard `autoreconf -fiv`
regenerates machinery before ordinary `%configure`, default make and install.
A minimal DELETE property-format correction is applied as described below; no
feature reduction, command rename, test exclusion or compiler warning suppression
is added. The original configure.ac compiler additions,
Makefile.am, CLI defaults and manual are preserved. In particular, upstream
already adds `-Wno-unused`; packaging does not add or remove that flag.

The generated original Automake `make check` is run unchanged, although this
release declares no TESTS or check_PROGRAMS. Additional downstream checks run
the same checker against staged and normally installed files: fixed archive,
licenses/manual, CLI statuses, private Xvfb PRIMARY/SECONDARY/CLIPBOARD byte
roundtrips, UTF-8, append, one-newline trim, a transfer larger than upstream's
4000-byte incremental threshold, original terminal-direction defaults, clear,
DELETE and explicit display/name. Xvfb allocates a private display with TCP
disabled; bounded foreground owners are reaped. No desktop clipboard is used.
These are functional roundtrips, not exhaustive ICCCM conformance, follow-mode,
clipboard-manager, native desktop, security or performance certification.

BuildRequires come from the current official/supplemental riscv64 repository
metadata (including Autoconf, Automake, pkgconf, libX11-devel and Xvfb); initial
full-name/file namespace admission found no conflict. Actual target DNF solver,
build/default check, installation, physical RPM/SRPM and current-head CI remain
required before merge. Target success is not inferred from local validation.

## Staged license repair

Exact head 4a5617599f7909689d45446c0ada2eb8173fbb99, Package CI
39278514634 attempt 1, compiled and ran the original make check, then failed
the staged checker because the main COPYING file had not yet been copied by
RPM's later percent-license processing. The recipe now installs the exact
original COPYING into the main license directory during percent-install, as
it already did for the test package. The installed license ownership and
byte-for-byte checks remain unchanged. This is a packaging-order correction,
not an upstream source defect; all original tests and downstream scenarios
remain mandatory. New exact-head CI and physical acceptance are still needed.

## DELETE response correction

Package CI 39285513960 attempt 1 at exact head
4e89469fdaef99b651b8b085c7871ad41beb86f5 passed compilation and the original
make check, but its downstream owner cleanup rejected X11 BadValue on stderr.
The original log did not identify the owner's request opcode, so complete runtime
causal confirmation is still pending replacement CI, not inferred from errno text.

Static review identifies a concrete protocol defect in original xsel.c
handle_delete: XChangeProperty receives format 0. The
[Xlib specification](https://x.org/releases/current/doc/libX11/libX11/libX11.pdf)
allows formats 8, 16 or 32, including an empty property. The
[ICCCM DELETE convention](https://www.x.org/releases/X11R7.6/doc/xorg-docs/specs/ICCCM/icccm.pdf)
requires a zero-length response of type NULL. The sole source-line patch changes
format 0 to 8, preserving NULL type, zero elements and deletion behavior. It is
downstream HPND-sell-variant work, not submitted upstream because no upstream
writes are authorized; remove it when a selected official release includes the
correction and all regressions pass. Zero-fuzz source matching is only static
patch validation, not a target test.

Every original downstream scenario and strict stderr failure remains mandatory.
The DELETE regression now explicitly waits for its owner and requires a clean
exit. Cleanup reports each owner PID, argv, selection, input size and completed
checks, preserves any earlier exception, and reaps all owners and the private
server before failing. No error is suppressed or accepted as transient.
Replacement exact-head CI, normal installation, physical RPM/SRPM and fresh
supplier/merge gates remain required; no target success is claimed here.

The first corrected-source head f0da946523ea810787770740938b7af26f185818
failed Package CI 39316372606/1 in percent-prep: GNU patch rejected the
asymmetric context hunk before compilation or QA. That rejection is reproduced
with GNU patch 2.8, despite the prior Apple patch dry-run passing. The hunk is
now regenerated as a standard balanced one-context unified diff, with exactly
the same unique source-line correction. Both GNU and Apple zero-fuzz dry-runs are
required locally; the SPEC and all QA/default commands remain byte-identical.
This is a patch-serialization repair, not a weakened test or new target proof.

## RISC-V assessment

The original C program uses Xlib and POSIX services with no architecture-specific
assembly found in this release. The DELETE correction is architecture-independent,
not a RISC-V workaround. Hosted locked-image
QEMU CI establishes emulated acceptance only; native behavior remains unclaimed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
