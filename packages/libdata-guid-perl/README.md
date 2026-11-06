<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::GUID 0.051

The frozen Ubuntu `libdata-guid-perl` key maps to the official
[Data-GUID 0.051](https://metacpan.org/dist/Data-GUID) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `68ea77c73fca891382f206e12449094501b6fbf2e57f54902d5064227cfd8e2e`.
The ordinary-file archive has one top-level tree and no traversal paths. Its
`LICENSE` and the sole installed `Data::GUID` module POD explicitly grant
redistribution under Perl's GPL/Artistic terms, without a conflicting grant.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-GUID` RPM nor a `perl(Data::GUID)` provider. It uniquely supplies
all hard dependencies, including `perl(Data::UUID)` 1.226, `perl(Sub::Exporter)`
0.990, and `perl(Sub::Install)` 0.929, satisfying upstream minima. All five
default upstream test files remain unchanged. The local macOS Perl lacks
Data::UUID, so local upstream tests could not be run; this is not test success.
Exact-head target CI must prove all five default files run without skips, plus
the target RPM build, installed functional smoke and physical products. PR CI
products do not establish public RPM publication.
