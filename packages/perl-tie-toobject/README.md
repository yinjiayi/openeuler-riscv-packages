<!-- SPDX-License-Identifier: Apache-2.0 -->
# Tie::ToObject 0.03

This directory packages the official stable CPAN release for openEuler 24.03
LTS SP3, riscv64/RVA23. The binary RPM is `perl-Tie-ToObject`; the managed
package ID is `perl-tie-toobject`. It reuses an existing blessed object when
tying a Perl variable, without calling the object's tie constructor again.

Source: https://cpan.metacpan.org/authors/id/N/NU/NUFFIN/Tie-ToObject-0.03.tar.gz

SHA-256: `a31a0d4430fe14f59622f31db7f25b2275dad2ec52f1040beb030d3e83ad3af4`.

The mandatory archive SHA-256 matches current official release metadata and
its exact filename entry in CHECKSUMS. The available PAUSE-signed index is
advisory: its historical 2021 SHA-1 signature verifies mathematically under
the officially anchored primary fingerprint
`2E66557AB97C19C791AF8E20328DA867450F89EC`, but reports an expired signing
subkey. It is not a current-strength detached archive signature.

The bundled historical 2008 SHA-1 SIGNATURE mathematically verifies and all
six listed source-member hashes match. Its public key came from an untrusted
keyserver, so that check does not independently authenticate the author's
identity. Official CPAN HTTPS and the mandatory archive SHA-256 remain the
source basis; no required signature policy is relaxed.

`lib/Tie/ToObject.pm` explicitly grants the same terms as Perl itself and
names copyright holder Yuval Kogman (2008):
`GPL-1.0-or-later OR Artistic-1.0-Perl`. The license-bearing module is shipped
as `%license`. There is no bundled third-party installer; Makefile.PL uses
ordinary ExtUtils::MakeMaker and does not automatically fetch dependencies.

Discovery lineage is Debian stable (trixie), `libtie-toobject-perl` 0.03-6.
Current managed paths, normalized open-PR titles/filenames and target RPM
provides/filelists were screened before source acquisition. The locked target
supplies MakeMaker, Test::More, Test::use::ok/ok, Tie::RefHash, Scalar::Util
and Carp. Test::use::ok and `ok` are supplied by `perl-Test-Simple`.

The SPEC preserves the complete upstream `make test` default suite:
`t/tie.t`, ten assertions, without exclusions or modifications. The same
suite passed on the host; that is not a RISC-V build claim. Installed smoke
checks version, shared object identity, read/write alias behavior and the
original rejection paths. CI must separately build the noarch RPM/SRPM
inside the locked riscv64 image, run all tests and install the actual RPM.

No patch is needed. QEMU-user is suitable for these pure-Perl functional
checks; no native-kernel, hardware, timing or performance claim is made.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
