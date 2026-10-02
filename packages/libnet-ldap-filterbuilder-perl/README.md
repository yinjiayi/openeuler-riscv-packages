# Net::LDAP::FilterBuilder 1.200002

`libnet-ldap-filterbuilder-perl` packages official CPAN 1.200002 for
openEuler 24.03 LTS SP3 `riscv64` / RVA23. The frozen inventory's Ubuntu
`resolute/universe` and Debian `stable/main` source rows both record
1.200002-4; they establish distribution lineage, not source bytes or a
packaging recipe. The full SHA-256 in `sources.yaml` matches publisher
`OLIVER/CHECKSUMS` for the official archive.

## Rights and scope

The archive's distribution-wide `LICENSE` names University of Oxford and
explicitly permits redistribution and modification under GPL version 1 or
later OR Artistic License 1.0. The sole module's POD and `README` repeat the
Perl 5 dual grant. The four original test files, example, and build metadata
have no conflicting separate notices. The archive contains only regular files
and directories, with no vendored code or external data fixture.

## Verification boundary

Checksum-bound official SP3 RVA23 primary metadata has no
`perl-Net-LDAP-FilterBuilder` or `perl(Net::LDAP::FilterBuilder)` provider.
It supplies Perl, overload, MakeMaker, Test::More, Test::Pod 1.52 and
Test::Pod::Coverage 1.10. The SPEC requires both POD test providers to keep
all four unchanged upstream `t/*.t` files active. Local macOS source tests
passed 15 assertions, but POD coverage self-skipped because that optional
module is absent on the Mac; target exact-head CI must prove it actually
ran. Installed-RPM smoke checks provider resolution, wildcard escaping and
logical filter composition. These are functional checks under QEMU user mode,
not native RISC-V or a security guarantee about every LDAP use.
