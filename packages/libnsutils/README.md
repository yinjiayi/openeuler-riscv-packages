# libnsutils 0.1.1

Official stable NetSurf utility library, pinned to the unchanged HTTPS release
archive with SHA-256 `5694b4526e458ed000413ce6027589cbe10a257a7ecf065a01421dc7299dea92`.
All 17 original files and the MIT notice are retained. Discovery lineage is
the frozen Arch extra 0.1.1-2 record; it is not executable source evidence.

The original default static build and original `make test` run are preserved.
A separate shared build runs the same original tests, with no source changes
or test filtering. The now-published NetSurf buildsystem 1.10 is a build
dependency, not vendored or silently substituted.

Both `%check` and post-install smoke compare all six installed headers and
compile the unchanged original `test/base64.c` against installed shared and
static libraries, then run all 32 assertions in unchanged `test/runtest.sh`
for each. QA ships the full original archive; no network is needed for tests.
Shared linkage is checked with readelf. This does not claim native RISC-V or
performance validation. Real RVA23 build/install and RPM/SRPM evidence must
come from CI; local tooling validation alone is not package acceptance.
