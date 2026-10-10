# python-stringcase

Stringcase converts strings among common naming conventions. This package targets
only openEuler 24.03 LTS SP3, riscv64/RVA23 with the repository's locked image.

## Official release and discovery identity

Official PyPI lists 1.2.0 as the latest stable release. Its SHA-256-verified sdist
omits tests. Source0 is therefore the complete official Git archive at fixed commit
`be60b723753d4796983729d49ef825826e0f882d` (SHA-256
`f0cb19e5fb6496426da7af7cf5a44a140212eefe12128ca6d982f3131060ccf2`).
All 12 archive files match the official Git blob identities. Its LICENSE,
README.rst, setup.cfg, setup.py and stringcase.py match the five non-generated
sdist members byte-for-byte; both setup.py and generated PKG-INFO declare 1.2.0.
This establishes release-associated source identity, not a Git tag or an inference
from commit time. No detached upstream signature is supplied.

The frozen `discovery-20260808T165000Z-9a89920c269462cd` Ubuntu resolute/universe
row `python-stringcase` is a discovery clue. Its version
`1.2.0~git20230617.57aae96-1` is retained verbatim in lineage, not adopted as a
stable upstream release. Independent source review maps the unknown raw component
to `github.com-okunishinishi-python-stringcase`. This is not an AUR claim.

## Dependencies and ownership

The unmodified distutils setup declares a single `stringcase` module and no runtime
dependencies; inert import inspection finds only standard-library `re`.
Builds use offline pip with target Python 3.11 and setuptools/wheel, no dependency
download. Target official metadata supplies python3-devel 3.11.6,
setuptools 68.0.0, wheel 0.40.0, pip 23.3.1 and coverage 7.3.2.
Full current official and supplemental primary/filelists scans found no package,
normalized capability or site-packages namespace ownership conflict. Supplemental
HTTP state/checksum binding proves inventory freshness, not runner trust or release
acceptance. MIT copyright and permission notices are installed unchanged. Packaging
is repository-authored under Apache-2.0; no distro/AUR recipe was copied or executed.

## Narrow source repair

Original `test_alphanumcase` requires `alphanumcase(None) == 'None'`, but the
released function passes None directly to `re.sub`, which rejects non-string
input. Patch0 only wraps that input in `str()`, as other converters already do.
This is a source-contract repair, not a RISC-V workaround or a removed test.
The patch was authored against the fixed official MIT source, contains no
borrowed distro recipe, and has not been submitted upstream. Remove it after a
verified stable release normalizes this input and passes its unchanged default
suite without the patch. Inert dry-run/apply and AST review verify the one-line
change; actual target execution remains required.

## Original default acceptance

The fixed source's Travis script runs `python -m unittest -v stringcase_test.py`,
`coverage run -m unittest stringcase_test` and
`coverage html -d docs/report/coverage/`. `%check` preserves all three (coverage's
module entry point is equivalent to its CLI), with no filters, skips or ignored
failures, and adds a 13-test/zero-skip completeness assertion. Upstream specifies no
coverage percentage threshold or separate lint/documentation test gate. Its
`after_success: coveralls` is external post-success reporting, not a test gate;
this recipe never publishes upstream or uses the historical encrypted Travis value.
Tracked historical `.coverage` is not reused: every target check and installed
acceptance uses a freshly allocated directory and dedicated `COVERAGE_FILE`.

The smoke test reruns the unchanged complete original suite and coverage report
from a new directory containing only the test module, and checks that `stringcase`
resolves to the installed RPM in `/usr/lib/python3.11/site-packages/` at version
1.2.0. No upstream source/backend/tests or local RPM/QEMU build was executed during
preparation. Pure string conversion tests do not require native timing/hardware;
target build/install status remains **unknown** until exact-head CI validates it.
No auto-merge, package merge or public release is claimed.
