<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-grapheme

This directory packages the official final PyPI `grapheme` release `0.6.0` for
openEuler 24.03 LTS SP3, `riscv64`/RVA23. The binary is `python3-grapheme`, import
namespace `grapheme`; it is not the separate C library `libgrapheme` or the
same-namespace updated fork `graphemeu`.

The unsigned official sdist SHA-256 is
`44c2b9f21bbe77cfb05835fec230bd435954275267fea1858013b102f8603cca`.
Upstream has no Git tag for 0.6.0. Fixed official commit
`66f07ca02fc64a9ea2f9b4ad66593b226d473adb` supplies the full original suite and
license missing from the sdist, SHA-256
`1cfb4997d0f3d1c513b19170d7eb7217d26ac6529d4178aaf8ed426471b4842a`.
All 25 Git blobs were checked; all released setup, library and generated Unicode
data bytes match the sdist. The SPEC repeats that match before building.

The full original MIT notice is retained. Bundled Unicode13 data has its own
Unicode copyright, not MIT. The complete official Unicode1991-2020 Data Files
permission notice is pinned from Unicode's ICU66 source and shipped unchanged
as `LICENSE-Unicode-data.txt`; unrelated ICU notices in that original file do
not mean ICU code is included. The original GraphemeBreakTest and property
inputs match the official Unicode13 UCD archive byte for byte.

The default upstream Travis suite runs all pytest tests, then repeats all tests
under coverage with `--source=grapheme`. Both whole commands are preserved;
target `py.test-3.11` and `python3 -m pytest` call `pytest.console_main`, and the
coverage module driver uses the target pytest module name rather than old
`py.test`. Nothing is filtered, skipped or patched: 10 original unittest
methods and 4 parametrized functions over all 602 Unicode13 conformance rows
remain. Benchmark.py is not part of default pytest collection; hosted coveralls
upload is not an offline correctness check and is not claimed here.

The original tests and Unicode-data tree are RPM-owned and repeated after
installation in clean scratch without a source library or PYTHONPATH shadow.
Build inputs use target Python3.11, setuptools68, pytest7.4.4 and coverage7.3.2.
There are no upstream library runtime dependencies; pytest/coverage are runtime
test support for the installed whole suite. Metadata and filelist closure found
no existing Python provider/namespace conflict; `flite`'s C grapheme sonames are
unrelated.

No RISC-V library or test patch is justified. Status stays `unknown` until
exact-head CI proves target build, both source and installed suites, and physical
RPM/SRPM products. Local repository and source-only checks are not target proof.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
