<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-which-perl

This package maps the frozen inventory's exact `libfile-which-perl` key to
official stable CPAN [File-Which 1.27](https://metacpan.org/dist/File-Which).
The HTTPS source SHA-256
`3201f1a60e3f16484082e6045c896842261fc345de9fb2e620fd2a2c7af3a93a`
matches the official CPAN `CHECKSUMS` index. Its 44 archive entries have one
top-level tree without traversal paths, links, or special files. Target CI
verifies the digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` runs all three upstream default test files. The suite includes
19 assertions in its main functional file, with upstream platform-specific
skips on Unix where Windows, Cygwin, DOS, and VMS behavior cannot apply.
The installed-RPM smoke checks the Perl auto-Provide and executable lookup
through the actual search path. The archive includes the GPL/Artistic license
choice used by Perl itself.

Successful PR CI artifacts alone do not prove public RPM repository
publication.
