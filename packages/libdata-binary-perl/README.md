<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Binary 0.01

The frozen Ubuntu `libdata-binary-perl` key maps to the official
[Data-Binary 0.01](https://metacpan.org/dist/Data-Binary) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `4821a2de10ac7108f4dcb284a71b876981b0cb1ea6c5ed6afb177bf2e7cb8d73`.
The archive contains one top-level tree with ordinary files and directories
and no traversal paths. Its README grants Artistic License 2.0 for the
software, and the sole installed module identifies the same copyright holder
without a conflicting grant. CI verifies the pinned source before building.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Binary` RPM nor a `perl(Data::Binary)` provider. It uniquely supplies
Encode, base, Test::More and MakeMaker. The package retains both default
upstream test files; they passed nine local assertions without skips. Exact-head
target CI must prove the target build, full default test run and installed-RPM
functional smoke. PR CI products do not establish public RPM publication.
