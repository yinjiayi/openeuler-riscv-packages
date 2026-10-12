# python-case-converter

Official stable Case-converter 1.2.0, distribution `case-converter` and import
module `caseconverter`. AUR discovery lineage identifies the candidate only;
neither an AUR recipe nor a distribution binary is used as upstream source.

The complete official tag resolves to commit
`c37a1240f08b0f8ec1963910fdfda23b51f013a1`. Its full archive SHA-256 is
`11ffdc0901540df4d994bfac96fdb9a576f136ca7b01c75ecb17b55b73e4afce`.
All 28 Git blobs were retained and verified; the 23 shared source blobs match
the independently verified official PyPI 1.2.0 sdist. The Git archive also
includes the original Makefile and GitLab CI, which the sdist omits. The
unchanged upstream MIT LICENSE governs the package. No patch is required.

`make coverage` means the original full `python3 -m pytest --cov-report=term
--cov=caseconverter **/*_test.py`, not a selected smoke subset. All nine original
test modules, 11 test functions and 95 literal parameter cases remain
unchanged. These are static source counts; actual collection, execution and
coverage must be established by target CI. No test skip or xfail was added.

`make package` means the original isolated `python3 -m build`, including its
default sdist-to-wheel path; no `--no-isolation` override is used. Build and
installed verification use the fixed official target `/usr/share/python-wheels`
providers: `python-pip-wheel` 23.3.1, `python-setuptools` 68.0.0 and
`python-wheel-wheel` 1:0.40.0. Their complete RPM payloads, wheel metadata and
licenses were inspected inertly; Python 3.11's actual ensurepip resolves that
directory and bootstraps without an index. Backend isolation inherits the
offline wheelhouse. These distribution wheels are dependencies, not extra
upstream source archives or locally executed tools. The source has no
pyproject.toml; the target build frontend's unchanged legacy backend requires
setuptools >=40.8.0 and wheel. Twine upload/release commands are publication
context, not part of this package's target build or test acceptance.

The RPM retains exactly the original 28 source files for audit and offline
rebuilding. Installed verification checks their SHA-256 values and ownership,
checks every installed original module/test file against those same values,
then runs unchanged `make coverage` against a symlink to the real RPM-owned
installed package from fresh scratch space. A separate fresh copy of the
RPM-owned original source runs unchanged `make package` offline. No copied
runtime source shadows the installed-test import.

Whole current target metadata was checked for canonical package/module
collisions and full dependency closure. Provider version bounds are a static
feasibility check, not a successful DNF transaction or riscv64 build. No local
upstream code, backend, default tests, RPM or QEMU build was executed. Target
status remains unknown until exact-head package CI proves source verification,
build, whole original defaults, installation and physical RPM/SRPM artifacts.
