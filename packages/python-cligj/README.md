<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-cligj

Packages Cligj 0.7.2 for openEuler 24.03 LTS SP3 riscv64/RVA23.
Upstream is BSD-3-Clause; Apache-2.0 covers original packaging only.

Official tag 0.7.2 points to immutable Git commit
b837c2cdd8811dff04f95cdfd0234efe6c638eab. All 21 original Git blobs,
full Mapbox BSD notice, complete tests/configuration and local GeoJSON fixtures
are preserved unchanged. The released PyPI sdist shares all originals except
setup.cfg's normalization/generated egg_info appendix; unchanged Git is used.
The actual Arch extra python-cligj 0.7.2-8 row is discovery lineage, not proof
that this package already exists or builds in the target repository.

Both engines run the original shared Travis command: py.test --cov cligj
--cov-report term-missing, with the full original test discovery and fixtures.
Original Python 3.6-3.8 matrix remains retained but unclaimed; running the shared
route on target Python 3.11 is not an upstream 3.11 matrix claim. Original
Python-version skip/xfail markers remain unmodified; no new filter, skip,
coverage threshold, source patch or disabled feature is introduced.
Coveralls after_success uploads and PyPI deployment are external publication
routes, preserved in the original configuration but not executed or claimed by
RPM verification; no uploader credential or network dependency is fabricated.
Runtime requires Click >=4.0; the original test extra requires pytest-cov.

Fresh complete non-runtime source copies prevent source-tree shadowing.
An exact original SHA-256 import guard checks buildroot/installed runtime without
preloading it before coverage. Installed smoke checks RPM ownership of every
original file, runtime module, archive and installed dist-info. Only explicitly
matched RPM-generated Python caches may be extra. Wheel construction is offline
with supplied setuptools/wheel and a fixed 1980 ZIP timestamp.

Trusted local repository tests and source-only verification are not target build
evidence. Original defaults/backend/RPM/installed execution occurs only in CI;
CI success, RPM/SRPM links and publication remain unverified.
