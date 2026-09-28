<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-bom-perl

This package maps the frozen inventory's exact `libfile-bom-perl` key to
official stable CPAN [File-BOM 0.18](https://metacpan.org/dist/File-BOM).
The release archive's SHA-256 is
`28edc43fcb118e11bc458c9ae889d56d388c1d9bc29997b00b1dffd8573823a3`,
matching the official CPAN `CHECKSUMS` index. Its 26 entries form one
top-level tree without path traversal, links, or special files. Target CI
verifies the digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` runs all six upstream test files. The release uses fixture setup and
teardown tests around BOM decoding, PerlIO, exception, and POD checks. Both
optional POD test dependencies are declared so those assertions run rather
than silently skip. The installed-RPM smoke checks the Perl auto-Provide and
UTF-8 BOM decoding. File::BOM uses the same GPL/Artistic choice as Perl.

A successful PR build and smoke will establish CI evidence, not public RPM
repository publication.
