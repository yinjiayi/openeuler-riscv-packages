<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-braceexpand

This directory packages upstream `https://github.com/trendels/braceexpand` version `0.1.7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The canonical component is `github.com-trendels-braceexpand`; the source RPM is
`python-braceexpand` and the binary RPM is `python3-braceexpand`, which provides
the former name. The original pure-Python implementation, type annotations and
`py.typed` marker remain enabled. Target Python 3.11 compatibility is pending CI,
not inferred from static review or other upstream interpreter matrix jobs.

## Official source and license

Source0 pins official tag `v0.1.7` at commit
`bb0c73c7a349477ef80d00da703cc72301a96727`, with SHA-256
`0d55d1459f7abbdd9c9681c50ea7efc963b1b2f4fcc18d875b5d81a380762cce`.
All 13 original Git blobs are retained, including the full MIT license, original
test file and test configuration. Fresh official PyPI and tags agree that 0.1.7
is the latest stable release; this is not an older-version workaround.

Frozen AUR, Debian and Ubuntu discovery lineage is retained. The raw AUR row was
stale and labeled GPL3, while the Debian/Ubuntu row held an unknown license for
later official review. Current fixed official `LICENSE` and `setup.py` establish
MIT with the 2015 Stanis Trendelenburg notice; original frozen decisions are not
rewritten or claimed to establish the license. Git records the release commit
as unsigned, not signature-verified; fixed archive SHA-256, all Git blob hashes
and independent official PyPI sdist identity are checked. No source patch.

## Original defaults and installed acceptance

The original Travis job invokes `make test`, whose two commands are the module
entrypoint doctests and `test_braceexpand.py`. `%check` retains both commands,
substituting only the fixed target Python 3 interpreter:

```text
python3 src/braceexpand/__init__.py
python3 test_braceexpand.py
```

The module's original `doctest.IGNORE_EXCEPTION_DETAIL` and nonzero failure exit,
all seven static unittest methods and every original table case remain unchanged.
Seven is a static method count, not an observed runtime result. There are no
third-party default test dependencies. The original setup uses target-supplied
setuptools; no build backend replacement or network install occurs. Tracked
`README.rst` is already present, so the optional Pandoc regeneration rule is not
part of the original default init/test route.

Installed smoke runs in a fresh directory outside the source tree with inherited
`PYTHONPATH` removed. It verifies binary RPM ownership of the imported module,
both typing payload files and the unchanged original test file shipped under
`/usr/share/python-braceexpand/tests/`, then runs the same original module-main
doctests and standalone unittest against installed code. No test exclusion,
weakened assertion, alternate discovery loader or ignored failure.

Complete checksum-bound official and supplemental primary/filelists metadata
were freshly rebound before admission: no matching module/RPM provider, owned
namespace or reverse requirement was found. Python 3.11.6 and setuptools 68.0.0
are supplied by the fixed target repository. Current main managed metadata and
all open PR actual paths are screened separately; final live-head gates remain
mandatory before submission. Static source and trusted repository verification
do not establish RPM build, installed test success, native validation or release.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
