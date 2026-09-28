<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-c3-perl

This package maps the frozen inventory's exact libalgorithm-c3-perl key
to the official [Algorithm-C3 0.11](https://metacpan.org/dist/Algorithm-C3)
CPAN release. The official CPAN CHECKSUMS SHA-256 and an independent HTTPS
download agree on aaf48467765deea6e48054bc7d43e46e4d40cbcda16552c629d37be098289309.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its included LICENSE grants the same GPL/Artistic choice
as Perl. CI verifies the pinned source before building for openEuler
24.03 LTS SP3 riscv64/RVA23.

The target Everything repository's SHA-256-verified primary metadata
contains no perl-Algorithm-C3 RPM or perl(Algorithm::C3) provider, while
MakeMaker, Test::More, Test::Pod, and Test::Pod::Coverage are available.
The frozen inventory row is an external Ubuntu discovery record, not target
repository availability evidence.

Upstream ships 11 default t/ regression files and two separately registered
xt/ POD files. The RPM check runs all 13 files without excluding the
infinite-loop regression, whose SIGALRM guard can expose target QEMU timing
limits; a local host pass cannot prove its target outcome. The installed-RPM
smoke verifies the version and a diamond-inheritance C3 merge order.
CI build artifacts are not evidence of public RPM repository publication.
