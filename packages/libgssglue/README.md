# libgssglue 0.9

Libgssglue is a GSS-API dispatch library, not a mechanism implementation.
This package retains the upstream MIT Kerberos adapter configuration and
declares official krb5-libs. It is independent of the Kerberos mechanism
provider; it installs the separate libgssglue SONAME and private
/usr/include/gssglue/gssapi header, not the provider's global GSS header.

## Fixed source and lineage

The official stable tag libgssglue-0.9 is commit
ada76bdaec665f70505f0b3aefe871b873e7c4b6. The source is the maintainer's
published release upload, not a generated VCS archive:
https://gitlab.com/gsasl/libgssglue/uploads/7310f7060cdf240a4b8eaaf80a435986/libgssglue-0.9.tar.gz
SHA-256: 67ed16283dc45fe6acdd71adac76acf4a8af41eb75d0bb27cbb10c6110c72601.
Its 79 regular members were safely parsed and independently hashed.

The accompanying official detached signature was cryptographically verified
with normal current-time GnuPG (exit 0, VALIDSIG), in an isolated public keyring.
The maintainer's official blog
https://blog.josefsson.org/2022/12/24/openpgp-key-on-fst-01sz/
binds https://josefsson.org/key-20190320.txt and primary fingerprint
B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE. The signing subkey is
A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2.
The metadata records the detached signature as advisory: CI requires the
pinned full SHA-256; it does not claim an automatic signature recheck or
GnuPG owner-trust certification.

Discovery lineage is the frozen official Ubuntu row 0.9-2 in snapshot
discovery-20260808T165000Z-9a89920c269462cd. Distribution packaging was not
executed or substituted for upstream source.

## Rights and complete notices

The root README's BSD shorthand does not override the individual grants.
COPYING and all 79 original source members are preserved verbatim in
license-notices as .notice files before configure can rewrite generated files.
Their complete original copyright/permission/disclaimer text remains present.
Two full GNU license texts are added; the resulting 81 notice files have a
checksum manifest verified both in %check and from the installed package.

University of Michigan files use BSD-3-Clause. Sun and OpenVision-named
permission notices use HPND-sell-variant, including supporting-documentation
and no-name-publicity conditions. This OpenVision-named text is NOT the
different SPDX OpenVision Kerberos administration license. MIT-derived OID
sources retain HPND-export-US-modify, including the historical US export
warning, no-name-publicity and modified-software-marking conditions.
No upstream C source is patched; generated configure outputs and the
independent package regression driver are separately identified.
No assertion of legal export authorization is made.

install-sh retains the complete X11 permission and advertising-name
restriction plus its FSF public-domain-changes notice. FSFAP/FSFUL cover
their original unlimited-copy/modify/distribute and notice-preservation text.
LicenseRef-GNU-build-helper-exceptions means the original GNU helpers'
GPL-2.0-or-later / GPL-3.0-or-later grants with their actual Autoconf
distribution or Libtool distribution exceptions, retained per member with
complete GPL2/GPL3 texts. It is not a new relicensing or a shortened notice.
The independent API driver contains its full MIT grant. The source archive
and all original per-file notices remain in the SRPM.

## Defaults and runtime acceptance

Use the shipped configure, with no autoreconf/bootstrap or disabled feature.
Default shared and static libraries and linker-version-script detection stay
enabled; the expected libtool 1:0:0 product is libgssglue.so.1.0.0.
The original Automake make check runs TESTS=generic, one original program
with 20 PASS print sites. No original test source/runner is changed or removed.
The original doc/gssapi_mech.conf is used for target checks and installed
as /etc/gssapi_mech.conf with noreplace semantics.

Installed replay compiles the unchanged generic.c separately against
libgssglue, without a build-directory libtool wrapper/RPATH. Its source is
also preserved in license-notices/tests/generic.c.notice. Six additional
strict-assert cases check empty OID sets, custom OID membership/ownership,
generic local-name exact bytes, duplicate-name lifetime, invalid-input
statuses and actual configured mechanism discovery. A private unregistered
test name-type OID avoids claims about Kerberos realm/DNS configuration.
No authentication exchange, credential acquisition, privileged setuid
behavior, security certification, native hardware, timing or performance
validation is claimed.

Installed smoke clears inherited loader overrides, verifies notice and
post-strip driver checksums, replays both programs, and retains raw
LD_DEBUG=bindings stderr and its SHA-256 on success or failure.
Six exact normal-symbol calls from the absolute installed API driver must
resolve to the same physical installed libgssglue.so.1.0.0 file using -ef;
loader aliases such as /lib64/lp64d are not rejected by spelling alone.

## Admission and evidence limits

Fresh official 24.03-LTS-SP3 metadata was fully joined: 18,503 primary
packages and 2,207,942 file rows. The static dependency projection closes
79 packages / 36 versioned bounds and finds no missing declared provider,
command outside declared closure, standalone identity or owned-path hit.
This is not solver equivalence or acceptance of stale supplemental metadata;
the actual CI package set and full supplemental namespace remain merge gates.

The recipe requires no undeclared build fetch after verified sources are
materialized. Metadata network_during_build=false expresses that recipe
requirement; it is not proof that the current CI bridge is network-isolated.
Local work is limited to inert source/metadata review and trusted repository
validation/source verify-only, never upstream C compilation/execution or
RPM/QEMU builds. RISC-V build, original tests, install, physical RPM/SRPM
products and public publication require real exact-head CI evidence.
