# URI::Encode 1.1.1

This directory packages the frozen Ubuntu `liburi-encode-perl` 1.1.1-3
lineage from the immutable 2026-08-08 discovery snapshot as the official CPAN
URI-Encode-v1.1.1 release. The CPAN HTTPS tarball is 15,424 bytes and its
SHA-256 `4bb9ce4e7016c0138cf9c2375508595286efa1c8dc15b45baa4c47281c08243b`
matches the publisher's `CHECKSUMS`. Its entries are regular files and
directories, without symlinks or path traversal.

The distribution `LICENSE` grants redistribution under the same terms as
Perl 5 and includes GPL version 1 (with a later-version option) and Artistic
License 1.0. The module POD and README repeat the Perl grant; `Build.PL` and
`META.json` label it `perl`. The two text-only default tests have no conflicting
notice. No third-party binary or vendored build helper is included.

The checksum-bound official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata has no `perl-URI-Encode` RPM or `perl(URI::Encode)` provider. It
provides Encode 3.21, Carp 1.50, Module::Build 0.42.34, Test::More 1.302198
and version 0.99.30. The upstream two `t/*.t` tests are unchanged; `%check`
executes the entire default suite. Installed-RPM smoke checks the module
provider, encode/decode round trip and reserved-character mode. A green
hosted QEMU-user CI run demonstrates target functional behavior, not native
RISC-V performance or public RPM publication.
