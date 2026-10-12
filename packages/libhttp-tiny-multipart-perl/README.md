# HTTP::Tiny::Multipart 0.08

This directory maps the frozen Ubuntu `libhttp-tiny-multipart-perl` 0.08-2
lineage to the official CPAN HTTP-Tiny-Multipart-0.08 release. The 9,067-byte
HTTPS archive SHA-256
`ed0d43d470797c236be7f83e414e31561560ef3f88fab1ec09def20d98c361d6`
matches the publisher's `CHECKSUMS`. All archive entries are regular files or
directories; there are no symlinks or path-traversal entries.

The distribution `LICENSE` and module POD expressly grant Artistic License
2.0; `Makefile.PL` and release metadata agree. The text-only tests contain no
conflicting grant. The frozen inventory classified one discovery input as
`license-blocked`; the inspected official source, not that untrusted metadata,
provides the explicit redistribution grant used here.

The checksum-bound official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata has no `perl-HTTP-Tiny-Multipart` RPM or
`perl(HTTP::Tiny::Multipart)` provider. It supplies HTTP::Tiny 0.088, Carp,
File::Basename, MIME::Base64, ExtUtils::MakeMaker and Test::More. All six
upstream `t/*.t` files remain unchanged. Four functional files mock
`HTTP::Tiny::request`, so they do not make network requests; two author-only
files self-skip unless `AUTHOR_TESTING` is set. The local source run passed
29 functional assertions and reported those two upstream skips.

Installed-RPM smoke uses the same in-memory request mock to verify multipart
method, URL, content type and field body without contacting a server. Hosted
QEMU-user CI can establish functional behavior but not native RISC-V or a
published RPM repository link.
