<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-mmagic-perl

This directory packages upstream `https://metacpan.org/release/KNOK/File-MMagic-1.30` version `1.30` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The canonical component is File::MMagic; the noarch RPM is `perl-file-mmagic`.
It provides file classification with the upstream magic data and does not
replace the `file` executable or its database.

The exact CPAN archive matches MetaCPAN release metadata and the publisher's
PAUSE-signed CHECKSUMS, verified at the historical signing time. Its complete
`COPYING` is installed unmodified and the original source notices remain in
`MMagic.pm`. The two LicenseRef identifiers denote the bundled file.kulp
and Ian F. Darwin notices, not a claim that those grants are a standard BSD
variant. The Apache Group terms and representative magic records, including
the seven FrameMaker rules, match the [Apache HTTP Server 1.3.9 upstream
source](https://github.com/apache/httpd/tree/3ed18253969134c39c56d9c91c77238e80d7f046).

`make test TEST_VERBOSE=1` invokes all seven unmodified original default
files; the separate installed smoke checks plain text and custom magic
recognition. No source patch or build-time network access is required.
RISC-V target build and installation are verified only by the hosted CI.
