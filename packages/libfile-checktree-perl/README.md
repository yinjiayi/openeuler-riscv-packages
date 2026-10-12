<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-checktree-perl

This package maps the frozen inventory's exact `libfile-checktree-perl` key to
official stable CPAN [File-CheckTree 4.42](https://metacpan.org/dist/File-CheckTree).
The HTTPS source SHA-256
`66fb417f8ff8a5e5b7ea25606156e70e204861c59fa8c3831925b4dd3f155f8a`
matches the official CPAN `CHECKSUMS` index. Its 16 archive entries are confined
to one top-level tree and contain no traversal paths, links, or special files.
The archive includes the GPL/Artistic license choice used by Perl itself.
Target CI verifies the pinned digest before building on openEuler 24.03 LTS SP3
`riscv64`/RVA23.

`%check` runs the complete upstream default `make test` suite. Its functional
file declares 23 assertions; the two additional release-only test files
self-skip by upstream design unless `RELEASE_TESTING` is set. The installed-RPM
smoke checks the Perl auto-Provide and a successful file-tree validation.

Successful PR CI artifacts alone do not prove public RPM repository publication.
