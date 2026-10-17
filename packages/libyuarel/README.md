# libyuarel 1.0

Canonical component `github.com-jacketizer-libyuarel`, discovered as the AUR
`libyuarel-git` clue; no AUR code is executed or reused. The independently
verified official stable tag `1.0` resolves to
`a1c9a19c03360909e7d3b9acbb7e0b986efbfb30`. The fixed official archive has SHA-256
`48409f4641827c18720907620aa87f8a4f8ac6c98af9cee22eb484ffd3cd2290`.
All 11 archive files match the complete official Git tree, with no omitted
export-ignore files, submodules or symlinks. The annotated tag and commit are
unsigned; there is no available signature to treat as verified. Full upstream
MIT terms and copyright are shipped under `%license`.

This in-place parser stores pointers into a caller-owned mutable string. It is
not a URL syntax validator, percent decoder or general security validation
library. No RFC conformance, adversarial-input safety, performance, native
RISC-V or concurrency claim is made.

The original default shared library, SONAME `libyuarel.so.1` and public header
remain. A local MIT Makefile patch adds staging and selectable `lib64`, a
relative linker symlink, and omits the upstream install-time `ldconfig` only
when `DESTDIR` is nonempty. The normal default remains `PREFIX=/usr`,
`LIBDIR=lib`, including the unchanged original `make check` target's private
`build/lib` installation. Runtime RPM scriptlets refresh the system loader
cache. RPM compiler/linker flags preserve upstream's shared/SONAME settings
but omit its `-s` stripping so ordinary debug artifacts remain enabled.
There is no library or test-source patch.

The initial target run failed in `%prep`, before compilation: GNU patch with
`--fuzz=0` rejected the first installation hunk. That hunk is now balanced
one-line context around the two added make variables; the installation change
and all original source/tests are unchanged. Validation explicitly uses GNU
`gpatch --dry-run --fuzz=0` as well as `git apply --check`. The initial local
check labelled GNU had actually resolved to Apple's `patch`; its success did
not establish GNU zero-fuzz applicability. A new target run must verify this
repair; the original failed run is not reclassified as successful. The next
target run passed that patch and compilation, then failed in `%install` because
SPEC-only `Source1`/`Source2` entries were not materialized by the repository
staging contract. The separate packaging-only second patch now adds exact
copies of the existing downstream QA files to the unpacked source; installation
uses those files. GNU zero-fuzz application and byte-for-byte comparison verify
the inputs without executing upstream code. No original source, test, default
feature or QA assertion is changed. Fresh target CI is still required; `%check`
was not reached in that failed run.

`%check` executes the original `make check` target used by upstream Travis CI:
all four original groups and their assertions remain byte-identical. The
installed-interface runner recompiles that same suite and the original
`examples/simple.c` against staged/installed headers and shared library,
requires all four group markers and nonzero failures, checks example output,
SONAME, relative symlink and all three dynamic API symbols. A separately
labelled downstream consumer checks representative component/path/query
results, null/error returns and in-place pointer aliasing; it is not an
upstream conformance suite. QA inputs and their checksum manifest ship in
`libyuarel-devel`, which has explicit compiler/tool runtime dependencies.

Build and installation are offline, only inside the locked openEuler
24.03 LTS SP3 riscv64/RVA23 target CI image. Host-side work verifies sources,
patch applicability, metadata, repository tests and golden evaluation only;
no local upstream program, RPM or QEMU build is run. Target CI/build/install
and physical RPM/SRPM/source/debug coexistence acceptance remain required
before merging. Provider inventory/namespace scans are not a DNF solver.

Patch removal: drop the staged-install patch once an official stable release
supports equivalent staging, multilib paths and relative SONAME symlinks.
Drop the downstream QA materialization patch only when the source staging
contract or official source supplies these same installed-interface QA inputs.
