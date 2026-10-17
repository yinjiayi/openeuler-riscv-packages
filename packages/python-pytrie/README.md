# python-pytrie 0.4.0

PyTrie is the official `gsakkis/pytrie` pure Python trie implementation. The
latest non-yanked stable PyPI release is 0.4.0. Source0 pins its original Git
tag's commit `d88f261d4e9c7046233f005034d7e15575bd30df`; all 34 regular Git
blobs match the fixed archive, and shared files match the official PyPI sdist.
No archive, upstream code or patch is committed here.

The frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
retains original Arch `python-pytrie`, Debian/Ubuntu `python-trie` and openSUSE
`python-PyTrie` lineage and its historical unverified-upstream decision.
Fresh official source verification resolves intake eligibility without rewriting
those discovery records. Target primary/filelists were scanned completely:
18,503 official and 1,192 supplemental entries, with fresh unchanged state and
repomd bindings, expose no existing PyTrie package/module provider or owner.

## Build and original tests

Retain the original setuptools backend and `setup.py test` with the unchanged
`test_suite='tests'`. This discovers both `tests/test_trie.py` and
`tests/test_mapping.py`, including inherited CPython mapping protocol tests.
Nothing is filtered, skipped or replaced. The target's Python 3.11.6
`python3-devel` provides `python3-test` and owns `test/mapping_tests.py`;
setuptools 68.0.0, wheel 0.40.0, pip 23.3.1 and sortedcontainers 2.4.0 are
available as target RPMs. The upstream release defines no pyproject, tox or
additional CI gates. Build and tests require no dependency downloads.

The installed smoke test imports only the system installed module under isolated
Python, verifies distribution identity and representative mapping/prefix behavior.
It supplements, never replaces, the complete upstream `%check` suite.

## Complete source and embedded-resource notices

Original PyTrie code is BSD-3-Clause, copyright 2009 George Sakkis. Preserve its
entire LICENSE and all source/docs/assets; do not remove generated resources.
The immutable source includes older Sphinx 0.6.3 HTML pages alongside Sphinx 1.5
pages and refreshed static assets. The active Sphinx asset bytes match official
Sphinx 1.5: PNGs/default CSS are exact, basic CSS uses its original width value,
and doctools/searchtools match its templates and static English stemmer,
stopwords and full Unicode splitter tables. Sources1/2 supply unmodified Sphinx
1.5 LICENSE/AUTHORS from commit `9f3a95e1da6c8a026df0b197e9d941f963341c38`.

Embedded jQuery 3.1.0 is byte-identical to its official release and the Sphinx
bundle. Source3 supplies its complete MIT grant from jQuery commit
`d0d2d9b9b004cf0c6763c871646e01ca67579253`.

All 63 generated Pygments token CSS rules correspond to official Pygments 2.1.3
FriendlyStyle plus the original SphinxStyle overrides. The precise original
Pygments generator version is not known; this is a static style/content
correspondence, not a claim that it was regenerated or that its version is known.
Sources4/5 supply the full unmodified BSD-2-Clause LICENSE/AUTHORS from Pygments
commit `4d8dbbb7861f6f8a78a952d5bcc3e7a9f5940675`. Sphinx's complete combined
LICENSE also preserves its incorporated-software grants. Every supplemental
notice is SHA-256 checked, retained in the SRPM sources and installed with
`%license`; the original HTML docs are installed without modification.

No upstream signatures were advertised for these inputs; SHA-256 and fixed
Git/blob identity are checked, and no signature claim is invented.

## Acceptance boundary

Trusted repository validation and source verification are not target build
success. Exact-head openEuler 24.03 LTS SP3 riscv64/RVA23 CI must still build,
run the complete upstream suite, install physical RPMs and pass the installed
smoke test. No local RPM, QEMU, backend or upstream tests were executed; no
auto-merge, target artifact or publication success is claimed.
