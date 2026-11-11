<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-easydict

This directory packages official stable easydict 1.13 for openEuler 24.03 LTS
SP3, Python 3.11, `riscv64`/RVA23. A source recipe is not a successful target
build or publication; both target acceptance and publication are pending.

Source0 is the official tag `1.13` at commit
`6df258e9bbeb2414bcb747b1691a6fbf5dfb7769`, SHA-256
`bfe062c8ae9a7d0acf1a069b2fc9d8aa2b9894c10d599b6d1768e4aa42088411`.
All eight Git blobs are retained unchanged, including workflow, module and
setup.py. The latest official PyPI stable is also 1.13; its sdist SHA-256 is
`b1135dedbc41c8010e2bc1f77ec9744c7faa42bce1a1c87416791449d6c87780`.
All six shared original sdist files equal the Git archive bytes. PyPI generated
metadata is not overlaid. GitHub API reports verified signed commit (`valid`);
this is not local PGP verification of the archive. Sources have SHA-256 binding.

The original default suite means the unchanged workflow's `ruff check` and
`python easydict/__init__.py -v`, retained in `%check`. Ruff uses `--isolated`
and a unique writable `/tmp/easydict-ruff.XXXXXX` cache to retain its original
unconfigured defaults instead of ancestor repository settings. The module has
60 statically counted doctest examples, not an observed passing runtime count.
Its original `doctest.testmod()` ignores failed-case counts. The complete
unchanged `python3 -m doctest -v easydict/__init__.py` is therefore also run to
propagate failures; no cases, source files, Ruff settings or features are
removed or patched. Installed smoke runs both complete commands against the
RPM-owned installed module, outside the source directory with PYTHONPATH unset,
and verifies import version, path and RPM ownership. Ruff checks the original
source/build tree, not a substituted installed-only subset. Other upstream
Python matrix versions are unverified; 3.11 is explicitly an original matrix
member. README examples involving simplejson are not an original default gate.

The original setuptools backend is unversioned, has no runtime dependencies,
and uses the supplied python3-setuptools 68.0.0. Complete official and
supplemental metadata were scanned (18,503 and 1,192 packages in each primary
and filelists document); there is no existing easydict provider, module owner
or reverse dependency. Supplied Python 3.11.6 and python3-ruff 0.7.0 (including
the Ruff executable) close the recipe dependencies. This is static supplier
evidence, not an executed DNF transaction or test success.

Original full `LICENSE` is LGPL version 3 and incorporates GPL version 3.
The conservative declared license is LGPL-3.0-only. Source1 supplies the full
unmodified incorporated GPL3 notice (29 June 2007), SHA-256
`3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`,
from the official GNU HTTPS mirror. It equals the complete original GNU
authority text. The original www.gnu.org endpoint failed two bounded TLS
reads in preparation; these raw retrieval failures remain recorded, while
the viable official ftp.gnu.org HTTPS mirror returned identical bytes without
weakening TLS. Both complete notices ship as `%license`; no source license is
replaced with the repository's packaging license.

Four frozen discovery rows (AUR 1.13-3, Debian 1.13-1, Fedora 1.10-11.fc44,
Ubuntu 1.13-1build1) remain historical lineage. Their discovery decision was
`unverified-upstream`; current fixed official tag/PyPI evidence resolves the
source identity without pretending the frozen distributions were current.
The canonical upstream is `github.com-makinacorpus-easydict`, distinct from
the binary RPM name `python3-easydict` and discovery directory `python-easydict`.

The first PR #2523 head `f1ca0d780f3402277e7958c247c35260dc43874e`,
Package CI run `38102104494`, failed before lint diagnostics or doctests:
Ruff 0.7.0 could not initialize `/workspace/.ruff_cache` on the read-only
repository mount. Prep, build and install phases had completed, but this is
not successful package acceptance. The original eight-file release has no
Ruff configuration. Official Ruff 0.7.0 source confirms `--isolated` ignores
all configuration files and uses unconfigured defaults, including the full
`E4`, `E7`, `E9`, `F` rule selection and no ignored rules; `--cache-dir` only
changes cache storage. This package-local environment repair does not alter
source, rule selection, discovered file inputs, or either complete doctest
gate. New-head target results remain pending; no lint/doctest pass is inferred.

Preparation executed only trusted repository validation and source-only
verification, not upstream imports, backend, doctests, Ruff, RPM or QEMU.
No successful build, RPM/SRPM URL, publication or runner trust restoration is
claimed. Package metadata requests no build network, but the current shared
build configuration enables container network. Fixed sources are reverified
cache-only; this does not establish a disconnected build/check container.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
