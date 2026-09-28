<!-- SPDX-License-Identifier: Apache-2.0 -->
# libconvert-binhex-perl

This package maps the frozen inventory's exact `libconvert-binhex-perl` key
to the official [Convert-BinHex 1.125](https://metacpan.org/dist/Convert-BinHex)
CPAN release. Its HTTPS archive was independently downloaded and pinned to
SHA-256 `513591b4be46bd7eb91e83197721b4a045a9753a3dd2f11de82c9d3013226397`,
matching the official CPAN `CHECKSUMS` index. The 34-entry archive has one
top-level tree with no traversal paths, links, or special files. CI verifies
the digest before building for openEuler 24.03 LTS SP3 `riscv64`/RVA23.

`%check` runs all six default upstream `t/*.t` files and the extended POD
test. One default file, `t/release-cpan-changes.t`, deliberately skips unless
upstream's `RELEASE_TESTING` flag is set; that skip is not counted as a pass.
The package retains the upstream `binhex.pl` and `debinhex.pl` commands. Its
installed-RPM smoke checks both commands parse, that the Perl module is
provided, and a known BinHex CRC. The upstream README still calls the API
alpha, although the CPAN release metadata labels 1.125 stable. The license
is the same GPL/Artistic choice as Perl itself.

This module is a dependency of MIME-tools' BinHex decoder proposed in PR
[#2160](https://github.com/yinjiayi/openeuler-riscv-packages/pull/2160).
Successful CI artifacts, if produced, will not by themselves prove public
RPM repository publication.
