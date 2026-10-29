<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Find 0.03

This package maps the frozen `libdata-find-perl` Debian/Ubuntu discovery key
to the official [Data-Find 0.03](https://metacpan.org/dist/Data-Find) CPAN
release. The official author-directory `CHECKSUMS` SHA-256 and an independent
HTTPS download agree on `a7e6bf23edca99cbdd86f0809bb439a87417614c91e66ce384ee09ecee00f016`.
The archive has one top-level directory, no traversal paths, and only regular
files and directories. The copyright holder's README and the sole installed
module's POD explicitly grant redistribution under the same GPL/Artistic
choice as Perl. The bundled `inc/MyBuilder.pm` supports the release build and
is not installed in the RPM.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Find` RPM nor a `perl(Data::Find)` provider. It uniquely supplies
Module::Build, Data::Dumper, Scalar::Util, Test::More, Test::Pod and
Test::Pod::Coverage; the last two are hard build dependencies so the upstream
POD tests cannot silently skip on target.

All four default upstream test files remain unchanged. Local macOS runs passed
10 assertions, with `t/pod-coverage.t` self-skipping only because the optional
module is absent there. Target exact-head CI must show all four files and no
skips, followed by installed-RPM smoke and physical artifact verification.
PR CI products do not establish public RPM publication.
