<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-searchpath-perl

This package maps the frozen inventory's exact `libfile-searchpath-perl` key
to official stable CPAN
[File-SearchPath 0.07](https://metacpan.org/dist/File-SearchPath). The HTTPS
source SHA-256
`be4a2594ef1a7577e773135add940179c6a324e07e12bcfdc463cb49119a2cb9`
matches the official CPAN `CHECKSUMS` index. Its 21 archive entries have one
top-level tree without path traversal, links, or special files. Target CI
verifies the digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` runs the complete upstream test file and its 16 assertions. The
package preserves file, executable, directory, and legacy path lookup
behavior. `Env::Path` is recommended by upstream but optional; the test
supports either its presence or absence. The installed-RPM smoke checks the
Perl auto-Provide and executable lookup via `PATH`. Upstream declares GPL
version 2 or later in the module and build script but provides no standalone
license file.

Successful PR CI artifacts alone do not prove public RPM repository
publication.
