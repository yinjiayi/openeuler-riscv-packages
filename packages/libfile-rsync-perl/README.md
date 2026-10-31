<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-rsync-perl

The frozen Ubuntu inventory row identifies official CPAN
[File-Rsync 0.49](https://metacpan.org/dist/File-Rsync). The archive's
SHA-256 `dd995df485f7334796d242efa277586d38d2544cace6ca0c3629a225df1e42d8`
matches publisher CHECKSUMS; README and module POD grant the same terms as
Perl. The archive has one top-level tree with ordinary files/directories.

Official RVA23 and the verified supplemental generation have no matching
module provider or file path. Official metadata supplies IPC::Run3 and
rsync 3.2.7. This is a snapshot check, not a guarantee of future state.

The original `test.pl` is retained in full; it exercises local rsync
operations in the isolated build tree. Target CI must prove the default tests,
RPM build and installation. The installed smoke checks the provider, module
version and argument construction; it is not a performance or remote-sync test.
