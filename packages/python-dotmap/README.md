<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-dotmap

This directory packages upstream `https://github.com/drgrib/dotmap` version `1.3.30` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The latest formal PyPI release is 1.3.30. Its source SHA-256 is
`5821a7933f075fb47563417c0e92e0b7c031158b4c9a6a7e56163479b658b368`.
The fixed official Git archive at `c7a778a95a01a7a0fd2f816a07c62de2478260c6`
has SHA-256 `a70f98a067dff5ca2ad799fe41aa013dc4f0fbee1611160639bf393162ea19a9`.
Its runtime module, whole tests, setup.py version 1.3.30 and full MIT license
match the formal release byte-for-byte. All twelve Git blobs were verified.
Current upstream HEAD is a later same-version rewrite and is not used;
the obsolete 1.3.8 Git tag is not substituted for the release. No release
archive signature is provided; fixed HTTPS origin, SHA-256 and Git blob
identity are required. No patch or borrowed distribution recipe is used.

Keep both original default commands: Makefile's `python3 -m unittest` and
Travis's `pytest dotmap/test.py`. The complete 29-method original suite,
setup/config/manifest/requirements/Makefile and Travis configuration remain
unchanged. Upstream's pytest 6.1.2 development pin is not a runtime or hard
backend requirement. The target provides pytest 7.4.4; its native unittest
collector supports this TestCase-only suite, but both full default commands
must still pass in target CI. No lint, typing or coverage gate is deleted.

Build offline with supplied setuptools 68.0.0, wheel 0.40.0 and pip 23.3.1.
Runtime is Python standard library only. The recipe does not invoke upstream
update.py, publishing commands or network dependency installation. Full
official/supplemental namespace and provider closure must remain fresh at
delivery; static closure does not prove an RPM transaction succeeds.

Installed acceptance verifies RPM ownership, version, original module/test
hashes and all 29 test methods before repeating both complete default suites
in separate writable tests-only directories. The unittest stage contains no
`dotmap` runtime package; the pytest stage retains `dotmap/test.py` without
`__init__.py`, so the installed regular package supplies imports. Build,
installation and compatibility success are pending CI, not local results.
