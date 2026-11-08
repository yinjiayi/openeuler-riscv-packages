<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-carp

This directory packages [Test::Carp 0.2](https://metacpan.org/dist/Test-Carp)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The fixed CPAN archive
matches the publisher's signed PAUSE CHECKSUMS and the MetaCPAN release
digest. Discovery retains Debian stable and Fedora 44 GA source lineage.

The unmodified upstream README is installed as the license notice. Both it
and the original module POD grant redistribution under the same terms as
Perl. No source patches are required.

The build runs the complete upstream default MakeMaker suite, including POD
and POD coverage. The original optional author-only PerlCritic check can
self-skip if its development dependency is absent. Installed smoke exercises
message matching through the vendor-installed module.
