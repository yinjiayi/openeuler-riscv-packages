<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-littleutils

This directory packages upstream `https://github.com/alexmojaki/littleutils` version `0.2.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and lineage

The official stable `v0.2.4` tag resolves to
`5e548dd0af1c1548f08baae5e01dc464d642cbf3`; PyPI also identifies version
`0.2.4` and the same official repository. `sources.yaml` pins the commit
archive with SHA-256
`aa8fc5782aeeed3ec3818bc84356075c2909dc4ff932c1e51af9ce4a714fad31`.
All ten regular archive members match their official recursive Git-tree blob
IDs. The archive contains only regular files and directories: no links,
duplicate names or traversal entries. No release signature was provided or
independently verified; SHA-256 verification remains mandatory in CI.

The immutable snapshot
`discovery-20260808T165000Z-9a89920c269462cd` identifies this project as
`github.com-alexmojaki-littleutils`, with the exact retained Arch, Debian,
Fedora and openSUSE lineage recorded in `package.yaml`. The separate
SourceForge project called `littleutils` is unrelated and is not source
evidence for this package. Distribution recipes were not executed or copied.

## Target provider and namespace

This is a new managed directory but a **target-provider update**, not new
software absent from openEuler. The configured official repository supplies
`python3-littleutils` at `0:0.2.2-1.oe2403sp3`, with
`python-littleutils`, `python3dist(littleutils)` and
`python3.11dist(littleutils)` capabilities. Retain the binary name
`python3-littleutils` and its versioned `python-littleutils` alias; epoch zero
and upstream `0.2.4` are newer than `0.2.2`, rather than a higher-Epoch
downgrade or parallel owner of the module. Python distribution capabilities
are generated from the installed egg-info. The original binary RPM
(23,537 bytes, SHA-256
`b9cf5f4ab218035f723eb25ba5a569a22bbd083ce9a38edb1b37decb6d7714f6`)
was inspected inertly, including its headers and all payload member names.

Checksum-bound official primary and full filelists each contain 18,503
package records. The only owner of the `littleutils` module/distribution
namespace is that original `python3-littleutils` binary. There are no
official reverse dependencies on the package or distribution capabilities,
so no exact-version official subpackage constraint is waived. The metadata
is rebound to the fresh official `repomd.xml` SHA-256
`1e7269d6fa08e8f837e0ead13ad324e7f4ee5569dde6691378a61a806145bc14`.
This is static supplier/upgrade admission, not a target DNF transaction or
proof of installed-RPM behavior; CI must build and install the update.

The supplemental immutable generation
`libstring-crc-cksum-perl-168799cc88e4f2ecedb72c084685a6fe8be65459-36796811483-1`
was rebound to its fresh state SHA-256
`239709ad8655b85638e380a012d1040e10f39836988c21c1296bd68cb5379149`.
All 1,192 binary primary and full filelist records contain no littleutils
package/capability/reverse dependency or module owner. Unsigned supplemental
metadata does not establish GPG or runner trust; it is a bounded collision
check, not publication or installation proof.

Build requirements are official Python 3.11.6 development files,
setuptools 68.0.0, setuptools_scm 7.1.0 and wheel 0.40.0. The upstream has
no runtime dependencies beyond Python >=3.8. The SCM version is supplied
through the backend's supported `SETUPTOOLS_SCM_PRETEND_VERSION=0.2.4`
override because the fixed archive deliberately has no `.git`; this does
not replace the backend or rewrite upstream version fields.

## License and unchanged tests

The upstream `LICENSE` is MIT, copyright Alex Hall (2018). Its
`SimpleNamespace` compatibility implementation is explicitly copied from
the Python library documentation; retain the additional PSF-2.0 notice in
`LICENSE.cpython`, fetched unchanged from fixed CPython 3.11.13 commit
`498b971ea3673012a1d4b21860b229d55fc6e575` and independently pinned in
`sources.yaml`. Both notices are installed as `%license`; no source patch
is introduced. The unused fallback still ships and its notice is not
discarded merely because Python 3.11 provides `types.SimpleNamespace`.

Both upstream `tox.ini` and `.github/workflows/test.yml` use
`python littleutils/__init__.py`. `%check` preserves that exact driver for
the supported Python 3.11 lane: it invokes the original embedded doctests
and returns their failure count. No doctest, exception expectation or
feature is removed, and no network or native-kernel behavior is required.
The installed smoke test separately checks the distribution version,
container utilities, grouping and string handling.

Local verification is repository metadata/unit/golden validation and source
materialization only. No upstream code, build backend, doctest, RPM or QEMU
build was executed locally; real target build/install and publication proof
remain CI gates. `riscv_status: unknown` is intentional until that evidence
exists. No public RPM/SRPM URL is claimed by this proposal.
