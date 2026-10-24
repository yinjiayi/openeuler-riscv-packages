<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-dicttoxml

This directory packages upstream `https://github.com/quandyfactory/dicttoxml` version `1.7.16` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and lineage

The official PyPI source distribution is fixed by SHA-256
`6f36ce644881db5cd8940bee9b7cb3f3f6b7b327ba8a67d83d3e2caa0538bf9d`.
Its implementation, README, setup.py, MANIFEST.in and license are byte-identical
to upstream `v1.7.16` commit `5742af60e6e417d0b47ce59ac433f033507df2dc`.
The sdist contains the complete current module and build inputs without the
Git repository's historical distribution binaries. Updates inspect the official
PyPI simple source index, not a wheel or a mutable binary download.

Discovery uses the non-stale merged component
`github.com-quandyfactory-dicttoxml` in snapshot
`discovery-20260808T165000Z-9a89920c269462cd`, retaining the actual Debian,
Fedora and openSUSE source rows and their original observed versions. This is
not the stale AUR-only row or the separate `dicttoxml2` fork.

## Target namespace and dependencies

The source RPM is `python-dicttoxml`; its installable subpackage is
`python3-dicttoxml` and its import namespace is `dicttoxml`. Complete primary
and filelists scans of the fixed official RVA23 repository (18,503 RPMs) and
supplemental generation
`libstring-crc-cksum-perl-168799cc88e4f2ecedb72c084685a6fe8be65459-36796811483-1`
(1,192 RPMs) found no normalized name/capability, reverse dependency or installed
namespace owner. Cached metadata was hash/size-bound to fresh metadata/state;
the unsigned supplemental HTTP view is a collision check, not trust recovery.

Official build providers are Python 3.11.6, setuptools 68.0.0 and wheel 0.40.0;
setuptools satisfies the sdist's `>=61.0.0` requirement. The original setup.py
is also the upstream documented source build/install interface. There are no
non-standard-library runtime dependencies, network tests or native-only tests.

## Test and license boundaries

The fixed upstream tag and official sdist publish no test suite, tox, Makefile
or CI configuration. No original default gate is removed. `%check` adds offline
README API assertions for nesting, type attributes, roots, XML fragments,
escaping, null/numeric/date values, CDATA, custom item names, unique IDs,
return types and unsupported-type errors. Installed smoke checks the RPM,
distribution/import version and representative XML operations. These are
additive packaging regressions, not a claim of a complete upstream test suite.

Upstream README explicitly selects GNU GPL version 2 (`GPL-2.0-only`). The full
LICENCE.txt and README copyright notice (Ryan McGreal, 2012) are installed;
there are no packaging patches or additional borrowed-code notices.

Local validation only checks repository metadata, source hashes and packaging
policy. Actual riscv64 build/install/smoke results remain CI acceptance gates;
this directory does not assert build success or publication.
