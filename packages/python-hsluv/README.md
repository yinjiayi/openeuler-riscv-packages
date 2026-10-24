<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-hsluv

HSLuv 5.0.4 is the pure Python implementation of HSLuv revision 4 and HPLuv
color conversion. It is not a renderer, color hardware test or performance
benchmark. Target: openEuler 24.03 LTS SP3, riscv64, RVA23.

## Official source and license

PyPI's stable 5.0.4 matches upstream tag `v5.0.4`, immutable Git commit
`50a60aa6357fd5f743e39d8e29b771a645a83b4a`. The complete source archive at
`https://github.com/hsluv/hsluv-python/archive/50a60aa6357fd5f743e39d8e29b771a645a83b4a.tar.gz`
has SHA-256 `441e9105e18277b9a3cb86cb7bdd9fddc0d4e0f8a4bc7eed962afd4233d10030`.
All 11 regular archive files matched the non-truncated official Git tree's
blob identities; paths/duplicates/link types were checked without executing
source. The tag is unsigned and no detached release signature is provided.
`LICENSE.txt` contains the original MIT permission and copyright notice;
source, snapshot data and packaged notices are retained.

Discovery lineage remains the committed August 8 snapshot's five Python
distribution rows. Its unrelated `node-hsluv` row, merged by a historical
overbroad homepage association, is deliberately excluded rather than used as
evidence for this Python release. No external distribution recipe was executed
or copied, and the official release verification resolves the old catalog's
unverified-upstream source gap without rewriting that snapshot.

## Offline dependencies and namespace

There are no third-party runtime or test dependencies. Build tools are the
official target Python 3.11, setuptools >=38.6.0, wheel and pip; current target
metadata supplies 3.11.6, 68.0.0, 0.40.0 and 23.3.1 respectively. The complete
18,503-row official repository metadata had no hsluv Python distribution or
named provider, bound to fresh matching before/after repomd bytes. Complete
official filelists show no top-level hsluv module or distribution owner:
nbxmpp's private `nbxmpp/third_party/hsluv.py` has a separate import/file
namespace and is not a provider for this RPM. Fresh state/repomd binding of
all 1,192 supplemental names/Provides and filelists also shows no owner.
That unsigned HTTP metadata does not prove runner or signing trust.
No target installation or dependency solver run has occurred locally.
All package build/install/test phases are offline;
pip uses `--no-index --no-deps`, and setuptools sees its requirement installed.

## Complete original default tests

An **original-suite run** means the two unchanged upstream unittest methods,
not two colors or only an import smoke test. `test_snapshot` checks all 4,096
original snapshot colors in both directions, preserving tolerance 1e-10.
`test_within_rgb_range` uses the entire 73 x 21 x 21 hue/saturation/lightness
grid and original unclamped/clamped HSLuv/HPLuv functions, preserving tolerance
1e-11 and strict clamped bounds. No cases, branches or tolerances are removed.

The SPEC follows upstream's supported Python 3.11 CI lane exactly: generate
an sdist, unpack that locally generated sdist and invoke `setup.py test` there.
The original suite and 4,096-color presence are checked before the entrypoint.
All snapshot/test files are packaged under `/usr/share/python-hsluv/tests`;
installation smoke repeats the complete two-method suite against the installed
RPM's `hsluv.py` from an empty temporary directory with path/version assertions.
The source tree is never substituted for installed behavior. Normal target
RPM byte-compilation supplies the module cache. ZIP's 1980 timestamp bound is
handled deterministically while preserving later SOURCE_DATE_EPOCH values.

No RISC-V source patch is proposed. Numerical correctness can be tested in
QEMU user mode; this asserts neither native hardware nor timing validation.
Local checks are repository/schema and source-verification checks only, not
an upstream/backend/test execution or a target RPM/QEMU build. Target status
is `unknown` until exact-head CI build/install evidence succeeds. A submitted
proposal or repository checks do not imply a merge, publication or built RPM.

External source and patch licenses remain those of their respective upstream
projects. The repository license covers original packaging materials only.
