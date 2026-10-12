# readline

This directory packages GNU Readline 8.3 with official patch level 003 for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Core, AUR metadata-only derivatives, Debian stable, and Fedora
44. No distribution or AUR packaging content was executed.

The base archive and all three patch-level files come from GNU's official
Readline directory. Each byte stream is independently SHA-256 pinned in
`sources.yaml`; the archive has one `readline-8.3/` root and no unsafe paths.
`COPYING` contains GPL-3.0-or-later terms, which also cover the official
patches.

The RPM builds shared Readline and History libraries against ncurses, applies
the official patches in order, checks patch level 3, preserves the upstream
root and examples check routes, and compiles an installed API smoke program.
The upstream root check target is empty; the examples check builds and runs
the upstream version program. Its required static library is built only for
testing and is not installed or packaged. The examples directory is on PATH
for the original check, and an additional exact 8.3 assertion prevents its
echo command from hiding a failed version invocation. The patch-level check
preserves the official three-line file and asserts its final numeric line,
rather than comparing the header and number together against 3. All build
and test phases are offline. Target CI success is required after refresh.
