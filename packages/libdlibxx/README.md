# libdlibxx 1.1.0

Official stable tag `v1.1.0` resolves to
`bbf532ad6b1d9c9cd350d9b83c73a8aff156a49e`; its fixed official commit archive
has SHA-256 `d3236abed9b11d09eb32c5d253986d06f62afbf18ba223cd1ce231cb65594329`.
All 17 regular source files match the official recursive Git tree byte-for-byte;
there are no gitlinks or archive links. The annotated tag is unsigned. The full
BSD-2-Clause LICENSE is retained; examples/source are governed by that project
license. AUR metadata is discovery lineage, not executed packaging authority.

The default shared library, C++11 setting, original SONAME `1.0.0`, original demo
and all three original plugin libraries remain enabled. Upstream has no CTest
registration or authored automated test suite. The original interactive demo is
run offline with all three documented plugin paths and EOF, both as originally
built and recompiled against staged/installed headers and library. The additional
simple example is also preserved and replayed with its supported a/b factories.
Plugin a intentionally defines C++-mangled `bin_op`; b has no `bin_op`; c exposes
C `bin_op` but no factory. Their original success/failure outputs are checked,
not silently interpreted as a uniform success interface.

Additional downstream API checks fail nonzero on wrong handle/error state,
factory identities, missing factories/symbols, filename, lazy/now resolution,
constructor loading, close state, or positive/negative integer sums. These are
downstream checks, not upstream suite/native validation. Original example bytes
are installed with SHA-256 replay checks. Runtime compiler/Boost headers are
declared because installed acceptance recompiles the unchanged examples and
consumer; it does not download or invoke upstream during local preparation.

The sole package-local BSD-2-Clause patch replaces hardcoded install destinations
with GNUInstallDirs, permitting relative `lib64`. It does not alter algorithm,
library features, SONAME, examples or test bodies. It is downstream-only, not
submitted upstream; remove when an official stable release honors the same
multilib variables. Debug flags and standard RPM debug subpackages remain enabled.

Complete fresh official openEuler and public supplemental primary/filelists
joins found no package/capability/path namespace collision and no missing provider
in the declared dependency closure. Non-equality version bounds are retained for
real DNF resolution, not claimed solved locally. Build/install/debug-subpackage
coexistence on the exact locked openEuler RVA23 riscv64 image remains a hosted-CI
and physical-artifact gate. No local target execution or native success claimed.
