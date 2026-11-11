# NetSurf buildsystem 1.10

Independent official buildsystem release, not the NetSurf browser. The frozen
catalog aggregated their stable lineage; this package retains only the exact
Arch 1.10-3, Fedora 1.10-8.fc44 and openSUSE 1.10-1.7 buildsystem rows. Its own
release index and Makefile component/version establish the separate boundary.

Official source: https://download.netsurf-browser.org/libs/releases/buildsystem-1.10.tar.gz
SHA-256: `3d3e39d569e44677c4b179129bde614c65798e2b3e6253160239d1fd6eae4d79`.
All 30 original regular files and notices remain in the archive; no source patch.
Normal upstream installation installs eight makefile fragments, the Perl test
runner and Jenkins helper. LLVM utilities are not installed as tooling.
No ELF binaries are installed, so no empty debuginfo subpackage is generated;
the example executables remain disposable target checks, not shipped products.

Licenses: root COPYING and the Jenkins helper are MIT; bundled LLVM sources
retain llvm/LICENSE.TXT (NCSA). LicenseRef-Sorttable-2007 denotes the original
llvm/sorttable.js notice, including Stuart Langridge's X11 declaration and Dean
Edwards's embedded MIT notice. The original linked author license page at
https://www.kryogenix.org/code/browser/licence.html explicitly grants MIT terms
to the browser-experiments code. Both original notice-bearing files and COPYING
are installed as licenses; the complete unmodified archive is retained as QA
data and in the SRPM. No unrelated LLVM third-party directories are present.

The original root `make test` is intentionally a dummy target: its successful
exit is not a claim of upstream behavioral coverage. `%check` and installed smoke
retain that target, build the unchanged example with the installed makefiles,
run the original example `test` target, then compile and execute both original
example test drivers against the resulting library. Ten installed tooling files
are byte-compared with the pinned archive, and Perl/shell syntax is checked.
No original tests, source files or default features are removed or rewritten.

Only repository validation runs locally. Real RPM build/install and these target
checks run in CI on openEuler 24.03 LTS SP3 riscv64/RVA23 under QEMU user mode;
they are not native-RISC-V or browser compatibility evidence. Main publication
requires separate verified RPM/SRPM and immutable repository acceptance.
